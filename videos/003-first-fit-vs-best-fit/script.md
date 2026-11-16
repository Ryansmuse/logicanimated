# Video 003 — First-Fit vs Best-Fit vs Worst-Fit (Hole Selection)

Source: Ryan's OS course deck `mainmemory-dynamic__3.pptx`, slides 33–37 ("Selecting a Hole").
Uses the deck's EXACT example: holes H1–H6 = 1M, 3M, 1.5M, 4M, 6M, 2M; a 2M process arrives.
Slide answers (verified by hand): First-fit → H2 (3M, leftover 1M) · Next-fit (prev search stopped at H2) → H4 (4M, leftover 2M) · Best-fit → H6 (2M, leftover 0) · Worst-fit → H5 (6M, leftover 4M).
Verdict per slide 37: first-fit/next-fit fastest and most balanced; best-fit fragments worst (smallest leftovers).

Format: 1080×1920 Short, Kokoro `am_michael`, segment-locked Manim scenes.
FIRST video with sound design: Meditation Impromptu bed (−24 dB) + Kenney SFX cues (see fits build's cue sheet).
Layout: SAFE ZONES only (x ±1.7, y −2.3…+3.2). Hole grid = 2 rows × 3 cards, 3.3 units wide.

## Narration (6 segments)

1. HOOK — "Four strategies get the same six holes, and the same two-megabyte process. And they pick four different holes. This is how your operating system decides where a program lives in memory."
2. SETUP — "With dynamic partitioning, memory is carved up at runtime, and every free block is called a hole. Six holes: one, three, one point five, four, six, and two megabytes. A two-megabyte process arrives. Where does it go?"
3. FIRST + NEXT — "First-fit scans from the start and takes the first hole that fits: the three, leaving one megabyte. Next-fit resumes where the last search stopped — so it skips ahead to the four."
4. BEST — "Best-fit scans every hole and takes the smallest one that fits — the two. A perfect fit, zero wasted. But it leaves tiny slivers everywhere, so it fragments memory the worst."
5. WORST — "Worst-fit takes the largest hole — the six — leaving four behind. The leftover stays useful, but you burned your biggest space on a small process."
6. VERDICT — "Same holes, same process, four different answers. In practice, first-fit and next-fit win — fast, balanced, no full scan. The OS is not hunting for the perfect hole. It takes a good one, fast."

## On-screen text
- S1: ONE PROCESS. / FOUR ANSWERS. / title chip: FIRST-FIT · NEXT-FIT · BEST-FIT · WORST-FIT
- S2: header DYNAMIC PARTITIONING; cards H1 1M, H2 3M, H3 1.5M / H4 4M, H5 6M, H6 2M; chip NEW PROCESS: 2 MB
- S3: FIRST-FIT → scan H1 (too small, error tick) → H2 picked, chip LEFTOVER 1 MB; then NEXT-FIT → resume marker at H2 → scan H3 → H4 picked, chip LEFTOVER 2 MB
- S4: BEST-FIT → sweep all → H6 picked, chip LEFTOVER 0 — PERFECT FIT; warning line: TINY SLIVERS → MOST FRAGMENTATION
- S5: WORST-FIT → H5 picked, chip LEFTOVER 4 MB; line: BIG LEFTOVER — BIGGEST HOLE BURNED
- S6: verdict table FIRST→H2 · NEXT→H4 · BEST→H6 · WORST→H5; FASTEST + BALANCED: FIRST / NEXT; closing: GOOD ONE, FAST.

## Upload metadata (when approved)
- Title: First-Fit vs Best-Fit vs Worst-Fit — Where Does the OS Put Your Program?
- Description: the four strategies on one example from class + MacLeod credit line (REQUIRED, CC BY) + channel line.
- Tags: operating systems, memory management, first fit, best fit, worst fit, next fit, dynamic partitioning, external fragmentation, os concepts, computer science, coding interview, learn to code, cs student, programming basics, memory allocation
- Pinned comment idea: "Which fit does your OS prof swear by — and is paging just the OS giving up on all four?"
