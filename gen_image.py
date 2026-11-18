#!/usr/bin/env python3
"""Draw the 18 November 2026 world-news front page (1024x1024 PNG).

Built locally with Pillow; the entry program (main.py, stdlib only) simply
copies the finished image. Deterministic: fixed geometry, fixed text, no
randomness, no timestamps embedded.
"""
import math
import os
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (246, 241, 229)
INK = (18, 18, 18)
RED = (178, 34, 34)
NAVY = (23, 42, 74)
SEA = (28, 68, 110)
TEAL = (16, 96, 110)
GREY = (90, 90, 88)
LIGHT = (232, 226, 210)

SERIF_B = "/usr/share/fonts/truetype/noto/NotoSerif-Bold.ttf"
SERIF_BLK = "/usr/share/fonts/truetype/noto/NotoSerif-Black.ttf"
SANS_B = "/usr/share/fonts/truetype/noto/NotoSans-Bold.ttf"
SANS_R = "/usr/share/fonts/truetype/noto/NotoSans-Regular.ttf"
SANS_BLK = "/usr/share/fonts/truetype/noto/NotoSans-Black.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_w):
    """Greedy word wrap by pixel width; returns list of lines."""
    words = text.split()
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if draw.textlength(trial, font=fnt) <= max_w or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def text_block(draw, xy, lines, fnt, fill=INK, align="left", leading=1.15):
    x, y = xy
    for ln in lines:
        w = draw.textlength(ln, font=fnt)
        if align == "center":
            draw.text((x - w / 2, y), ln, font=fnt, fill=fill)
        elif align == "right":
            draw.text((x - w, y), ln, font=fnt, fill=fill)
        else:
            draw.text((x, y), ln, font=fnt, fill=fill)
        y += int(fnt.size * leading)
    return y


def rule(draw, x0, x1, y, fill=INK, width=2):
    draw.line([(x0, y), (x1, y)], fill=fill, width=width)


def explosion(draw, cx, cy, r, fill=(232, 120, 30)):
    """Starburst: alternating long/short triangles around a centre."""
    pts = []
    for i in range(24):
        ang = math.pi * 2 * i / 24
        rr = r if i % 2 == 0 else r * 0.45
        pts.append((cx + rr * math.cos(ang), cy + rr * math.sin(ang)))
    draw.polygon(pts, fill=fill)
    draw.ellipse([cx - r * 0.45, cy - r * 0.45, cx + r * 0.45, cy + r * 0.45],
                 fill=(250, 200, 60))


def smoke(draw, cx, cy, fill=(120, 120, 118)):
    for dx, dy, r in [(-34, 6, 26), (0, -12, 32), (34, 4, 26), (-8, -30, 24),
                      (22, -26, 20)]:
        draw.ellipse([cx + dx - r, cy + dy - r, cx + dx + r, cy + dy + r],
                     fill=fill)


def flame(draw, cx, base_y, w, h):
    """Simple flame: stacked triangles, orange over yellow."""
    draw.polygon([(cx - w, base_y), (cx + w, base_y), (cx, base_y - h)],
                 fill=(232, 110, 20))
    draw.polygon([(cx - w * 0.55, base_y), (cx + w * 0.55, base_y),
                  (cx, base_y - h * 0.62)], fill=(250, 200, 60))


def bridge_scene(draw, x0, y0, x1, y1):
    """Kerch Bridge: sea, deck with a collapsed middle span, smoke, fire."""
    draw.rectangle([x0, y0, x1, y1], fill=(214, 226, 238))  # sky
    draw.rectangle([x0, y0, x1, y0 + 26], fill=(250, 214, 130))  # low sun band
    draw.ellipse([x0 + 26, y0 + 8, x0 + 78, y0 + 60], fill=(250, 190, 80))
    sea_y = y0 + int((y1 - y0) * 0.62)
    draw.rectangle([x0, sea_y, x1, y1], fill=SEA)
    for i in range(5):  # wave lines
        yy = sea_y + 14 + i * 16
        draw.line([(x0 + 12 + i * 30, yy), (x1 - 12 - i * 22, yy)],
                  fill=(120, 170, 205), width=3)
    deck_y = sea_y - 34
    mid = (x0 + x1) // 2
    # pylons
    for px in (x0 + 70, x1 - 70):
        draw.rectangle([px - 7, deck_y - 96, px + 7, deck_y], fill=(70, 70, 72))
        draw.line([(px, deck_y - 96), (max(x0, px - 90), deck_y)],
                  fill=(120, 120, 122), width=2)
        draw.line([(px, deck_y - 96), (min(x1, px + 90), deck_y)],
                  fill=(120, 120, 122), width=2)
    # deck: left and right spans, middle collapsed
    draw.rectangle([x0, deck_y, mid - 58, deck_y + 12], fill=(52, 52, 54))
    draw.rectangle([mid + 58, deck_y, x1, deck_y + 12], fill=(52, 52, 54))
    # fallen span tilted into the sea
    draw.polygon([(mid - 52, deck_y + 4), (mid + 46, deck_y + 30),
                  (mid + 40, deck_y + 44), (mid - 58, deck_y + 18)],
                 fill=(52, 52, 54))
    explosion(draw, mid, deck_y - 6, 46)
    smoke(draw, mid - 8, deck_y - 66)
    smoke(draw, mid + 40, deck_y - 52, fill=(140, 140, 138))


