# Best Time to Buy and Sell Stock — LeetCode 121 — Video Script

Channel: logicanimated (@logicanimated) · vertical Short, 1080×1920
Status: BUILT Nov 15, 2026 at Ryan's request ("make another video"). Kokoro audio 76.26s total (segments 12.69/11.50/12.89/13.74/12.05/11.39, mean −17.4 dB). Segment-locked Manim video: `BestTimeToBuyAndSellStock.mp4`, 1080×1920, 76.26s, scenes within 0.08s of targets, frame-verified incl. safe-box check (all content inside x ±1.7, y −2.3…+3.2; code endcard at y −2.08). Not yet uploaded.
**Layout: SAFE-ZONE compliant** (see SAFE_ZONES.md) — all critical content inside x ±1.7, y −2.3…+3.2; chart built 3.4 units wide, centered; nothing essential in the bottom overlay zone.

## The example (verified by running the algorithm, Nov 15, 2026)

prices = [7, 1, 5, 3, 6, 4] — trace (cheapest so far / sell today / best profit):
- Day 1: 7 → cheapest 7, sell 0, best 0
- Day 2: 1 → cheapest 1, sell 0, best 0
- Day 3: 5 → cheapest 1, sell 4, best 4
- Day 4: 3 → cheapest 1, sell 2, best 4
- Day 5: 6 → cheapest 1, sell 5, best 5 ← buy at 1 (day 2), sell at 6 (day 5)
- Day 6: 4 → cheapest 1, sell 3, best 5
**Answer: 5.** Brute force would check 15 buy/sell pairs for just these 6 days (n² growth).

## Narration script (Kokoro `am_michael`, numbers written out for TTS)

1. **Hook** — "LeetCode 121. Best Time to Buy and Sell Stock. Buy once, sell once on a later day, and keep the biggest profit. Checking every pair of days works, but it is far too slow."
2. **Setup** — "Here are six days of prices: seven, one, five, three, six, four. The best trade is hiding in there somewhere. We will find it in a single pass, tracking just two numbers."
3. **The idea** — "Number one: the cheapest price so far. That is your best possible buy day up to now. Number two: the best profit so far. Every day, ask one question. If I sold today, what would I make?"
4. **Trace, days 1–3** — "Day one, price seven. Cheapest is seven, profit zero. Day two, price one. New cheapest: one. Day three, price five. Sell today and you make five minus one, which is four. Best profit: four."
5. **Trace, days 4–6** — "Day four, price three. Selling makes two. No better. Day five, price six. Six minus one is five. New best. Day six, price four makes three. So the answer stays five."
6. **Payoff + code** — "Buy at one, sell at six, profit five. One pass through the array, two numbers tracked. That is O of n time, O of one space. And here is the whole solution in code."

Word count: ~187 → est. ~70–80s at the fragmentation video's Kokoro pace.

## Scene plan (segment-locked: one Manim scene per narration segment)

| # | Visuals (all inside the safe box) |
|---|---|
| 1 | "LEETCODE 121" header, "Best Time to Buy and Sell Stock" title, buy→sell arrow chips ("BUY once · SELL once · later"), then "every pair of days" with a red ✗ "too slow" |
| 2 | Bar chart of the 6 prices (3.4 units wide, centered, baseline y −1.2, price labels on bars, day labels under), caption "find the best trade in ONE pass" |
| 3 | Two tracker cards side by side (each ~1.62 wide): "CHEAPEST SO FAR" (blue) and "BEST PROFIT" (gold), question card under: "If I sold today, what would I make?" |
| 4 | Chart + trackers live: day highlight 1→3, cheapest 7→1, callout "5 − 1 = 4", best-profit card flips to 4 |
| 5 | Chart continues: days 4→6, callout "6 − 1 = 5" gold, "ANSWER 5" badge, buy/sell markers on day 2 and day 5 bars |
| 6 | Code block (Python, fitted ≤3.4 wide) + chips "TIME O(n)" "SPACE O(1)" + endcard "logicanimated" — all inside the safe box (endcard ~y −1.9, not at the frame bottom) |

Python solution shown in scene 6:
```python
def maxProfit(prices):
    cheapest = prices[0]
    best = 0
    for p in prices:
        cheapest = min(cheapest, p)
        best = max(best, p - cheapest)
    return best
```

## Upload copy (for when it's built)

**Title (recommended):** Best Time to Buy and Sell Stock — LeetCode 121 in 60 Seconds
Alternatives: "LeetCode 121 Solved in One Pass — Buy Low, Sell High" · "Max Profit in One Pass — LeetCode 121 Explained"

**Description:**
Short, visual explainers that make hard ideas click.

LeetCode 121 — Best Time to Buy and Sell Stock. Given daily prices [7, 1, 5, 3, 6, 4], buy once and sell once on a later day for the maximum profit.

The one-pass trick: track the cheapest price seen so far and the best profit seen so far. Each day, test selling today (today's price minus the cheapest before it). Answer here: buy at 1, sell at 6, profit 5 — in O(n) time and O(1) space, no pair-checking.

From LeetCode / algorithms — arrays, one-pass scans, greedy tracking.

#leetcode #algorithms #coding #programming #computerscience

**Tags:** leetcode 121, best time to buy and sell stock, leetcode, max profit stock, one pass algorithm, greedy algorithm, arrays, coding interview, data structures and algorithms, dsa, programming, computer science, python leetcode, coding

**Pinned comment idea:** "What threw you the first time: selling before buying, or forgetting you can make 0 by not trading? Next up: maximum subarray (Kadane's)."

## Production notes
- Segment-locked build (one scene per segment, padded to measured Kokoro audio + 0.4s), same pipeline as the fragmentation video.
- SAFE ZONES: chart/trackers/code all ≤3.4 units wide centered; headers ≤ y 3.2; lowest essential element ≥ y −2.3. Verify one frame per scene against the safe box before upload.
- Audio: local Kokoro `am_michael` only, no downloads.
