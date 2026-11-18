#!/usr/bin/env python3
"""Render the front page that sums up 18 November 2026, as a 1024x1024 PNG.

The drawing runs here, on this machine, with Pillow. The shipped entry
program (main.py) only copies the finished picture, so the graded run is
deterministic and needs no network. Nothing here is random and no clock
value is baked into the picture.
"""
from __future__ import annotations

import math
import os

from PIL import Image, ImageDraw, ImageFont

SIDE = 1024
EDGE = 24

PALETTE = {
    "paper": (246, 241, 229),
    "ink": (18, 18, 18),
    "scarlet": (178, 34, 34),
    "navy": (23, 42, 74),
    "ocean": (28, 68, 110),
    "lagoon": (16, 96, 110),
    "muted": (60, 60, 60),
    "panel": (232, 226, 210),
    "sky": (214, 226, 238),
    "gold": (200, 160, 60),
}

FONT_FILES = {
    "serif": "/usr/share/fonts/truetype/noto/NotoSerif-Bold.ttf",
    "serif_heavy": "/usr/share/fonts/truetype/noto/NotoSerif-Black.ttf",
    "sans": "/usr/share/fonts/truetype/noto/NotoSans-Regular.ttf",
    "sans_bold": "/usr/share/fonts/truetype/noto/NotoSans-Bold.ttf",
    "sans_heavy": "/usr/share/fonts/truetype/noto/NotoSans-Black.ttf",
}

_cache: dict = {}


def typeface(kind: str, size: int):
    """Load (once) and return a TrueType font of the requested kind/size."""
    key = (kind, size)
    if key not in _cache:
        _cache[key] = ImageFont.truetype(FONT_FILES[kind], size)
    return _cache[key]


def split_lines(pen, text: str, face, width: int) -> list:
    """Break text into lines that fit `width` pixels, word by word."""
    out, current = [], ""
    for word in text.split():
        candidate = f"{current} {word}".strip()
        if pen.textlength(candidate, font=face) <= width or not current:
            current = candidate
        else:
            out.append(current)
            current = word
    if current:
        out.append(current)
    return out


class Sheet:
    """A 1024x1024 newspaper sheet with small drawing helpers."""

    def __init__(self):
        self.image = Image.new("RGB", (SIDE, SIDE), PALETTE["paper"])
        self.pen = ImageDraw.Draw(self.image)

    def hline(self, left: int, right: int, y: int, colour, thick: int = 2):
        self.pen.line([(left, y), (right, y)], fill=colour, width=thick)

    def box(self, area, colour=None, outline=None, thick: int = 3):
        self.pen.rectangle(area, fill=colour, outline=outline, width=thick)

    def paragraph(self, x: int, y: int, text: str, kind: str, size: int,
                  width: int, colour=None, gap: float = 1.18) -> int:
        """Draw wrapped text; return the y just below the last line."""
        face = typeface(kind, size)
        ink = PALETTE["ink"] if colour is None else colour
        for line in split_lines(self.pen, text, face, width):
            self.pen.text((x, y), line, font=face, fill=ink)
            y += int(size * gap)
        return y

    def centred(self, x: int, y: int, text: str, kind: str, size: int,
                colour=None):
        face = typeface(kind, size)
        ink = PALETTE["ink"] if colour is None else colour
        self.pen.text((x, y), text, font=face, fill=ink, anchor="ma")

    def right(self, x: int, y: int, text: str, kind: str, size: int,
              colour=None):
        face = typeface(kind, size)
        ink = PALETTE["ink"] if colour is None else colour
        self.pen.text((x, y), text, font=face, fill=ink, anchor="ra")

    def save(self, path: str):
        self.image.save(path, format="PNG", optimize=True)
        print("wrote", path, os.path.getsize(path), "bytes")


