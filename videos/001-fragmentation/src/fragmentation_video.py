from manim import *

config.background_color = "#070718"
config.pixel_width = 1080
config.pixel_height = 1920
config.frame_width = 4.5
config.frame_height = 8.0
config.frame_rate = 30

BLUE_C = "#58C4DD"
PROG_FILL = "#274b73"
GOLD_C = "#FFC94D"
GREEN_C = "#83C167"
RED_C = "#FC6255"
GREY_C = "#888888"
HOLE_FILL = "#2a2a35"
MAX_W = 4.3
KB = 0.042  # scene units per KB for the 100 KB strip (total 4.2 wide)
STRIP_Y = 0.9


def fit(mob, max_w=MAX_W):
    if mob.width > max_w:
        mob.scale_to_fit_width(max_w)
    return mob


class SegBase(Scene):
    def begin(self):
        self.elapsed = 0.0

    def do(self, dur, *anims):
        self.play(*anims, run_time=dur)
        self.elapsed += dur

    def pause(self, dur):
        if dur > 0.01:
            self.wait(dur)
            self.elapsed += dur

    def pad_to(self, total):
        self.pause(total - self.elapsed)

    def line(self, text, y, size=29, color=WHITE, bold=False, max_w=MAX_W):
        t = Text(text, font_size=size, weight=BOLD if bold else NORMAL, color=color)
        t.move_to(UP * y)
        fit(t, max_w=max_w)
        return t

    def header(self, text, y=3.45, color=WHITE, size=35):
        return self.line(text, y, size=size, color=color, bold=True, max_w=4.15)

    # Memory strip from [(label, kb, kind)] kind in {"prog", "hole"}
    def make_strip(self, segments, y=STRIP_Y, height=1.1):
        group = VGroup()
        self.strip_parts = {}
        x = -sum(kb for _, kb, _ in segments) * KB / 2
        for label, kb, kind in segments:
            w = kb * KB
            fill = PROG_FILL if kind == "prog" else HOLE_FILL
            stroke = BLUE_C if kind == "prog" else GREY_C
            rect = Rectangle(width=w, height=height, stroke_color=stroke, stroke_width=2.5,
                             fill_color=fill, fill_opacity=1)
            rect.move_to([x + w / 2, y, 0])
            lab = Text(label, font_size=18, weight=BOLD, color=WHITE if kind == "prog" else GREY_C)
            fit(lab, max_w=w - 0.06)
            lab.move_to(rect.get_center())
            part = VGroup(rect, lab)
            group.add(part)
            self.strip_parts[label] = part
            x += w
        return group

    def size_label(self, part, text, color=GREY_C, y_off=0.45):
        lab = Text(text, font_size=16, color=color)
        c = part.get_center()
        lab.move_to([c[0], STRIP_Y - 0.55 - y_off + 0.45, 0])
        return lab


EXT_SEGMENTS = [("P1", 20, "prog"), ("", 10, "hole"), ("P2", 25, "prog"),
                ("", 15, "hole"), ("P3", 10, "prog"), ("", 20, "hole")]


# ============================================================
# SEG 1 — 7.16s. Hook: full and free at the same time.
# ============================================================
class Frag1(SegBase):
    def construct(self):
        self.begin()
        big = VGroup(
            Text("Full AND free", font_size=44, weight=BOLD, color=WHITE),
            Text("at the same time?", font_size=44, weight=BOLD, color=GOLD_C),
        ).arrange(DOWN, buff=0.18)
        big.move_to(UP * 3.0)
        fit(big)
        self.do(1.0, Write(big))

        strip = self.make_strip([("USED", 50, "prog"), ("FREE", 50, "hole")], y=1.15, height=1.15)
        self.do(0.9, FadeIn(strip, shift=UP * 0.2))
        self.pause(1.4)

        title = self.header("FRAGMENTATION", y=-0.6, color=GOLD_C, size=38)
        self.do(1.1, Write(title))
        sub = self.line("...and it comes in two kinds", -1.35, size=26, color=GREY_C)
        self.do(0.6, FadeIn(sub))

        chip1 = self.line("1. INTERNAL", -2.3, size=28, color=BLUE_C, bold=True)
        chip2 = self.line("2. EXTERNAL", -3.0, size=28, color=BLUE_C, bold=True)
        self.do(0.7, FadeIn(chip1), FadeIn(chip2))
        self.pad_to(7.16)


