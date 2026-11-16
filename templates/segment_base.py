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


# Usage: subclass SegBase (or a project base extending it), one Scene per
# narration segment. In construct(): self.begin(), animate with self.do(dur, ...)
# and self.pause(dur) so every second is accounted for, then self.pad_to(SEG_TOTAL)
# where SEG_TOTAL = measured Kokoro segment duration + 0.4s pause (last segment:
# audio duration only). Render each scene separately, verify durations with
# ffprobe, concat in order, mux the combined narration.wav.