def burst(pen, cx: int, cy: int, radius: int):
    """A starburst: 12 long spikes and a hot yellow core."""
    points = []
    for step in range(24):
        theta = math.tau * step / 24
        reach = radius if step % 2 == 0 else radius * 0.45
        points.append((cx + reach * math.cos(theta),
                       cy + reach * math.sin(theta)))
    pen.polygon(points, fill=(232, 120, 30))
    core = radius * 0.45
    pen.ellipse([cx - core, cy - core, cx + core, cy + core],
                fill=(250, 200, 60))


def puff(pen, cx: int, cy: int, shade=(120, 120, 118)):
    """A small cloud of smoke made of five overlapping discs."""
    for dx, dy, r in ((-34, 6, 26), (0, -12, 32), (34, 4, 26),
                      (-8, -30, 24), (22, -26, 20)):
        pen.ellipse([cx + dx - r, cy + dy - r, cx + dx + r, cy + dy + r],
                    fill=shade)


def tongue(pen, cx: int, base: int, half_w: int, tall: int):
    """A flame: an orange triangle with a smaller yellow one inside."""
    pen.polygon([(cx - half_w, base), (cx + half_w, base),
                 (cx, base - tall)], fill=(232, 110, 20))
    pen.polygon([(cx - half_w * 0.55, base), (cx + half_w * 0.55, base),
                 (cx, base - tall * 0.62)], fill=(250, 200, 60))


def paint_bridge(pen, area):
    """The Kerch Bridge: a deck whose middle span has fallen into the sea."""
    x0, y0, x1, y1 = area
    pen.rectangle(area, fill=PALETTE["sky"])
    pen.rectangle([x0, y0, x1, y0 + 26], fill=(250, 214, 130))
    pen.ellipse([x0 + 26, y0 + 8, x0 + 78, y0 + 60], fill=(250, 190, 80))
    water = y0 + int((y1 - y0) * 0.62)
    pen.rectangle([x0, water, x1, y1], fill=PALETTE["ocean"])
    for row in range(5):
        yy = water + 14 + row * 16
        pen.line([(x0 + 12 + row * 30, yy), (x1 - 12 - row * 22, yy)],
                 fill=(120, 170, 205), width=3)
    deck = water - 34
    middle = (x0 + x1) // 2
    for post in (x0 + 70, x1 - 70):
        pen.rectangle([post - 7, deck - 96, post + 7, deck], fill=(70, 70, 72))
        pen.line([(post, deck - 96), (max(x0, post - 90), deck)],
                 fill=(120, 120, 122), width=2)
        pen.line([(post, deck - 96), (min(x1, post + 90), deck)],
                 fill=(120, 120, 122), width=2)
    pen.rectangle([x0, deck, middle - 58, deck + 12], fill=(52, 52, 54))
    pen.rectangle([middle + 58, deck, x1, deck + 12], fill=(52, 52, 54))
    pen.polygon([(middle - 52, deck + 4), (middle + 46, deck + 30),
                 (middle + 40, deck + 44), (middle - 58, deck + 18)],
                fill=(52, 52, 54))
    burst(pen, middle, deck - 6, 46)
    puff(pen, middle - 8, deck - 66)
    puff(pen, middle + 40, deck - 52, shade=(140, 140, 138))