# ============================================================
# SEG 2 — 16.85s. Internal: 64 KB block, 40 used, 24 trapped.
# ============================================================
class Frag2(SegBase):
    def construct(self):
        self.begin()
        head = self.header("INTERNAL FRAGMENTATION", color=BLUE_C, size=32)
        self.do(1.2, Write(head))
        defn = self.line("waste INSIDE a block", 2.8, size=27, color=WHITE)
        self.do(0.7, FadeIn(defn))
        self.pause(1.6)

        # Block: 64 KB wide = 4.1 units, program 40 KB = 2.5625, waste 24 KB = 1.5375
        block_w, prog_w = 4.1, 4.1 * 40 / 64
        waste_w = block_w - prog_w
        block = Rectangle(width=block_w, height=1.35, stroke_color=WHITE, stroke_width=3)
        block.move_to(UP * 1.15)
        self.do(1.0, Create(block))
        blab = self.line("one block = 64 KB", 0.18, size=24, color=GREY_C)
        self.do(0.5, FadeIn(blab))
        self.pause(2.0)

        prog = Rectangle(width=prog_w, height=1.35, stroke_color=BLUE_C, stroke_width=2,
                         fill_color=PROG_FILL, fill_opacity=1)
        prog.move_to([block.get_left()[0] + prog_w / 2, 1.15, 0])
        plab = Text("program: 40 KB", font_size=21, weight=BOLD, color=WHITE)
        fit(plab, max_w=prog_w - 0.1)
        plab.move_to(prog.get_center())
        self.do(1.2, FadeIn(prog), FadeIn(plab))
        self.pause(2.8)

        waste = Rectangle(width=waste_w, height=1.35, stroke_color=RED_C, stroke_width=2,
                          fill_color=RED_C, fill_opacity=0.55)
        waste.move_to([block.get_right()[0] - waste_w / 2, 1.15, 0])
        wlab = Text("24 KB", font_size=21, weight=BOLD, color=WHITE)
        fit(wlab, max_w=waste_w - 0.08)
        wlab.move_to(waste.get_center())
        self.do(1.0, FadeIn(waste), FadeIn(wlab))

        wasted = self.line("24 KB wasted — trapped inside", -0.85, size=28, color=RED_C, bold=True)
        self.do(0.8, Write(wasted))
        note = self.line("nobody else can use it", -1.6, size=25, color=GREY_C)
        self.do(0.7, FadeIn(note))
        self.do(1.2, Indicate(waste, scale_factor=1.05, color=RED_C))
        self.pad_to(16.85)


# ============================================================
# SEG 3 — 11.54s. External: holes 10 / 15 / 20 appear.
# ============================================================
class Frag3(SegBase):
    def construct(self):
        self.begin()
        head = self.header("EXTERNAL FRAGMENTATION", color=BLUE_C, size=32)
        self.do(1.2, Write(head))
        defn = self.line("waste BETWEEN blocks", 2.8, size=27, color=WHITE)
        self.do(0.7, FadeIn(defn))

        strip = self.make_strip(EXT_SEGMENTS)
        self.do(1.4, LaggedStart(*[FadeIn(p, shift=UP * 0.2) for p in strip], lag_ratio=0.12))

        ghost = self.line("programs load... and exit", -0.35, size=25, color=GREY_C)
        self.do(0.8, FadeIn(ghost))
        self.do(0.9, FadeOut(ghost))

        holes = [p for (lab, kb, kind), p in zip(EXT_SEGMENTS, strip) if kind == "hole"]
        sizes = ["10 KB", "15 KB", "20 KB"]
        for hole, s in zip(holes, sizes):
            lab = Text(s, font_size=19, weight=BOLD, color=GOLD_C)
            lab.next_to(hole, DOWN, buff=0.14)
            self.do(1.1, Indicate(hole, scale_factor=1.12, color=GOLD_C), FadeIn(lab))
        self.pad_to(11.54)