def flag(draw, fx, fy, fw, fh, kind):
    """Draw one small flag at (fx, fy); kind selects the design."""
    draw.rectangle([fx, fy, fx + fw, fy + fh], outline=INK, width=2)
    if kind == "usa":
        for s in range(7):
            draw.rectangle([fx, fy + s * 7, fx + fw, fy + s * 7 + 7],
                           fill=(178, 34, 34) if s % 2 == 0
                           else (250, 250, 250))
        draw.rectangle([fx, fy, fx + 30, fy + 24], fill=(30, 50, 110))
        for sx in (6, 16, 26):
            for sy in (5, 13):
                draw.ellipse([fx + sx - 2, fy + sy - 2, fx + sx + 2,
                              fy + sy + 2], fill=(250, 250, 250))
    elif kind == "jpn":
        draw.rectangle([fx, fy, fx + fw, fy + fh], fill=(250, 250, 250))
        draw.ellipse([fx + fw // 2 - 13, fy + fh // 2 - 13,
                      fx + fw // 2 + 13, fy + fh // 2 + 13],
                     fill=(188, 0, 45))
    elif kind == "ind":
        draw.rectangle([fx, fy, fx + fw, fy + 15], fill=(255, 153, 51))
        draw.rectangle([fx, fy + 15, fx + fw, fy + 31], fill=(250, 250, 250))
        draw.rectangle([fx, fy + 31, fx + fw, fy + 46], fill=(19, 136, 8))
        cx, cy = fx + fw // 2, fy + 23
        draw.ellipse([cx - 8, cy - 8, cx + 8, cy + 8], outline=(0, 0, 128),
                     width=2)
        for a in range(0, 360, 45):
            r = math.radians(a)
            draw.line([(cx, cy), (cx + 8 * math.cos(r), cy + 8 * math.sin(r))],
                      fill=(0, 0, 128), width=1)
    elif kind == "aus":
        draw.rectangle([fx, fy, fx + fw, fy + fh], fill=(0, 0, 139))
        # union canton, simplified
        draw.rectangle([fx, fy, fx + 34, fy + 22], fill=(200, 30, 30))
        draw.line([(fx, fy), (fx + 34, fy + 22)], fill=(250, 250, 250), width=2)
        draw.line([(fx + 34, fy), (fx, fy + 22)], fill=(250, 250, 250), width=2)
        for sx, sy in [(52, 12), (60, 32), (46, 36)]:
            draw.ellipse([fx + sx - 3, fy + sy - 3, fx + sx + 3, fy + sy + 3],
                         fill=(250, 250, 250))
    elif kind == "chn":
        draw.rectangle([fx, fy, fx + fw, fy + fh], fill=(222, 30, 30))
        draw.ellipse([fx + 12, fy + 9, fx + 24, fy + 21], fill=(250, 210, 40))
        for sx, sy in [(34, 8), (42, 14), (42, 24), (34, 30)]:
            draw.ellipse([fx + sx - 3, fy + sy - 3, fx + sx + 3,
                          fy + sy + 3], fill=(250, 210, 40))
    elif kind == "can":
        draw.rectangle([fx, fy, fx + 18, fy + fh], fill=(200, 30, 30))
        draw.rectangle([fx + fw - 18, fy, fx + fw, fy + fh], fill=(200, 30, 30))
        draw.rectangle([fx + 18, fy, fx + fw - 18, fy + fh],
                       fill=(250, 250, 250))
        # maple leaf, simplified as a red diamond-star
        cx, cy = fx + fw // 2, fy + fh // 2
        draw.polygon([(cx, cy - 14), (cx + 6, cy - 4), (cx + 14, cy - 8),
                      (cx + 9, cy + 2), (cx + 13, cy + 8), (cx + 4, cy + 7),
                      (cx + 3, cy + 15), (cx - 3, cy + 15), (cx - 4, cy + 7),
                      (cx - 13, cy + 8), (cx - 9, cy + 2), (cx - 14, cy - 8),
                      (cx - 6, cy - 4)], fill=(200, 30, 30))


def quad_scene(draw, x0, y0, x1, y1):
    """Four Quad flags on poles: USA, Japan, India, Australia — Manila talks."""
    draw.rectangle([x0, y0, x1, y1], fill=(222, 232, 240))
    draw.rectangle([x0, y1 - 26, x1, y1], fill=(120, 140, 120))  # ground
    base_y = y1 - 26
    kinds = ["usa", "jpn", "ind", "aus"]
    fw, fh = 56, 36
    gap = (x1 - x0 - 4 * fw) // 5
    for i, kind in enumerate(kinds):
        fx = x0 + gap + i * (fw + gap)
        fy = y0 + 26
        draw.rectangle([fx - 3, fy, fx, base_y], fill=(90, 90, 90))  # pole
        flag(draw, fx, fy, fw, fh, kind)
    draw.text(((x0 + x1) // 2, y1 - 20), "MANILA",
              font=font(SANS_BLK, 13), fill=(70, 70, 70), anchor="ma")


def canada_china_scene(draw, x0, y0, x1, y1):
    """Canada and China flags facing each other over a handshake table."""
    draw.rectangle([x0, y0, x1, y1], fill=(226, 234, 228))
    draw.rectangle([x0, y1 - 26, x1, y1], fill=(140, 130, 110))  # ground
    base_y = y1 - 26
    fw, fh = 74, 46
    # Canada, left
    fx = x0 + 28
    fy = y0 + 22
    draw.rectangle([fx - 4, fy, fx, base_y], fill=(90, 90, 90))
    flag(draw, fx, fy, fw, fh, "can")
    # China, right
    fx2 = x1 - 28 - fw
    draw.rectangle([fx2 + fw, fy, fx2 + fw + 4, base_y], fill=(90, 90, 90))
    flag(draw, fx2, fy, fw, fh, "chn")
    # table between the poles with a small globe on it
    cx = (x0 + x1) // 2
    draw.rectangle([cx - 52, base_y - 34, cx + 52, base_y - 28],
                   fill=(120, 80, 40))
    draw.rectangle([cx - 44, base_y - 28, cx - 36, base_y], fill=(90, 60, 30))
    draw.rectangle([cx + 36, base_y - 28, cx + 44, base_y], fill=(90, 60, 30))
    draw.ellipse([cx - 20, base_y - 72, cx + 20, base_y - 32], fill=SEA,
                 outline=INK, width=2)
    draw.arc([cx - 20, base_y - 72, cx + 20, base_y - 32], 200, 340,
             fill=(120, 170, 205), width=2)
    draw.line([(cx - 20, base_y - 52), (cx + 20, base_y - 52)],
              fill=(120, 170, 205), width=2)


def cyclone_scene(draw, x0, y0, x1, y1):
    """Cyclone Akvan: spiral cloud bands over a dark teal sea, rain below."""
    draw.rectangle([x0, y0, x1, y1], fill=(30, 60, 90))
    sea_y = y0 + int((y1 - y0) * 0.66)
    draw.rectangle([x0, sea_y, x1, y1], fill=(16, 70, 90))
    cx = (x0 + x1) // 2
    cy = y0 + int((y1 - y0) * 0.38)
    # spiral arms
    for k in range(3):
        pts = []
        for t in range(0, 181, 6):
            ang = math.radians(t + k * 120)
            rr = 8 + t * 0.42
            pts.append((cx + rr * math.cos(ang), cy + rr * math.sin(ang) * 0.8))
        draw.line(pts, fill=(220, 230, 240), width=10)
    draw.ellipse([cx - 14, cy - 12, cx + 14, cy + 12], fill=(250, 250, 250))
    # rain streaks
    for i in range(9):
        rx = x0 + 14 + i * 30
        draw.line([(rx, sea_y + 6), (rx - 8, sea_y + 30)],
                  fill=(150, 200, 220), width=3)
    for i in range(4):
        yy = sea_y + 12 + i * 14
        draw.line([(x0 + 10 + i * 24, yy), (x1 - 10 - i * 18, yy)],
                  fill=(90, 160, 190), width=3)
    # land warning triangle
    tx, ty = x1 - 52, y0 + 18
    draw.polygon([(tx, ty), (tx + 34, ty), (tx + 17, ty + 30)],
                 fill=(250, 200, 60), outline=INK, width=2)
    draw.text((tx + 17, ty + 8), "!", font=font(SANS_BLK, 16), fill=INK,
              anchor="ma")


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    M = 24  # margin
    X0, X1 = M, W - M

    # ---- masthead ----
    d.rectangle([X0, M, X1, 118], fill=INK)
    d.text(((X0 + X1) // 2, 30), "THE WORLD IN ONE DAY",
           font=font(SERIF_BLK, 58), fill=(250, 248, 240), anchor="ma")
    d.text(((X0 + X1) // 2, 92), "ONE IMAGE  •  EVERY STORY THAT MATTERED",
           font=font(SANS_B, 17), fill=(200, 160, 60), anchor="ma")
    rule(d, X0, X1, 128, fill=RED, width=5)

    # ---- dateline ----
    d.text((X0, 138), "WEDNESDAY, 18 NOVEMBER 2026",
           font=font(SANS_BLK, 26), fill=INK)
    d.text((X1, 138), "WORLD NEWS",
           font=font(SANS_B, 26), fill=RED, anchor="ra")
    rule(d, X0, X1, 172, width=2)

    # ---- lead story: Kerch Bridge, second strike ----
    ly0, ly1 = 184, 512
    d.rectangle([X0, ly0, X1, ly1], outline=INK, width=3)
    bridge_scene(d, X0 + 3, ly0 + 3, X1 - 3, ly0 + 208)
    hy = ly0 + 214
    for ln in wrap(d, "KERCH BRIDGE SPAN FALLS INTO THE SEA",
                   font(SERIF_BLK, 40), X1 - X0 - 28):
        d.text((X0 + 14, hy), ln, font=font(SERIF_BLK, 40), fill=INK)
        hy += 48
    d.text((X0 + 14, ly0 + 266),
           "Second Ukrainian strike in two days halts road traffic",
           font=font(SANS_R, 23), fill=(60, 60, 60))
    d.text((X0 + 14, ly0 + 294),
           "to occupied Crimea; Russia hits back at bridges in Kyiv.",
           font=font(SANS_R, 20), fill=(60, 60, 60))

    # ---- three panels ----
    py0, py1 = 528, 852
    pw = (X1 - X0 - 2 * 16) // 3
    panels = [
        ("TRUMP ARRIVES IN MANILA",
         "Quad talks open ahead of his visit to China.",
         quad_scene),
        ("CANADA AND CHINA EXTEND TRADE DEALS",
         "Xi meets Carney before the APEC summit.",
         canada_china_scene),
        ("CYCLONE AKVAN STRENGTHENS",
         "Bay of Bengal storm puts India's east coast on alert.",
         cyclone_scene),
    ]
    for i, (head, sub, scene) in enumerate(panels):
        px0 = X0 + i * (pw + 16)
        px1 = px0 + pw
        d.rectangle([px0, py0, px1, py1], outline=INK, width=3)
        scene(d, px0 + 3, py0 + 3, px1 - 3, py0 + 158)
        y = py0 + 168
        for ln in wrap(d, head, font(SERIF_B, 27), px1 - px0 - 20):
            d.text((px0 + 10, y), ln, font=font(SERIF_B, 27), fill=INK)
            y += 32
        for ln in wrap(d, sub, font(SANS_R, 19), px1 - px0 - 20):
            d.text((px0 + 10, y), ln, font=font(SANS_R, 19), fill=(60, 60, 60))
            y += 24

    # ---- ticker: also today ----
    ty0, ty1 = 868, 952
    d.rectangle([X0, ty0, X1, ty1], fill=(232, 226, 210), outline=INK, width=2)
    d.text((X0 + 12, ty0 + 6), "ALSO TODAY",
           font=font(SANS_BLK, 20), fill=RED)
    ticker = ("Democrats celebrate taking Congress  •  UK sanctions Israeli "
              "settlement firms  •  Knesset elects new Speaker in blow to "
              "Netanyahu  •  Dhoni retires from IPL, to mentor CSK  •  Iran "
              "claims fresh drone attack on Bahrain radar")
    y = ty0 + 30
    for ln in wrap(d, ticker, font(SANS_R, 18), X1 - X0 - 24):
        d.text((X0 + 12, y), ln, font=font(SANS_R, 18), fill=INK)
        y += 22

    # ---- footer ----
    rule(d, X0, X1, 966, fill=RED, width=3)
    d.text(((X0 + X1) // 2, 976), "18 NOVEMBER 2026  •  THE DAY IN ONE IMAGE",
           font=font(SANS_B, 18), fill=INK, anchor="ma")

    out = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                       "assets", "entry.png")
    img.save(out, format="PNG", optimize=True)
    print("wrote", out, os.path.getsize(out), "bytes")


if __name__ == "__main__":
    main()
