"""Mix narration + music bed + SFX cues into one track, then (optionally) mux.

Usage:
  python mix_audio.py --narration fits-audio/narration_full.wav \
      --cues fits_cues.json --out fits_final_audio.wav [--mux fits_video_only.mp4 --final FirstFitVsBestFit.mp4]

Bed defaults to music/bed-meditation-impromptu-01.mp3 at -24 dB with 1.5s fade-in
and 2.5s fade-out, trimmed to the narration length. Cues come from sfx/core/.
A limiter guards the sum. Part of the logicanimated pipeline (video 003+).
"""
import argparse, json, os, subprocess, sys

BASE = os.path.dirname(os.path.abspath(__file__))


def probe_dur(path):
    out = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                          "-of", "csv=p=0", path], capture_output=True, text=True)
    return float(out.stdout.strip())


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--narration", required=True)
    ap.add_argument("--cues", required=True)
    ap.add_argument("--bed", default=os.path.join(BASE, "music", "bed-meditation-impromptu-01.mp3"))
    ap.add_argument("--bed-db", type=float, default=-10.0)  # Ryan-tuned Nov 15: -24 dB buried the bed (-43 dB in pauses, inaudible); -13 was audible; -10 is his pick (bed ~-29 dB in pauses, ~7 dB under the voice). Verify a pause window before delivering.
    ap.add_argument("--out", required=True)
    ap.add_argument("--mux", default=None)
    ap.add_argument("--final", default=None)
    args = ap.parse_args()

    dur = probe_dur(args.narration)
    cues = json.load(open(args.cues))
    inputs = ["-i", args.narration, "-i", args.bed]
    for c in cues:
        inputs += ["-i", os.path.join(BASE, "sfx", "core", c["file"])]
    fc = []
    bed_gain = 10 ** (args.bed_db / 20)
    fc.append(f"[1:a]atrim=0:{dur:.2f},asetpts=PTS-STARTPTS,afade=t=in:st=0:d=1.5,"
              f"afade=t=out:st={dur - 2.5:.2f}:d=2.5,volume={bed_gain:.4f}[bed]")
    labels = ["[0:a]", "[bed]"]
    for i, c in enumerate(cues):
        g = 10 ** (c["gain_db"] / 20)
        fc.append(f"[{i + 2}:a]adelay={int(c['t'] * 1000)}:all=1,volume={g:.4f}[c{i}]")
        labels.append(f"[c{i}]")
    fc.append(f"{''.join(labels)}amix=inputs={len(labels)}:normalize=0,alimiter=limit=0.89,aresample=48000[mix]")
    cmd = ["ffmpeg", "-y", "-v", "error"] + inputs + ["-filter_complex", ";".join(fc),
                                                      "-map", "[mix]", "-c:a", "pcm_s16le", args.out]
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        print(r.stderr[-1500:]); sys.exit(1)
    print("mixed:", args.out, round(probe_dur(args.out), 2), "s")
    if args.mux and args.final:
        r = subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", args.mux, "-i", args.out,
                            "-map", "0:v", "-map", "1:a", "-c:v", "copy", "-c:a", "aac",
                            "-b:a", "192k", "-shortest", args.final], capture_output=True, text=True)
        if r.returncode != 0:
            print(r.stderr[-1500:]); sys.exit(1)
        print("muxed:", args.final, round(probe_dur(args.final), 2), "s")


if __name__ == "__main__":
    main()
