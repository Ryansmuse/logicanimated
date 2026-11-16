# YouTube Shorts safe zones — production rule (from Ryan's phone check, Nov 15, 2026)

Ryan watched the published fragmentation Short on his phone and reported parts of the
video are clipped and cannot be seen. Causes: the Shorts player's own UI overlays
(bottom channel/title/subscribe block, right-side like/comment/share rail, top bar),
plus taller phones (e.g. 20:9) crop the left/right edges of a 9:16 video when filling
the screen (~12% per side).

## The rule for every future @logicanimated video

Canvas: 1080×1920, Manim frame 4.5 × 8.0 units (240 px per unit).

**Critical content box — everything the viewer must read stays inside:**
- x: −1.7 … +1.7 units (middle 3.4 units / ~816 px, centered)
- y: −2.3 … +3.2 units

**Dead zones (decorative/background only, never essential text or visuals):**
- Bottom: y < −2.3 (bottom ~410 px) — Shorts overlay: channel name, title, subscribe
- Top: y > +3.2 (top ~190 px) — Shorts top bar
- Sides: |x| > 1.7 — side crop on tall phones + right action rail
  (extra care: right rail buttons sit mid-height, roughly y −0.5…−2.0 at the right edge)

**Layout consequences:**
- Wide visuals (12-cell arrays, 100 KB memory strips) must be designed ≤3.4 units wide
  and centered — taller cells, or a two-row layout — never the 4.2–4.3 units used in the
  first two videos.
- Endcards, captions, and payoff lines move UP into the safe box; nothing important
  below y = −2.3. (In the fragmentation video the "...with 45 KB still free" line at
  y −3.6 and the endcards at y −3.55/−3.78 sat in the dead zone.)
- Before uploading, verify one frame per scene against this box, not just for
  overlaps/clipping inside the render.
