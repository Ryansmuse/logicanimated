"""Kokoro narration for the hole-fits video (am_michael, same pipeline)."""
import os
import numpy as np
import soundfile as sf
from kokoro_onnx import Kokoro

BASE = os.path.dirname(os.path.abspath(__file__))
MODEL_DIR = os.path.expanduser("~/workspace/binary-search-animation/kokoro-model")
OUT = os.path.join(BASE, "fits-audio")
os.makedirs(OUT, exist_ok=True)

SEGMENTS = [
    "Four strategies get the same six holes, and the same two-megabyte process. And they pick four different holes. This is how your operating system decides where a program lives in memory.",
    "With dynamic partitioning, memory is carved up at runtime, and every free block is called a hole. Six holes: one, three, one point five, four, six, and two megabytes. A two-megabyte process arrives. Where does it go?",
    "First-fit scans from the start and takes the first hole that fits: the three, leaving one megabyte. Next-fit resumes where the last search stopped, so it skips ahead to the four.",
    "Best-fit scans every hole and takes the smallest one that fits, the two. A perfect fit, zero wasted. But it leaves tiny slivers everywhere, so it fragments memory the worst.",
    "Worst-fit takes the largest hole, the six, leaving four behind. The leftover stays useful, but you burned your biggest space on a small process.",
    "Same holes, same process, four different answers. In practice, first-fit and next-fit win: fast, balanced, no full scan. The O S is not hunting for the perfect hole. It takes a good one, fast.",
]

kokoro = Kokoro(os.path.join(MODEL_DIR, "kokoro-v1.0.onnx"), os.path.join(MODEL_DIR, "voices-v1.0.bin"))
SR = 24000
PAUSE = np.zeros(int(0.4 * SR), dtype=np.float32)
parts, durations = [], []
for i, text in enumerate(SEGMENTS, 1):
    samples, sr = kokoro.create(text, voice="am_michael", speed=1.0, lang="en-us")
    samples = np.asarray(samples, dtype=np.float32)
    sf.write(os.path.join(OUT, f"seg{i}.wav"), samples, SR)
    durations.append(len(samples) / SR)
    parts.append(samples)
    if i < len(SEGMENTS):
        parts.append(PAUSE)
full = np.concatenate(parts)
peak = np.max(np.abs(full))
full = full * (10 ** (-1.5 / 20) / peak)
sf.write(os.path.join(OUT, "narration_full.wav"), full, SR)
print("segments:", [round(d, 2) for d in durations])
print("total with pauses:", round(len(full) / SR, 2))
