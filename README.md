# logicanimated

**Short, visual explainers that make hard ideas click.**

Source archive for the YouTube channel [@logicanimated](https://www.youtube.com/channel/UCdV7eAyp0vh_rx3Qcggggxg) — every video's script, Manim source, narration audio, and final render, kept in the open.

## Videos

| # | Title | Published | Watch | Source |
|---|-------|-----------|-------|--------|
| 001 | Internal vs External Fragmentation — Memory Full AND Free? | Nov 15, 2026 | [YouTube Short](https://youtube.com/shorts/cSCvb2YmyH4) | [videos/001-fragmentation](videos/001-fragmentation) |

## How each video is made

1. **Script** — narration written out word-for-word, every number in the examples verified before writing (`script.md` in each video folder).
2. **Voice** — Kokoro TTS (`am_michael`), generated locally, one file per script segment; segments are loudness-normalized and joined with 0.4s pauses.
3. **Animation** — Manim (Community Edition), vertical 1080×1920. One scene per narration segment, each scene timed to its segment's *measured* audio length ("segment-locked"), so picture and voice can't drift apart.
4. **Verify** — segment durations checked with ffprobe, sample frames inspected visually, then the joined video is muxed with the narration and checked again.
5. **Publish** — uploaded to YouTube as a Short; the watch link is added to the table above.

## Repo layout

```
videos/NNN-slug/
  script.md     the script: narration, scene-by-scene visuals, upload copy
  src/          Manim scene file + Kokoro audio generator used for this video
  audio/        narration.mp3 + per-segment MP3s
  <Final>.mp4   the exact render that was uploaded
templates/      shared segment-locked scene base code (see segment_base.py)
```

Deliberately **not** in this repo: the Kokoro model files (~338 MB, over GitHub's file-size limit — they live on the build machine), Manim's partial-render cache, and WAV audio masters (the repo keeps MP3s; WAVs stay local). Each video folder is ~7 MB.

## Channel

- YouTube: [@logicanimated](https://www.youtube.com/channel/UCdV7eAyp0vh_rx3Qcggggxg)
- Topics: algorithms, operating systems, and CS fundamentals — animated step by step