# ============================================================
# SEG 4 — 11.94s. 45 KB free, 30 KB program can't load.
# ============================================================
class Frag4(SegBase):
    def construct(self):
        self.begin()
        head = self.header("EXTERNAL FRAGMENTATION", color=BLUE_C, size=32)
        strip = self.make_strip(EXT_SEGMENTS)
        self.add(head, strip)
        for (lab, kb, kind), part in zip(EXT_SEGMENTS, strip):
            if kind == "hole":
                t = Text(f"{kb} KB", font_size=19, weight=BOLD, color=GOLD_C)
                t.next_to(part, DOWN, buff=0.14)
                self.add(t)

        sumline = self.line("10 + 15 + 20 = 45 KB free", 2.55, size=29, color=WHITE, bold=True)
        self.do(1.3, Write(sumline))
        self.pause(0.9)

        gold = Rectangle(width=30 * KB, height=0.85, stroke_color=GOLD_C, stroke_width=3,
                         fill_color=GOLD_C, fill_opacity=0.85)
        gold.move_to(DOWN * 1.15)
        glab = Text("NEW: 30 KB", font_size=20, weight=BOLD, color=BLACK)
        fit(glab, max_w=30 * KB - 0.08)
        glab.move_to(gold.get_center())
        goldgrp = VGroup(gold, glab)
        self.do(0.8, FadeIn(goldgrp, shift=UP * 0.2))
        need = self.line("needs 30 KB in ONE piece", -2.15, size=25, color=GOLD_C)
        self.do(0.6, FadeIn(need))
        self.pause(1.6)

        holes = [p for (lab, kb, kind), p in zip(EXT_SEGMENTS, strip) if kind == "hole"]
        for hole in holes:
            x_mark = Text("X", font_size=30, weight=BOLD, color=RED_C)
            x_mark.move_to(hole.get_center() + UP * 0.02)
            target_pos = hole.get_center() + UP * 1.05
            self.do(0.9, goldgrp.animate.move_to(target_pos), FadeIn(x_mark))

        self.do(0.5, goldgrp.animate.move_to(DOWN * 1.15).set_opacity(0.45))
        cant = self.line("CAN'T LOAD", -2.95, size=36, color=RED_C, bold=True)
        self.do(1.0, Write(cant))
        sub = self.line("...with 45 KB still free", -3.6, size=24, color=GREY_C)
        self.do(0.7, FadeIn(sub))
        self.pad_to(11.94)


# ============================================================
# SEG 5 — 13.18s. Fixes: compaction + paging.
# ============================================================
class Frag5(SegBase):
    def construct(self):
        self.begin()
        head = self.header("TWO FIXES", color=GOLD_C, size=36)
        self.do(0.7, Write(head))

        fix1 = self.line("Fix 1: COMPACTION", 2.75, size=27, color=BLUE_C, bold=True)
        self.do(0.6, FadeIn(fix1))
        strip = self.make_strip(EXT_SEGMENTS, y=1.85, height=0.95)
        self.do(0.8, FadeIn(strip))

        # Compact: P2 slides next to P1, P3 next to P2, holes merge at right
        p1 = self.strip_parts["P1"]; p2 = self.strip_parts["P2"]; p3 = self.strip_parts["P3"]
        holes = [p for (lab, kb, kind), p in zip(EXT_SEGMENTS, strip) if kind == "hole"]
        left = strip.get_left()[0]
        p2_new = [left + (20 + 25 / 2) * KB, 1.85, 0]
        p3_new = [left + (20 + 25 + 10 / 2) * KB, 1.85, 0]
        merged = Rectangle(width=45 * KB, height=0.95, stroke_color=GREY_C, stroke_width=2.5,
                           fill_color=HOLE_FILL, fill_opacity=1)
        merged.move_to([left + (55 + 45 / 2) * KB, 1.85, 0])
        mlab = Text("one hole: 45 KB", font_size=19, weight=BOLD, color=GOLD_C)
        fit(mlab, max_w=1.8)
        mlab.move_to([merged.get_center()[0], 1.02, 0])
        self.do(1.6, p2.animate.move_to(p2_new), p3.animate.move_to(p3_new),
                *[FadeOut(h) for h in holes])
        self.do(0.6, FadeIn(merged), FadeIn(mlab))

        gold = Rectangle(width=30 * KB, height=0.7, stroke_color=GOLD_C, stroke_width=2.5,
                         fill_color=GOLD_C, fill_opacity=0.85)
        gold.move_to([merged.get_center()[0] - (45 - 30) * KB / 2, 1.85, 0])
        self.do(0.8, FadeIn(gold, shift=DOWN * 0.3))
        fits = self.line("30 KB fits now", 0.45, size=24, color=GREEN_C, bold=True)
        self.do(0.5, FadeIn(fits))
        self.pause(0.4)

        fix2 = self.line("Fix 2: PAGING", -0.35, size=27, color=BLUE_C, bold=True)
        self.do(0.6, FadeIn(fix2))

        # Frame grid: 5 cols x 4 rows
        grid = VGroup()
        frames = []
        for r in range(4):
            for c in range(5):
                sq = Square(side_length=0.52, stroke_color=GREY_C, stroke_width=2,
                            fill_color=HOLE_FILL, fill_opacity=1)
                sq.move_to([(c - 2) * 0.62, -1.35 - r * 0.62, 0])
                grid.add(sq)
                frames.append(sq)
        self.do(1.4, LaggedStart(*[FadeIn(s) for s in grid], lag_ratio=0.03))
        used_idx = [1, 4, 6, 9, 12, 15, 18]
        self.do(1.2, *[frames[i].animate.set_fill(PROG_FILL, opacity=1).set_stroke(color=BLUE_C) for i in used_idx])
        anylab = self.line("one program, scattered frames — all usable", -3.78, size=20, color=GREEN_C, max_w=4.0)
        self.do(0.7, FadeIn(anylab))
        self.do(1.2, Indicate(VGroup(*[frames[i] for i in used_idx]), scale_factor=1.03, color=BLUE_C))
        self.pad_to(13.18)


