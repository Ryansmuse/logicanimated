import os
import numpy as np
import soundfile as sf
from kokoro_onnx import Kokoro

MODEL_DIR = os.path.expanduser("~/workspace/binary-search-animation/kokoro-model")
OUT_DIR = os.path.expanduser("~/workspace/youtube-logicanimated/stock-audio")
os.makedirs(OUT_DIR, exist_ok=True)

kokoro = Kokoro(
    os.path.join(MODEL_DIR, "kokoro-v1.0.onnx"),
    os.path.join(MODEL_DIR, "voices-v1.0.bin"),
)

SEGMENTS = [
    "LeetCode 121. Best Time to Buy and Sell Stock. Buy once, sell once on a later day, and keep the biggest profit. Checking every pair of days works, but it is far too slow.",
    "Here are six days of prices: seven, one, five, three, six, four. The best trade is hiding in there somewhere. We will find it in a single pass, tracking just two numbers.",
    "Number one: the cheapest price so far. That is your best possible buy day up to now. Number two: the best profit so far. Every day, ask one question. If I sold today, what would I make?",
    "Day one, price seven. Cheapest is seven, profit zero. Day two, price one. New cheapest: one. Day three, price five. Sell today and you make five minus one, which is four. Best profit: four.",
    "Day four, price three. Selling makes two. No better. Day five, price six. Six minus one is five. New best. Day six, price four makes three. So the answer stays five.",
    "Buy at one, sell at six, profit five. One pass through the array, two numbers tracked. That is O of n time, O of one space. And here is the whole solution in code.",
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
