"""Video 003: First-Fit vs Next-Fit vs Best-Fit vs Worst-Fit (hole selection).

Uses Ryan's course-deck example: holes 1, 3, 1.5, 4, 6, 2 MB; a 2 MB process.
Answers: FIRST->H2, NEXT->H4, BEST->H6, WORST->H5.
Segment-locked to Kokoro narration; SAFE-ZONE layout (x +-1.7, y -2.3..+3.2).
Render: manim render -qm --resolution 1080,1920 fits_video.py Fits1..Fits6
"""
from manim import *

config.frame_width = 4.5
config.frame_height = 8.0

INK = "#e8eef5"
MUTE = "#9fb4c8"
GOLD = "#e8b64c"
HOLE_FILL = "#22354d"
HOLE_EDGE = "#7fa6c9"
SOFT_RED = "#e08a8a"
SEG = [12.57, 15.30, 11.52, 11.90, 9.73, 13.72]
TARGETS = [s + 0.4 for s in SEG[:-1]] + [SEG[-1]]

HOLES = [("H1", "1 MB"), ("H2", "3 MB"), ("H3", "1.5 MB"),
         ("H4", "4 MB"), ("H5", "6 MB"), ("H6", "2 MB")]
XS = [-1.11, 0.0, 1.11]
YS = [1.55, 0.45]


def fit(mob, max_w=None, max_h=None):
    if max_w and mob.width > max_w:
        mob.scale(max_w / mob.width)
    if max_h and mob.height > max_h:
        mob.scale(max_h / mob.height)
    return mob


def txt(s, size=34, color=INK, weight=BOLD):
    return Text(s, font_size=size, color=color, weight=weight)


