# Internal vs External Fragmentation — Video Script for @logicanimated

**Format:** Vertical Short, 9:16 (1080×1920)
**Runtime:** 169 words; estimated ~65s, actual recorded narration is 73.79s with pauses (see Audio note below)
**Voice:** Kokoro `am_michael`, speed 1.0 (channel voice, same as before)
**Style:** Manim dark stage (black → navy), memory drawn as one horizontal strip of blocks; programs in blue, free holes in grey, wasted space in red, fixes in gold/green — channel palette

**Verified examples (all arithmetic checked):**
- Internal: fixed block **64 KB**, program needs **40 KB** → **24 KB** trapped inside the block
- External: 100 KB strip = P1 20 | hole 10 | P2 25 | hole 15 | P3 10 | hole 20 → **45 KB free total**, biggest hole **20 KB** → a **30 KB** program cannot load
- Compaction: holes merge into one 45 KB space → 30 KB fits, 15 KB left over
- Paging tradeoff: 30 KB program in 4 KB pages = 8 pages (32 KB) → **2 KB** internal waste in the last page

---

## Narration — copy-paste block (for TTS)

Your memory can be full and free at the same time. That is fragmentation, and it comes in two kinds. Internal fragmentation is waste inside a block. Blocks are fixed-size — say, sixty-four kilobytes. A program needs forty, gets the whole block, and the leftover twenty-four kilobytes stay trapped inside, unusable by anyone else. External fragmentation is waste between blocks. Programs load and exit, leaving free holes scattered around: ten kilobytes here, fifteen there, twenty over there. That is forty-five kilobytes free in total. But a new program needs thirty in one piece. The biggest hole is twenty — so it cannot load, even though the memory is there. Two fixes. Compaction shuffles programs together so the holes merge into one big space. Paging chops memory into small fixed frames, so a program can grab any free frames, anywhere. But paging trades one kind for the other. Thirty kilobytes in four-kilobyte pages wastes two kilobytes inside the last page. You do not eliminate fragmentation. You choose where it lives.

## Narration — segmented (one file per segment, for Kokoro generation)

1. "Your memory can be full and free at the same time. That is fragmentation, and it comes in two kinds."
2. "Internal fragmentation is waste inside a block. Blocks are fixed-size — say, sixty-four kilobytes. A program needs forty, gets the whole block, and the leftover twenty-four kilobytes stay trapped inside, unusable by anyone else."
3. "External fragmentation is waste between blocks. Programs load and exit, leaving free holes scattered around: ten kilobytes here, fifteen there, twenty over there."
4. "That is forty-five kilobytes free in total. But a new program needs thirty in one piece. The biggest hole is twenty — so it cannot load, even though the memory is there."
5. "Two fixes. Compaction shuffles programs together so the holes merge into one big space. Paging chops memory into small fixed frames, so a program can grab any free frames, anywhere."
6. "But paging trades one kind for the other. Thirty kilobytes in four-kilobyte pages wastes two kilobytes inside the last page. You do not eliminate fragmentation. You choose where it lives."

---

## Scene-by-scene

| # | On-screen | Visual direction |
|---|---|---|
| 1 | **Full and free at the same time?** | A memory strip fades in: left half filled blue ("used"), right half grey ("free") — then a red **✗** stamps over it. Title lands: "FRAGMENTATION" |
| 2 | **INTERNAL** = waste *inside* a block · block = 64 KB · needs 40 KB · **24 KB wasted** | One big outlined block labeled 64 KB. A blue program bar fills the first 40 KB. The remaining 24 KB section fills with red hatch/stripes and a lock icon feel: label "trapped — no one else can use it" |
| 3 | **EXTERNAL** = waste *between* blocks · holes: 10 + 15 + 20 KB | The 100 KB strip: P1 (blue) / hole (grey, pulses) / P2 / hole (pulses) / P3 / hole (pulses), each segment labeled with its size as the voice names it |
| 4 | **Free total: 45 KB** · new program: 30 KB · biggest hole: 20 KB · **CAN'T LOAD** | Counter adds the holes: 10 + 15 + 20 = 45 KB free. A gold 30 KB block tries hole 1 (✗), hole 2 (✗), hole 3 (✗), then shakes/stops. Big red "CAN'T LOAD — memory still free" |
| 5 | **Fix 1: compaction** → one 45 KB space · **Fix 2: paging** → any free frames | Top: the strip's programs slide together, holes merge into one 45 KB space, the 30 KB block drops in ✓. Bottom: the strip redraws as a grid of small 4 KB frames, scattered frames light up |
| 6 | 30 KB = 8 pages × 4 KB · last page: **2 KB wasted** · *You don't eliminate fragmentation. You choose where it lives.* | Eight page boxes in a row; the program fills 7 fully and the 8th only halfway, the empty half marked red "2 KB internal waste". Closing line writes in gold, end card: CPU logo + "logicanimated" |

**Audio (generated Nov 15, 2026, Kokoro `am_michael`):** `fragmentation-audio/narration.mp3` / `narration.wav` — **73.79s total** (came in ~9s over the ~65s estimate; segments 2 and 3 read slower than the pace assumed). Loudness-normalized (mean −17.2 dB, peak −1.5 dB). Segments in `fragmentation-audio/seg1–6.wav`, with start times in the combined file: S1 0:00 (6.76s) · S2 0:07 (16.45s) · S3 0:24 (11.14s) · S4 0:36 (11.54s) · S5 0:47 (12.78s) · S6 1:01 (13.12s), 0.4s pauses between. Build the Manim scenes to these measured lengths, segment-locked like binary search v2.

**Video (built Nov 15, 2026):** `Fragmentation.mp4` — Manim scene file `fragmentation_video.py` (Frag1–Frag6), segment-locked to the measured audio (all six segments within 0.03s of their targets), spread portrait layout. 1080×1920, 30 fps, 73.79s, H.264 + AAC, ~5.2 MB, audio mean −17.2 dB / peak −1.4 dB. Cue frames visually verified (hook, internal block, holes strip, CAN'T LOAD, compaction/paging fixes after a label-overlap fix in Frag5, paging tradeoff close). Not yet uploaded.

**Pinned comment / end-screen line:** "Next: paging, animated — how your computer pretends memory is infinite (virtual memory)"

---

## Upload copy (ready to paste)

**Title (recommended):** Internal vs External Fragmentation — Memory Full AND Free?
Alternatives: Why Your RAM Fails With 45 KB Still Free · Fragmentation Explained in 60 Seconds, Animated

**Description:**
Short, visual explainers that make hard ideas click.

Internal vs external fragmentation, animated: internal fragmentation is space wasted *inside* an allocated block (a 40 KB program in a fixed 64 KB block traps 24 KB). External fragmentation is space wasted *between* blocks — 45 KB free in holes of 10, 15 and 20 KB still can't fit a 30 KB program. Compaction and paging fix it, but paging trades external fragmentation for a little internal.

From operating systems / memory management — fixed partitions, dynamic partitions, compaction, and paging.

#operatingsystems #computerscience #programming #coding #techexplained

**Tags:** internal fragmentation, external fragmentation, fragmentation operating system, memory management, operating systems, paging, compaction, fixed partition, dynamic partition, computer science, os concepts, gate computer science, programming, cs student, virtual memory

**Thumbnail text (if a long-form version is made):** FULL... BUT FREE? — the strip with red ✗ over the 30 KB block
