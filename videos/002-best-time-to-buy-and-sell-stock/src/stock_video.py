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


# ---------------- Stock-video specifics (SAFE-ZONE layout) ----------------
# Critical content box: x in [-1.7, 1.7], y in [-2.3, 3.2] (see SAFE_ZONES.md).
PRICES = [7, 1, 5, 3, 6, 4]
CHART_BASE = -0.75
CHART_SCALE = 0.40
BAR_XS = [-1.50, -0.90, -0.30, 0.30, 0.90, 1.50]


class StockBase(SegBase):
    def hdr(self, text, color=GOLD, size=32):
        return self.line(text, 2.98, size=size, color=color, bold=True, max_w=3.4)

    def make_chart(self, fills=None, borders=None):
        """Bars + price labels + day labels + baseline, all in the safe box."""
        fills = fills or {}
        borders = borders or {}
        g = VGroup()
        base = Rectangle(width=3.44, height=0.03, fill_color=GRAY,
                         fill_opacity=0.9, stroke_width=0)
        base.move_to([0, CHART_BASE, 0])
        g.add(base)
        self._bars = []
        for i, p in enumerate(PRICES):
            h = p * CHART_SCALE
            bar = Rectangle(width=0.40, height=h,
                            fill_color=fills.get(i, PROG_FILL), fill_opacity=0.95,
                            stroke_color=borders.get(i, WHITE), stroke_width=2)
            bar.move_to([BAR_XS[i], CHART_BASE + h / 2, 0])
            lab = fit(Text(str(p), font_size=25, color=WHITE, weight=BOLD),
                           0.34)
            lab.move_to([BAR_XS[i], CHART_BASE + h + 0.24, 0])
            day = fit(Text(f"D{i+1}", font_size=19, color=GRAY), 0.36)
            day.move_to([BAR_XS[i], CHART_BASE - 0.32, 0])
            self._bars.append(VGroup(bar, lab))
            g.add(self._bars[-1], day)
        return g

    def tracker_cards(self, cheapest="—", best="—", y=-1.80):
        def card(cx, label, value, color):
            box = RoundedRectangle(corner_radius=0.09, width=1.62, height=0.78,
                                   stroke_color=color, stroke_width=2.5,
                                   fill_color=BLACK, fill_opacity=0.55)
            box.move_to([cx, y, 0])
            lab = fit(Text(label, font_size=16, color=color, weight=BOLD), 1.5)
            lab.move_to([cx, y + 0.20, 0])
            val = fit(Text(str(value), font_size=33, color=WHITE, weight=BOLD), 0.9)
            val.move_to([cx, y - 0.17, 0])
            return VGroup(box, lab, val), val
        lc, lv = card(-0.86, "CHEAPEST SO FAR", cheapest, BLUE)
        rc, rv = card(0.86, "BEST PROFIT", best, GOLD)
        self._cheap_val, self._best_val = lv, rv
        return VGroup(lc, rc)

    def set_tracker(self, which, new_value, dur=0.5):
        old = self._cheap_val if which == "cheap" else self._best_val
        new = fit(Text(str(new_value), font_size=33, color=WHITE, weight=BOLD), 0.9)
        new.move_to(old.get_center())
        if which == "cheap":
            self._cheap_val = new
        else:
            self._best_val = new
        self.do(dur, FadeOut(old, shift=DOWN * 0.08), FadeIn(new, shift=UP * 0.08))

    def chip(self, text, cx, cy, color, w=1.58, size=19):
        box = RoundedRectangle(corner_radius=0.10, width=w, height=0.52,
                               stroke_color=color, stroke_width=2.5,
                               fill_color=BLACK, fill_opacity=0.6)
        box.move_to([cx, cy, 0])
        t = fit(Text(text, font_size=size, color=color, weight=BOLD), w - 0.16)
        t.move_to([cx, cy, 0])
        return VGroup(box, t)