class FitsBase(Scene):
    def pad_to(self, target, start):
        left = target - (self.renderer.time - start)
        if left > 0:
            self.wait(left)

    def header(self, s, y=2.78, size=36, color=INK):
        h = fit(txt(s, size=size, color=color), max_w=3.35)
        h.move_to([0, y, 0])
        return h

    def hole_grid(self):
        cards = []
        for i, (h, sz) in enumerate(HOLES):
            x, y = XS[i % 3], YS[i // 3]
            rect = RoundedRectangle(corner_radius=0.07, width=1.02, height=0.92,
                                    stroke_color=HOLE_EDGE, stroke_width=3.5,
                                    fill_color=HOLE_FILL, fill_opacity=1.0)
            rect.move_to([x, y, 0])
            hl = txt(h, size=19, color=MUTE).move_to([x, y + 0.27, 0])
            st = fit(txt(sz, size=30), max_w=0.9).move_to([x, y - 0.14, 0])
            cards.append(VGroup(rect, hl, st))
        return cards

    def ring(self, card):
        r = RoundedRectangle(corner_radius=0.09, width=1.14, height=1.04,
                             stroke_color=GOLD, stroke_width=6, fill_opacity=0)
        r.move_to(card[0].get_center())
        return r

    def pick(self, card):
        card[0].set_fill(GOLD, opacity=0.92)
        card[1].set_color("#1a1a1a")
        card[2].set_color("#1a1a1a")

    def unpick(self, card):
        card[0].set_fill(HOLE_FILL, opacity=1.0)
        card[1].set_color(MUTE)
        card[2].set_color(INK)

    def chip(self, s, y=-0.85, color=GOLD, fill="#141c26"):
        t = fit(txt(s, size=27, color=color), max_w=3.0)
        box = RoundedRectangle(corner_radius=0.09, width=t.width + 0.34, height=0.52,
                               stroke_color=color, stroke_width=3,
                               fill_color=fill, fill_opacity=1.0)
        g = VGroup(box, t)
        g.move_to([0, y, 0])
        return g


class Fits1(FitsBase):
    def construct(self):
        start = self.renderer.time
        t1 = fit(txt("ONE PROCESS.", size=44), max_w=3.35).move_to([0, 2.62, 0])
        t2 = fit(txt("FOUR ANSWERS.", size=44, color=GOLD), max_w=3.35).move_to([0, 1.98, 0])
        self.play(FadeIn(t1, shift=UP * 0.15), FadeIn(t2, shift=UP * 0.15), run_time=0.8)
        mini = VGroup()
        for i, (_, sz) in enumerate(HOLES):
            r = RoundedRectangle(corner_radius=0.05, width=0.48, height=0.6,
                                 stroke_color=HOLE_EDGE, stroke_width=3,
                                 fill_color=HOLE_FILL, fill_opacity=1.0)
            r.move_to([-1.36 + i * 0.545, 0.92, 0])
            st = fit(txt(sz.replace(" MB", ""), size=21), max_w=0.42).move_to(r.get_center())
            mini.add(VGroup(r, st))
        self.wait(2.4)
        self.play(LaggedStart(*[FadeIn(m) for m in mini], lag_ratio=0.12), run_time=1.6)
        chip = self.chip("NEW PROCESS: 2 MB", y=-0.02)
        self.play(FadeIn(chip, shift=UP * 0.12), run_time=0.6)
        names = fit(txt("FIRST · NEXT · BEST · WORST", size=24, color=MUTE), max_w=3.3).move_to([0, -1.05, 0])
        self.wait(1.2)
        self.play(FadeIn(names), run_time=0.6)
        bot = fit(txt("HOW THE OS PICKS A HOLE", size=26), max_w=3.3).move_to([0, -1.95, 0])
        self.play(FadeIn(bot), run_time=0.6)
        self.pad_to(TARGETS[0], start)


class Fits2(FitsBase):
    def construct(self):
        start = self.renderer.time
        h = self.header("DYNAMIC PARTITIONING", size=33)
        sub = fit(txt("EVERY FREE BLOCK IS A HOLE", size=23, color=MUTE), max_w=3.3).move_to([0, 2.28, 0])
        self.play(FadeIn(h, shift=UP * 0.12), FadeIn(sub), run_time=0.7)
        cards = self.hole_grid()
        self.wait(3.6)
        self.play(LaggedStart(*[FadeIn(c, scale=0.85) for c in cards], lag_ratio=0.14), run_time=4.6)
        chip = self.chip("NEW PROCESS: 2 MB", y=-0.72)
        self.wait(1.4)
        self.play(FadeIn(chip, shift=UP * 0.12), run_time=0.6)
        q = fit(txt("WHERE DOES IT GO?", size=32, color=GOLD), max_w=3.3).move_to([0, -1.62, 0])
        self.wait(0.9)
        self.play(FadeIn(q), run_time=0.6)
        self.pad_to(TARGETS[1], start)


class Fits3(FitsBase):
    def construct(self):
        start = self.renderer.time
        cards = self.hole_grid()
        h1 = self.header("FIRST-FIT", color=GOLD)
        self.play(FadeIn(h1, shift=UP * 0.12), *[FadeIn(c) for c in cards], run_time=0.6)
        ring = self.ring(cards[0])
        self.wait(0.6)
        self.play(FadeIn(ring), run_time=0.3)                      # at H1 ~1.2s
        self.wait(0.3)
        self.play(ring.animate.set_stroke(SOFT_RED), run_time=0.25)  # too small
        self.wait(0.35)
        self.play(ring.animate.move_to(cards[1][0].get_center()).set_stroke(GOLD), run_time=0.5)
        self.play(Indicate(cards[1], scale_factor=1.07, color=GOLD), run_time=0.5)
        self.pick(cards[1])
        chip1 = self.chip("LEFTOVER 1 MB", y=-0.85)
        self.play(FadeIn(chip1, shift=UP * 0.1), FadeOut(ring), run_time=0.5)
        # --- next-fit ---
        h2 = self.header("NEXT-FIT", color=GOLD)
        self.wait(1.15)
        self.play(Transform(h1, h2), FadeOut(chip1), run_time=0.5)
        self.unpick(cards[1])
        ring2 = self.ring(cards[1])
        tag = fit(txt("RESUME", size=18, color=GOLD), max_w=0.9).move_to([XS[1], YS[0] + 0.72, 0])
        self.play(FadeIn(ring2), FadeIn(tag), run_time=0.4)
        self.wait(0.4)
        self.play(ring2.animate.move_to(cards[2][0].get_center()), FadeOut(tag), run_time=0.45)
        self.play(ring2.animate.set_stroke(SOFT_RED), run_time=0.25)  # H3 too small
        self.wait(0.3)
        self.play(ring2.animate.move_to(cards[3][0].get_center()).set_stroke(GOLD), run_time=0.5)
        self.play(Indicate(cards[3], scale_factor=1.07, color=GOLD), run_time=0.5)
        self.pick(cards[3])
        chip2 = self.chip("LEFTOVER 2 MB", y=-0.85)
        self.play(FadeIn(chip2, shift=UP * 0.1), FadeOut(ring2), run_time=0.5)
        self.pad_to(TARGETS[2], start)


class Fits4(FitsBase):
    def construct(self):
        start = self.renderer.time
        cards = self.hole_grid()
        h = self.header("BEST-FIT", color=GOLD)
        self.play(FadeIn(h, shift=UP * 0.12), *[FadeIn(c) for c in cards], run_time=0.6)
        ring = self.ring(cards[0])
        self.wait(0.55)
        self.play(FadeIn(ring), run_time=0.25)
        for i in range(1, 6):
            self.play(ring.animate.move_to(cards[i][0].get_center()), run_time=0.32)
        self.play(Indicate(cards[5], scale_factor=1.08, color=GOLD), run_time=0.5)
        self.pick(cards[5])
        chip = self.chip("LEFTOVER 0 — PERFECT FIT", y=-0.85)
        self.play(FadeIn(chip, shift=UP * 0.1), FadeOut(ring), run_time=0.5)
        warn = fit(txt("TINY SLIVERS → MOST FRAGMENTATION", size=23, color=SOFT_RED), max_w=3.3)
        warn.move_to([0, -1.72, 0])
        self.wait(2.6)
        self.play(FadeIn(warn), run_time=0.6)
        self.pad_to(TARGETS[3], start)


class Fits5(FitsBase):
    def construct(self):
        start = self.renderer.time
        cards = self.hole_grid()
        h = self.header("WORST-FIT", color=GOLD)
        self.play(FadeIn(h, shift=UP * 0.12), *[FadeIn(c) for c in cards], run_time=0.6)
        ring = self.ring(cards[4])
        self.wait(1.2)
        self.play(FadeIn(ring), run_time=0.3)
        self.play(Indicate(cards[4], scale_factor=1.08, color=GOLD), run_time=0.5)
        self.pick(cards[4])
        chip = self.chip("LEFTOVER 4 MB", y=-0.85)
        self.play(FadeIn(chip, shift=UP * 0.1), FadeOut(ring), run_time=0.5)
        line = fit(txt("BIG LEFTOVER — BIGGEST HOLE BURNED", size=23, color=MUTE), max_w=3.3)
        line.move_to([0, -1.72, 0])
        self.wait(2.2)
        self.play(FadeIn(line), run_time=0.6)
        self.pad_to(TARGETS[4], start)


class Fits6(FitsBase):
    def construct(self):
        start = self.renderer.time
        h = self.header("SAME INPUT. FOUR ANSWERS.", size=30)
        self.play(FadeIn(h, shift=UP * 0.12), run_time=0.7)
        rows = [("FIRST-FIT", "H2 · 3 MB"), ("NEXT-FIT", "H4 · 4 MB"),
                ("BEST-FIT", "H6 · 2 MB"), ("WORST-FIT", "H5 · 6 MB")]
        groups = []
        for i, (name, hole) in enumerate(rows):
            y = 1.92 - i * 0.66
            n = txt(name, size=23)
            n.move_to([-1.65 + n.width / 2, y, 0])
            a = txt("→", size=23, color=MUTE).move_to([0.32, y, 0])
            hv = txt(hole, size=23, color=GOLD)
            hv.move_to([0.62 + hv.width / 2, y, 0])
            groups.append(VGroup(n, a, hv))
        self.wait(0.7)
        self.play(LaggedStart(*[FadeIn(g, shift=RIGHT * 0.15) for g in groups], lag_ratio=0.22), run_time=3.4)
        verdict = self.chip("FASTEST + BALANCED: FIRST & NEXT", y=-0.92, color=GOLD)
        self.wait(1.6)
        self.play(FadeIn(verdict, shift=UP * 0.1), run_time=0.6)
        close = fit(txt("GOOD ONE, FAST.", size=34), max_w=3.3).move_to([0, -1.92, 0])
        self.wait(2.2)
        self.play(FadeIn(close), run_time=0.6)
        self.pad_to(TARGETS[5], start)
