import os
import numpy as np
import soundfile as sf
from kokoro_onnx import Kokoro

MODEL_DIR = os.path.expanduser("~/workspace/binary-search-animation/kokoro-model")
OUT_DIR = os.path.expanduser("~/workspace/youtube-logicanimated/fragmentation-audio")
os.makedirs(OUT_DIR, exist_ok=True)

kokoro = Kokoro(
    os.path.join(MODEL_DIR, "kokoro-v1.0.onnx"),
    os.path.join(MODEL_DIR, "voices-v1.0.bin"),
)

SEGMENTS = [
    "Your memory can be full and free at the same time. That is fragmentation, and it comes in two kinds.",
    "Internal fragmentation is waste inside a block. Blocks are fixed-size — say, sixty-four kilobytes. A program needs forty, gets the whole block, and the leftover twenty-four kilobytes stay trapped inside, unusable by anyone else.",
    "External fragmentation is waste between blocks. Programs load and exit, leaving free holes scattered around: ten kilobytes here, fifteen there, twenty over there.",
    "That is forty-five kilobytes free in total. But a new program needs thirty in one piece. The biggest hole is twenty — so it cannot load, even though the memory is there.",
    "Two fixes. Compaction shuffles programs together so the holes merge into one big space. Paging chops memory into small fixed frames, so a program can grab any free frames, anywhere.",
    "But paging trades one kind for the other. Thirty kilobytes in four-kilobyte pages wastes two kilobytes inside the last page. You do not eliminate fragmentation. You choose where it lives.",
]

PAUSE_S = 0.4

all_samples = []
sr_global = None
for i, text in enumerate(SEGMENTS, start=1):
    samples, sr = kokoro.create(text, voice="am_michael", speed=1.0, lang="en-us")
    sr_global = sr
    out = os.path.join(OUT_DIR, f"seg{i}.wav")
    sf.write(out, samples, sr)
    print(f"{out}: {len(samples)/sr:.2f}s @ {sr}Hz")
    all_samples.append(samples)
    if i < len(SEGMENTS):
        all_samples.append(np.zeros(int(PAUSE_S * sr), dtype=samples.dtype))

combined = np.concatenate(all_samples)
raw_path = os.path.join(OUT_DIR, "narration_full_raw.wav")
sf.write(raw_path, combined, sr_global)
print(f"{raw_path}: {len(combined)/sr_global:.2f}s total (incl. {PAUSE_S}s pauses)")