# ============================================================
# SEG 6 — 13.12s. Paging tradeoff + closing line.
# ============================================================
class Frag6(SegBase):
    def construct(self):
        self.begin()
        head = self.header("PAGING'S TRADEOFF", color=GOLD_C, size=34)
        self.do(1.0, Write(head))
        sub = self.line("a 30 KB program in 4 KB pages:", 2.75, size=25, color=GREY_C)
        self.do(0.6, FadeIn(sub))

        pages = VGroup()
        rects = []
        for i in range(8):
            r = Rectangle(width=0.48, height=0.95, stroke_color=WHITE, stroke_width=2,
                          fill_color="#1a1a24", fill_opacity=1)
            r.move_to([(i - 3.5) * 0.545, 1.55, 0])
            num = Text(str(i + 1), font_size=17, color=GREY_C)
            num.next_to(r, DOWN, buff=0.09)
            pages.add(VGroup(r, num))
            rects.append(r)
        self.do(1.2, LaggedStart(*[FadeIn(p, shift=UP * 0.2) for p in pages], lag_ratio=0.08))
        self.pause(0.4)

        fills = []
        for i in range(7):
            fills.append(rects[i].animate.set_fill(PROG_FILL, opacity=1).set_stroke(color=BLUE_C))
        self.do(1.6, LaggedStart(*fills, lag_ratio=0.12))

        half = Rectangle(width=0.24, height=0.95, stroke_width=0,
                         fill_color=PROG_FILL, fill_opacity=1)
        half.move_to([rects[7].get_left()[0] + 0.12, 1.55, 0])
        waste = Rectangle(width=0.24, height=0.95, stroke_color=RED_C, stroke_width=1.5,
                          fill_color=RED_C, fill_opacity=0.55)
        waste.move_to([rects[7].get_right()[0] - 0.12, 1.55, 0])
        self.do(0.7, FadeIn(half), FadeIn(waste))
        wlab = self.line("last page: 2 KB used, 2 KB wasted", 0.15, size=24, color=RED_C, bold=True)
        self.do(0.8, FadeIn(wlab))
        self.pause(2.2)

        line1 = self.line("You don't eliminate fragmentation.", -1.15, size=27, color=WHITE)
        self.do(1.1, Write(line1))
        line2 = self.line("You choose where it lives.", -1.95, size=30, color=GOLD_C, bold=True)
        self.do(1.1, Write(line2))
        endcard = self.line("logicanimated", -3.55, size=20, color=GREY_C)
        self.do(0.6, FadeIn(endcard))
        self.pad_to(13.12)