def paint_flag(pen, area, kind: str):
    """One small flag inside `area`; `kind` picks the design."""
    fx, fy, fw, fh = area[0], area[1], area[2] - area[0], area[3] - area[1]
    pen.rectangle(area, outline=PALETTE["ink"], width=2)
    if kind == "usa":
        for stripe in range(7):
            top = fy + stripe * 7
            colour = (178, 34, 34) if stripe % 2 == 0 else (250, 250, 250)
            pen.rectangle([fx, top, fx + fw, top + 7], fill=colour)
        pen.rectangle([fx, fy, fx + 30, fy + 24], fill=(30, 50, 110))
        for sx in (6, 16, 26):
            for sy in (5, 13):
                pen.ellipse([fx + sx - 2, fy + sy - 2, fx + sx + 2,
                             fy + sy + 2], fill=(250, 250, 250))
    elif kind == "jpn":
        pen.rectangle(area, fill=(250, 250, 250))
        pen.ellipse([fx + fw // 2 - 13, fy + fh // 2 - 13,
                     fx + fw // 2 + 13, fy + fh // 2 + 13], fill=(188, 0, 45))
    elif kind == "ind":
        pen.rectangle([fx, fy, fx + fw, fy + 15], fill=(255, 153, 51))
        pen.rectangle([fx, fy + 15, fx + fw, fy + 31], fill=(250, 250, 250))
        pen.rectangle([fx, fy + 31, fx + fw, fy + 46], fill=(19, 136, 8))
        cx, cy = fx + fw // 2, fy + 23
        pen.ellipse([cx - 8, cy - 8, cx + 8, cy + 8], outline=(0, 0, 128),
                    width=2)
        for step in range(8):
            theta = math.tau * step / 8
            pen.line([(cx, cy),
                      (cx + 8 * math.cos(theta), cy + 8 * math.sin(theta))],
                     fill=(0, 0, 128), width=1)
    elif kind == "aus":
        pen.rectangle(area, fill=(0, 0, 139))
        pen.rectangle([fx, fy, fx + 34, fy + 22], fill=(200, 30, 30))
        pen.line([(fx, fy), (fx + 34, fy + 22)], fill=(250, 250, 250), width=2)
        pen.line([(fx + 34, fy), (fx, fy + 22)], fill=(250, 250, 250), width=2)
        for sx, sy in ((52, 12), (60, 32), (46, 36)):
            pen.ellipse([fx + sx - 3, fy + sy - 3, fx + sx + 3, fy + sy + 3],
                        fill=(250, 250, 250))
    elif kind == "chn":
        pen.rectangle(area, fill=(222, 30, 30))
        pen.ellipse([fx + 12, fy + 9, fx + 24, fy + 21], fill=(250, 210, 40))
        for sx, sy in ((34, 8), (42, 14), (42, 24), (34, 30)):
            pen.ellipse([fx + sx - 3, fy + sy - 3, fx + sx + 3, fy + sy + 3],
                        fill=(250, 210, 40))
    elif kind == "can":
        pen.rectangle([fx, fy, fx + 18, fy + fh], fill=(200, 30, 30))
        pen.rectangle([fx + fw - 18, fy, fx + fw, fy + fh], fill=(200, 30, 30))
        pen.rectangle([fx + 18, fy, fx + fw - 18, fy + fh],
                      fill=(250, 250, 250))
        cx, cy = fx + fw // 2, fy + fh // 2
        pen.polygon([(cx, cy - 14), (cx + 6, cy - 4), (cx + 14, cy - 8),
                     (cx + 9, cy + 2), (cx + 13, cy + 8), (cx + 4, cy + 7),
                     (cx + 3, cy + 15), (cx - 3, cy + 15), (cx - 4, cy + 7),
                     (cx - 13, cy + 8), (cx - 9, cy + 2), (cx - 14, cy - 8),
                     (cx - 6, cy - 4)], fill=(200, 30, 30))


def paint_quad(pen, area):
    """Four Quad flags on poles — the Manila talks: US, Japan, India, AUS."""
    x0, y0, x1, y1 = area
    pen.rectangle(area, fill=(222, 232, 240))
    pen.rectangle([x0, y1 - 26, x1, y1], fill=(120, 140, 120))
    ground = y1 - 26
    flag_w, flag_h = 56, 36
    slot = (x1 - x0 - 4 * flag_w) // 5
    for pos, kind in enumerate(("usa", "jpn", "ind", "aus")):
        left = x0 + slot + pos * (flag_w + slot)
        top = y0 + 26
        pen.rectangle([left - 3, top, left, ground], fill=(90, 90, 90))
        paint_flag(pen, (left, top, left + flag_w, top + flag_h), kind)
    pen.text(((x0 + x1) // 2, y1 - 20), "MANILA",
             font=typeface("sans_heavy", 13), fill=(70, 70, 70), anchor="ma")


def paint_trade(pen, area):
    """Canada and China flags facing each other across a small globe table."""
    x0, y0, x1, y1 = area
    pen.rectangle(area, fill=(226, 234, 228))
    pen.rectangle([x0, y1 - 26, x1, y1], fill=(140, 130, 110))
    ground = y1 - 26
    flag_w, flag_h = 74, 46
    top = y0 + 22
    left = x0 + 28
    pen.rectangle([left - 4, top, left, ground], fill=(90, 90, 90))
    paint_flag(pen, (left, top, left + flag_w, top + flag_h), "can")
    right = x1 - 28 - flag_w
    pen.rectangle([right + flag_w, top, right + flag_w + 4, ground],
                  fill=(90, 90, 90))
    paint_flag(pen, (right, top, right + flag_w, top + flag_h), "chn")
    centre = (x0 + x1) // 2
    pen.rectangle([centre - 52, ground - 34, centre + 52, ground - 28],
                  fill=(120, 80, 40))
    pen.rectangle([centre - 44, ground - 28, centre - 36, ground],
                  fill=(90, 60, 30))
    pen.rectangle([centre + 36, ground - 28, centre + 44, ground],
                  fill=(90, 60, 30))
    pen.ellipse([centre - 20, ground - 72, centre + 20, ground - 32],
                fill=PALETTE["ocean"], outline=PALETTE["ink"], width=2)
    pen.arc([centre - 20, ground - 72, centre + 20, ground - 32], 200, 340,
            fill=(120, 170, 205), width=2)
    pen.line([(centre - 20, ground - 52), (centre + 20, ground - 52)],
             fill=(120, 170, 205), width=2)


def paint_storm(pen, area):
    """Cyclone Akvan: spiral cloud bands over a dark teal sea, rain below."""
    x0, y0, x1, y1 = area
    pen.rectangle(area, fill=(30, 60, 90))
    water = y0 + int((y1 - y0) * 0.66)
    pen.rectangle([x0, water, x1, y1], fill=(16, 70, 90))
    cx = (x0 + x1) // 2
    cy = y0 + int((y1 - y0) * 0.38)
    for arm in range(3):
        trail = []
        for step in range(0, 181, 6):
            theta = math.radians(step + arm * 120)
            reach = 8 + step * 0.42
            trail.append((cx + reach * math.cos(theta),
                          cy + reach * math.sin(theta) * 0.8))
        pen.line(trail, fill=(220, 230, 240), width=10)
    pen.ellipse([cx - 14, cy - 12, cx + 14, cy + 12], fill=(250, 250, 250))
    for col in range(9):
        rx = x0 + 14 + col * 30
        pen.line([(rx, water + 6), (rx - 8, water + 30)],
                 fill=(150, 200, 220), width=3)
    for row in range(4):
        yy = water + 12 + row * 14
        pen.line([(x0 + 10 + row * 24, yy), (x1 - 10 - row * 18, yy)],
                 fill=(90, 160, 190), width=3)
    tx, ty = x1 - 52, y0 + 18
    pen.polygon([(tx, ty), (tx + 34, ty), (tx + 17, ty + 30)],
                fill=(250, 200, 60), outline=PALETTE["ink"], width=2)
    pen.text((tx + 17, ty + 8), "!", font=typeface("sans_heavy", 16),
             fill=PALETTE["ink"], anchor="ma")


def build_sheet() -> Sheet:
    """Compose the whole front page and return the finished sheet."""
    sheet = Sheet()
    left, right = EDGE, SIDE - EDGE

    # ---- masthead ----
    sheet.box((left, EDGE, right, 118), colour=PALETTE["ink"])
    sheet.centred((left + right) // 2, 30, "THE WORLD IN ONE DAY",
                  "serif_heavy", 58, colour=(250, 248, 240))
    sheet.centred((left + right) // 2, 92,
                  "ONE IMAGE  •  EVERY STORY THAT MATTERED",
                  "sans_bold", 17, colour=PALETTE["gold"])
    sheet.hline(left, right, 128, PALETTE["scarlet"], thick=5)

    # ---- dateline ----
    sheet.pen.text((left, 138), "WEDNESDAY, 18 NOVEMBER 2026",
                   font=typeface("sans_heavy", 26), fill=PALETTE["ink"])
    sheet.right(right, 138, "WORLD NEWS", "sans_bold", 26,
                colour=PALETTE["scarlet"])
    sheet.hline(left, right, 172, PALETTE["ink"])

    # ---- lead story: the Kerch Bridge, struck a second day ----
    lead_top, lead_bottom = 184, 512
    sheet.box((left, lead_top, right, lead_bottom), outline=PALETTE["ink"])
    paint_bridge(sheet.pen, (left + 3, lead_top + 3, right - 3,
                             lead_top + 208))
    sheet.paragraph(left + 14, lead_top + 214,
                    "KERCH BRIDGE SPAN FALLS INTO THE SEA",
                    "serif_heavy", 40, right - left - 28, gap=1.2)
    sheet.pen.text((left + 14, lead_top + 266),
                   "Second Ukrainian strike in two days halts road traffic",
                   font=typeface("sans", 23), fill=PALETTE["muted"])
    sheet.pen.text((left + 14, lead_top + 294),
                   "to occupied Crimea; Russia hits back at bridges in Kyiv.",
                   font=typeface("sans", 20), fill=PALETTE["muted"])

    # ---- three panels ----
    panel_top, panel_bottom = 528, 852
    col_w = (right - left - 2 * 16) // 3
    stories = [
        ("TRUMP ARRIVES IN MANILA",
         "Quad talks open ahead of his visit to China.",
         paint_quad),
        ("CANADA AND CHINA EXTEND TRADE DEALS",
         "Xi meets Carney before the APEC summit.",
         paint_trade),
        ("CYCLONE AKVAN STRENGTHENS",
         "Bay of Bengal storm puts India's east coast on alert.",
         paint_storm),
    ]
    for pos, (headline, standfirst, painter) in enumerate(stories):
        px0 = left + pos * (col_w + 16)
        px1 = px0 + col_w
        sheet.box((px0, panel_top, px1, panel_bottom), outline=PALETTE["ink"])
        painter(sheet.pen, (px0 + 3, panel_top + 3, px1 - 3, panel_top + 158))
        y = sheet.paragraph(px0 + 10, panel_top + 168, headline,
                            "serif", 27, px1 - px0 - 20, gap=1.19)
        sheet.paragraph(px0 + 10, y, standfirst, "sans", 19,
                        px1 - px0 - 20, colour=PALETTE["muted"], gap=1.26)

    # ---- ticker: also today ----
    tick_top, tick_bottom = 868, 952
    sheet.box((left, tick_top, right, tick_bottom), colour=PALETTE["panel"],
              outline=PALETTE["ink"], thick=2)
    sheet.pen.text((left + 12, tick_top + 6), "ALSO TODAY",
                   font=typeface("sans_heavy", 20), fill=PALETTE["scarlet"])
    sheet.paragraph(left + 12, tick_top + 30,
                    "Democrats celebrate taking Congress  •  UK sanctions "
                    "Israeli settlement firms  •  Knesset elects new Speaker "
                    "in blow to Netanyahu  •  Dhoni retires from IPL, to "
                    "mentor CSK  •  Iran claims fresh drone attack on "
                    "Bahrain radar",
                    "sans", 18, right - left - 24, gap=1.22)

    # ---- footer ----
    sheet.hline(left, right, 966, PALETTE["scarlet"], thick=3)
    sheet.centred((left + right) // 2, 976,
                  "18 NOVEMBER 2026  •  THE DAY IN ONE IMAGE",
                  "sans_bold", 18)
    return sheet


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    target = os.path.join(here, "assets", "entry.png")
    build_sheet().save(target)


if __name__ == "__main__":
    main()