class Stock1(StockBase):
    SEG = 13.09

    def construct(self):
        self.begin()
        h = self.hdr("LEETCODE 121")
        t1 = self.line("Best Time to Buy", 2.38, size=35, bold=True, max_w=3.4)
        t2 = self.line("and Sell Stock", 1.90, size=35, bold=True, max_w=3.4)
        self.do(1.4, FadeIn(h, shift=DOWN * 0.15), FadeIn(t1, shift=UP * 0.12),
                FadeIn(t2, shift=UP * 0.12))
        c1 = self.chip("BUY ONCE", -0.86, 1.15, BLUE)
        c2 = self.chip("SELL LATER", 0.86, 1.15, GOLD)
        self.do(2.6, FadeIn(c1, shift=UP * 0.12), FadeIn(c2, shift=UP * 0.12))
        q = self.line("check every pair of days?", 0.25, size=23, color=GRAY, max_w=3.4)
        self.do(3.2, FadeIn(q))
        ok = self.line("it works...",  -0.35, size=24, max_w=3.4)
        slow = self.line("but FAR TOO SLOW", -0.95, size=29, color=RED, bold=True, max_w=3.4)
        self.do(2.8, FadeIn(ok))
        self.do(2.2, FadeIn(slow, shift=UP * 0.1))
        self.pad_to(self.SEG)


class Stock2(StockBase):
    SEG = 11.90

    def construct(self):
        self.begin()
        h = self.hdr("SIX DAYS OF PRICES", size=29)
        arr = self.line("[7, 1, 5, 3, 6, 4]", 2.42, size=27, color=BLUE, bold=True, max_w=3.4)
        self.do(1.6, FadeIn(h, shift=DOWN * 0.15), FadeIn(arr))
        chart = self.make_chart()
        bars = [self._bars[i] for i in range(6)]
        rest = [m for m in chart.submobjects if m not in bars]
        self.do(0.8, *[FadeIn(m) for m in rest])
        for b in bars:
            self.do(0.62, GrowFromEdge(b[0], DOWN), FadeIn(b[1]))
        cap = self.line("ONE PASS · TWO NUMBERS", -1.80, size=23, color=GOLD, bold=True, max_w=3.4)
        self.do(2.2, FadeIn(cap, shift=UP * 0.1))
        self.pad_to(self.SEG)


class Stock3(StockBase):
    SEG = 13.29

    def construct(self):
        self.begin()
        h = self.hdr("TRACK TWO NUMBERS", size=29)
        self.do(1.2, FadeIn(h, shift=DOWN * 0.15))

        def big_card(cx, label, sub, color):
            box = RoundedRectangle(corner_radius=0.10, width=1.62, height=1.55,
                                   stroke_color=color, stroke_width=3,
                                   fill_color=BLACK, fill_opacity=0.55)
            box.move_to([cx, 1.55, 0])
            l1 = fit(Text(label, font_size=19, color=color, weight=BOLD), 1.5)
            l1.move_to([cx, 1.98, 0])
            l2 = fit(Text(sub, font_size=16, color=WHITE), 1.48)
            l2.move_to([cx, 1.62, 0])
            num = fit(Text("1" if color == BLUE else "2", font_size=30,
                                color=color, weight=BOLD), 0.5)
            num.move_to([cx, 1.12, 0])
            return VGroup(box, l1, l2, num)

        c1 = big_card(-0.86, "CHEAPEST", "best buy so far", BLUE)
        c2 = big_card(0.86, "BEST PROFIT", "best result so far", GOLD)
        self.do(3.4, FadeIn(c1, shift=UP * 0.15))
        self.do(3.4, FadeIn(c2, shift=UP * 0.15))
        qbox = RoundedRectangle(corner_radius=0.10, width=3.40, height=0.95,
                                stroke_color=WHITE, stroke_width=2.5,
                                fill_color=BLACK, fill_opacity=0.5)
        qbox.move_to([0, -0.55, 0])
        q1 = self.line("IF I SOLD TODAY,", -0.38, size=25, bold=True, max_w=3.3)
        q2 = self.line("WHAT WOULD I MAKE?", -0.78, size=25, bold=True, max_w=3.3)
        self.do(2.6, FadeIn(qbox), FadeIn(q1), FadeIn(q2))
        note = self.line("ask it every single day", -1.95, size=20, color=GRAY, max_w=3.4)
        self.do(1.6, FadeIn(note))
        self.pad_to(self.SEG)


class Stock4(StockBase):
    SEG = 14.14

    def construct(self):
        self.begin()
        h = self.hdr("DAYS 1 TO 3", size=30)
        chart = self.make_chart()
        cards = self.tracker_cards("—", "—")
        self.do(1.3, FadeIn(h, shift=DOWN * 0.15), FadeIn(chart), FadeIn(cards))
        ring = SurroundingRectangle(self._bars[0], color=GOLD, buff=0.06, stroke_width=4)
        self.do(1.2, Create(ring))
        self.set_tracker("cheap", "7", 0.6)
        self.set_tracker("best", "0", 0.6)
        self.pause(1.2)
        ring2 = SurroundingRectangle(self._bars[1], color=GOLD, buff=0.06, stroke_width=4)
        self.do(1.2, Transform(ring, ring2))
        self.set_tracker("cheap", "1", 0.7)
        self.pause(1.3)
        ring3 = SurroundingRectangle(self._bars[2], color=GOLD, buff=0.06, stroke_width=4)
        self.do(1.2, Transform(ring, ring3))
        call = self.line("5 − 1 = 4", 2.42, size=31, color=GOLD, bold=True, max_w=3.4)
        self.do(1.1, FadeIn(call, scale=1.25))
        self.set_tracker("best", "4", 0.7)
        self.pad_to(self.SEG)


class Stock5(StockBase):
    SEG = 12.45

    def construct(self):
        self.begin()
        h = self.hdr("DAYS 4 TO 6", size=30)
        chart = self.make_chart(fills={1: BLUE, 4: GOLD})
        cards = self.tracker_cards("1", "4")
        self.do(1.2, FadeIn(h, shift=DOWN * 0.15), FadeIn(chart), FadeIn(cards))
        ring = SurroundingRectangle(self._bars[3], color=WHITE, buff=0.06, stroke_width=4)
        self.do(1.1, Create(ring))
        c1 = self.line("3 − 1 = 2", 2.42, size=25, color=GRAY, max_w=3.4)
        self.do(1.3, FadeIn(c1))
        self.pause(0.9)
        ring2 = SurroundingRectangle(self._bars[4], color=GOLD, buff=0.06, stroke_width=5)
        self.do(1.1, Transform(ring, ring2), FadeOut(c1))
        c2 = self.line("6 − 1 = 5", 2.42, size=33, color=GOLD, bold=True, max_w=3.4)
        self.do(1.1, FadeIn(c2, scale=1.3))
        self.set_tracker("best", "5", 0.7)
        ring3 = SurroundingRectangle(self._bars[5], color=WHITE, buff=0.06, stroke_width=4)
        self.do(1.0, Transform(ring, ring3))
        c3 = self.line("4 − 1 = 3", 2.42, size=25, color=GRAY, max_w=3.4)
        self.do(1.2, FadeOut(c2), FadeIn(c3))
        badge = self.chip("ANSWER: 5", 0, 2.42, GOLD, w=2.2, size=27)
        buy = fit(Text("BUY", font_size=15, color=BLUE, weight=BOLD), 0.5)
        buy.move_to([BAR_XS[1], -1.26, 0])
        sell = fit(Text("SELL", font_size=15, color=GOLD, weight=BOLD), 0.55)
        sell.move_to([BAR_XS[4], -1.26, 0])
        self.do(1.3, FadeOut(c3), FadeIn(badge, scale=1.2), FadeIn(buy), FadeIn(sell))
        self.pad_to(self.SEG)


class Stock6(StockBase):
    SEG = 11.39

    def construct(self):
        self.begin()
        h = self.hdr("THE SOLUTION", size=30)
        self.do(1.0, FadeIn(h, shift=DOWN * 0.15))
        code = [
            ("def maxProfit(prices):", 0),
            ("cheapest = prices[0]", 1),
            ("best = 0", 1),
            ("for p in prices:", 1),
            ("cheapest = min(cheapest, p)", 2),
            ("best = max(best, p - cheapest)", 2),
            ("return best", 1),
        ]
        y = 2.30
        objs = []
        for text, indent in code:
            t = Text(text, font_size=21, color=WHITE, font="Monospace")
            fit(t, 3.35 - indent * 0.22)
            t.move_to([-1.68 + indent * 0.22 + t.width / 2, y, 0])
            objs.append(t)
            y -= 0.44
        for t in objs:
            self.do(0.62, FadeIn(t, shift=RIGHT * 0.08))
        c1 = self.chip("TIME  O(n)", -0.86, -1.52, BLUE)
        c2 = self.chip("SPACE  O(1)", 0.86, -1.52, GOLD)
        self.do(1.4, FadeIn(c1, shift=UP * 0.1), FadeIn(c2, shift=UP * 0.1))
        end = self.line("logicanimated", -2.08, size=21, color=GOLD, bold=True, max_w=3.4)
        self.do(1.2, FadeIn(end))
        self.pad_to(self.SEG)
