#!/usr/bin/env python3
"""news-image-20261122 v6: "v1.1 + plntky's numbers" — the front page that
scored highest (v1.1, 98.5964%, 12-0) with the four things research round
3 found missing from it.

Research round 3 (fresh top 10, 22:38 WIB) proved three things:
1. The "decline" v1.1 -> v3 -> v4 -> v5 is NOISE: all four versions faced
   the EXACT SAME 7 opponents, margins 96/93/92/93 of 120 — all < 1 SE.
   But v1.1's edge is real: it is the only version that maxed the
   provisional round (40/40), because its 35-story breadth beat the
   strongest anchor 5-0.
2. The single biggest gap is CONTEND, not the image: every entry at
   ranks 1-185 has contend, every entry at 190+ does not, and all four
   of our versions are NULL. A lottery we cannot force — so v6's job is
   to be the highest-win_rate image we can field (v1.1's base) and hope
   its heat closes with a median (+0.40) boost.
3. v5's cut to 6 stories LOST breadth points: v1.1's adaptive wins are
   ALL attributed to breadth ("35 stories versus A's four items"), while
   rank 1 at 300px is mostly noise in its bottom two thirds and is still
   #1. Breadth dominates the 300px legibility deduction.

So v6 keeps v1.1's skeleton whole — 35 stories, 7 regions, lead trio in
order (186 drones / COP31 no-deal / Iran Bahrain CLAIM), DATE CHECK,
certainty labels, sources, number strip — and adds the four things the
top 10 all have and v1.1 lacked:
1. A UTC timeline strip under the region bar (7 timed beats, v2's code).
2. Plntky-style GIANT number anchors (28-32px) on the small cards,
   overlaid ON the 48px illustrated scenes (v3's scenes + anchors, with
   the 2px contrasting stroke so they read at 300px).
3. The COP31 hero's empty dashed box fixed: a real scene — delegates
   at a table, gavel, and a rotated red NO DEAL stamp (v3's art).
4. A bigger world map (360x130, was 340x123) with the region-colour
   key underneath (v2's key).

Layout budget: the 30px timeline strip is paid for by compressing the
top (masthead cap 88 -> 76px, numbers 30 -> 28px) and by keeping the
hero art at 122px (v1.1 had 130, v3 had 100) — NOT by shortening the
heroes the way v2/v3 did, because v1.1's tall heroes are part of what
won the provisional round. Tiles stay 136px with 48px scenes.

Deterministic: fixed fonts, no randomness, no network. PIL only.
"""
from PIL import Image, ImageDraw, ImageFont
import math
import os

W = H = 1024
PAPER = (247, 244, 235)
CARD = (250, 247, 240)
INK = (17, 19, 23)
WHITE = (255, 255, 255)
RED = (200, 50, 40)
CRIMSON = (184, 32, 24)
NAVY = (29, 53, 87)
GOLD = (201, 162, 39)
GREY = (110, 110, 105)
GREEN = (46, 125, 50)
TEAL = (14, 124, 123)
AMBER = (183, 121, 31)

SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SERIF_I = "/usr/share/fonts/truetype/noto/NotoSerif-Italic.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
MASTHEAD = "/usr/share/fonts/truetype/noto/NotoSerif-ExtraCondensedBold.ttf"
MASTHEAD_NUM = "/usr/share/fonts/truetype/noto/NotoSerif-Bold.ttf"
MAP_PATH = "/home/hatch/workspace/makefun/news-image-20261122-work/world_map5.png"
OUT_RGB = "/home/hatch/workspace/makefun/news-image-20261122-work/entry-v6-rgb.png"
OUT_PAL = "/home/hatch/workspace/makefun/news-image-20261122-work/entry-v6-pal.png"


def F(p, s):
    return ImageFont.truetype(p, s)


def wrap(d, text, font, max_w):
    lines, cur = [], ""
    for w in text.split():
        t = (cur + " " + w).strip()
        if d.textlength(t, font=font) <= max_w:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def block(d, x, y, text, font, max_w, leading, color=INK, max_lines=None):
    lines = wrap(d, text, font, max_w)
    if max_lines:
        lines = lines[:max_lines]
    for ln in lines:
        d.text((x, y), ln, font=font, fill=color)
        y += leading
    return y


def badge(d, x, y, text, color):
    """Small verification pill, right-aligned at x (x = right edge)."""
    f = F(SANS_B, 11)
    tw = d.textlength(text, font=f)
    d.rounded_rectangle([x - tw - 12, y, x, y + 15], radius=7, fill=color)
    d.text((x - tw / 2 - 6, y + 2), text, font=f, fill=(255, 255, 255), anchor="mt")


def kicker_label(d, x, y, text, size=17):
    """Red kicker label inside an illustration (top-left)."""
    f = F(SANS_B, size)
    tw = d.textlength(text, font=f)
    d.rectangle([x, y, x + tw + 16, y + size + 10], fill=RED)
    d.text((x + 8, y + 4), text, font=f, fill=(255, 255, 255))


def stat_chip(d, x, y, text):
    """White stat chip inside an illustration (bottom-left)."""
    f = F(SANS_B, 12)
    tw = d.textlength(text, font=f)
    d.rectangle([x, y, x + tw + 12, y + 20], fill=(255, 255, 255))
    d.text((x + 6, y + 3), text, font=f, fill=INK)


def map_key(d, x, y, items):
    """One row of the region-colour key under the map: colour chip + name."""
    cx = x
    f = F(SANS_B, 11)
    for name, color in items:
        d.rectangle([cx, y + 1, cx + 10, y + 11], fill=color)
        d.text((cx + 14, y), name, font=f, fill=INK)
        cx += 14 + d.textlength(name, font=f) + 16
    return cx


# ------------------------------------------------- hero illustrations (314x122)
# v6: v3's enriched scenes (delegates + NO DEAL stamp for COP31, extra
# drones + smoke over Dymer, Patriot launcher + second ship off Bahrain).
# Each art function gets the image itself (img) so the COP31 stamp can
# be drawn on a transparent layer, rotated, and composited.
def art_cop31(img, d, x, y, w, h):
    # Antalya: negotiation table, five delegates, document, gavel, flags,
    # and a rotated red NO DEAL stamp over the scene (rank 5 style).
    d.rectangle([x, y, x + w, y + h], fill=(224, 238, 224))
    # flags behind the delegates: three small pennants on poles
    for fx, fc in [(35, (200, 50, 40)), (155, (29, 53, 87)), (275, (14, 124, 123))]:
        d.line([x + fx, y + 8, x + fx, y + 30], fill=(90, 90, 90), width=2)
        d.polygon([(x + fx, y + 8), (x + fx + 16, y + 13), (x + fx, y + 18)], fill=fc)
    # delegates: heads + suited bodies behind the table
    skins = [(230, 200, 170), (200, 160, 130), (240, 210, 180),
             (180, 140, 110), (220, 190, 160)]
    suits = [(29, 53, 87), (90, 90, 90), (14, 124, 123), (110, 70, 40), (60, 90, 60)]
    for i, hx in enumerate([40, 100, 160, 220, 275]):
        d.ellipse([x + hx - 10, y + 26, x + hx + 10, y + 46], fill=skins[i])
        d.pieslice([x + hx - 10, y + 26, x + hx + 10, y + 46], start=180, end=360,
                   fill=(40, 32, 24))
        d.polygon([(x + hx - 22, y + 72), (x + hx - 16, y + 48),
                   (x + hx + 16, y + 48), (x + hx + 22, y + 72)], fill=suits[i])
        d.polygon([(x + hx - 4, y + 48), (x + hx, y + 58), (x + hx + 4, y + 48)],
                  fill=(255, 255, 255))
    # table (front panel + top edge)
    d.rectangle([x, y + 72, x + w, y + h], fill=(150, 110, 70))
    d.rectangle([x, y + 72, x + w, y + 76], fill=(180, 140, 95))
    # document on the table, left
    d.rectangle([x + 28, y + 78, x + 100, y + 96], fill=(255, 255, 255),
                outline=NAVY, width=1)
    for i in range(3):
        d.line([x + 34, y + 83 + i * 4, x + 94, y + 83 + i * 4], fill=GREY, width=1)
    # gavel, centre
    d.line([x + 118, y + 94, x + 138, y + 80], fill=(120, 80, 40), width=4)
    d.rectangle([x + 132, y + 74, x + 152, y + 84], fill=(120, 80, 40))
    # nameplate on the table, right of the gavel
    d.rectangle([x + 160, y + 80, x + 196, y + 88], fill=(255, 255, 255),
                outline=GREY, width=1)
    d.line([x + 164, y + 84, x + 192, y + 84], fill=GREY, width=1)
    # rotated NO DEAL stamp over the table, lower-right (small enough to
    # leave the delegates' heads and the stat chip clear)
    stamp = Image.new("RGBA", (130, 40), (0, 0, 0, 0))
    sd = ImageDraw.Draw(stamp)
    sd.rectangle([3, 3, 126, 36], outline=(200, 50, 40), width=4)
    sd.text((65, 20), "NO DEAL", font=F(SANS_B, 20), fill=(200, 50, 40), anchor="mm")
    stamp = stamp.rotate(-8, expand=True, resample=Image.BICUBIC)
    img.paste(stamp, (x + 168, y + 40), stamp)


def art_drones(img, d, x, y, w, h):
    # Kyiv night: drones, interceptor bursts, skyline, and the Dymer block
    # burning — fire at its base, smoke rising, embers. No empty sky.
    d.rectangle([x, y, x + w, y + h], fill=(16, 22, 48))
    for sx, sy in [(16, 12), (70, 8), (130, 14), (195, 10), (250, 16), (300, 10),
                   (50, 30), (165, 28), (230, 32), (285, 34)]:
        d.ellipse([x + sx, y + sy, x + sx + 3, y + sy + 3], fill=(255, 255, 255))
    # drones: small dark crosses with red lights (two more, top-right)
    for dx, dy in [(45, 16), (115, 12), (185, 20), (245, 14), (290, 24), (150, 34),
                   (262, 10), (215, 6)]:
        d.line([x + dx - 10, y + dy, x + dx + 10, y + dy], fill=(200, 200, 210), width=2)
        d.line([x + dx, y + dy - 6, x + dx, y + dy + 6], fill=(200, 200, 210), width=2)
        d.ellipse([x + dx - 2, y + dy - 2, x + dx + 2, y + dy + 2], fill=(255, 60, 40))
    # interceptor bursts
    for fx, fy in [(95, 58), (205, 52), (275, 64)]:
        for a in range(8):
            ang = a * math.pi / 4
            d.line([x + fx, y + fy, x + fx + 16 * math.cos(ang),
                    y + fy + 16 * math.sin(ang)], fill=(255, 200, 90), width=3)
        d.ellipse([x + fx - 4, y + fy - 4, x + fx + 4, y + fy + 4],
                  fill=(255, 220, 120))
    # skyline across the whole bottom
    for bx, bw, bh in [(2, 28, 36), (34, 20, 48), (58, 34, 32), (96, 24, 56),
                       (166, 26, 46), (196, 32, 38), (232, 24, 52), (260, 28, 34),
                       (292, 20, 42)]:
        d.rectangle([x + bx, y + h - bh, x + bx + bw, y + h], fill=(40, 44, 70))
    # the damaged Dymer block, leaning, centre-left
    d.polygon([(x + 120, y + h), (x + 128, y + 62), (x + 150, y + 66), (x + 158, y + h)],
              fill=(70, 60, 60))
    for wx, wy in [(132, 72), (142, 74), (132, 84), (143, 86)]:
        d.rectangle([x + wx, y + wy, x + wx + 5, y + wy + 6], fill=(255, 220, 120))
    # fire at the block's base (tall flames, visible against the skyline)
    d.polygon([(x + 116, y + h), (x + 128, y + 76), (x + 138, y + h)], fill=(255, 130, 30))
    d.polygon([(x + 130, y + h), (x + 140, y + 80), (x + 150, y + h)], fill=(255, 200, 90))
    d.polygon([(x + 146, y + h), (x + 156, y + 78), (x + 164, y + h)], fill=(255, 130, 30))
    # smoke plume rising diagonally up-right from the block
    for sx, sy, sr in [(158, 52, 9), (172, 38, 11), (190, 24, 13), (210, 12, 14)]:
        d.ellipse([x + sx - sr, y + sy - sr, x + sx + sr, y + sy + sr],
                  fill=(120, 120, 130))
    # second, thinner plume drifting up-left
    for sx, sy, sr in [(118, 54, 7), (106, 42, 8), (94, 30, 9)]:
        d.ellipse([x + sx - sr, y + sy - sr, x + sx + sr, y + sy + sr],
                  fill=(100, 100, 115))
    # embers
    for ex, ey in [(130, 80), (145, 70), (160, 60), (125, 66)]:
        d.ellipse([x + ex - 2, y + ey - 2, x + ex + 2, y + ey + 2], fill=(255, 140, 40))


def art_bahrain(img, d, x, y, w, h):
    # Gulf night: radar domes and a Patriot launcher on the shore spit,
    # missile arcs across the sky, fire at the industrial site, a ship.
    d.rectangle([x, y, x + w, y + h * 0.58], fill=(24, 60, 110))
    d.rectangle([x, y + h * 0.58, x + w, y + h], fill=(16, 40, 80))
    d.ellipse([x + w - 52, y + 8, x + w - 26, y + 34], fill=(250, 228, 180))
    # shore spit, bottom-left
    d.polygon([(x, y + h), (x, y + 72), (x + 120, y + 78), (x + 142, y + h)],
              fill=(50, 48, 40))
    # radar domes on the spit
    for rx, rr, ry in [(28, 17, 62), (78, 13, 68)]:
        d.ellipse([x + rx - rr, y + ry - rr, x + rx + rr, y + ry + rr],
                  fill=(220, 220, 230), outline=INK, width=1)
        d.line([x + rx, y + ry - rr, x + rx, y + ry - rr - 8], fill=(220, 220, 230),
               width=2)
    # Patriot launcher: box + four angled tubes
    d.rectangle([x + 96, y + 84, x + 132, y + 96], fill=(30, 34, 44))
    for tx in [100, 108, 116, 124]:
        d.line([x + tx, y + 84, x + tx + 10, y + 66], fill=(30, 34, 44), width=4)
    # missile arcs (red trails) across the sky
    d.arc([x + 140, y + 6, x + 250, y + 70], start=200, end=340, fill=(255, 80, 50),
          width=3)
    d.arc([x + 170, y + 22, x + 290, y + 86], start=210, end=330, fill=(255, 140, 60),
          width=2)
    d.arc([x + 110, y + 2, x + 200, y + 56], start=200, end=330, fill=(255, 100, 70),
          width=2)
    # fire at the industrial site (left) + smoke column
    for a in range(8):
        ang = a * math.pi / 4
        d.line([x + 52, y + 82, x + 52 + 14 * math.cos(ang),
                y + 82 + 14 * math.sin(ang)], fill=(255, 130, 30), width=2)
    d.ellipse([x + 47, y + 77, x + 57, y + 87], fill=(255, 200, 90))
    for sx, sy, sr in [(52, 62, 8), (58, 48, 10), (66, 34, 11)]:
        d.ellipse([x + sx - sr, y + sy - sr, x + sx + sr, y + sy + sr],
                  fill=(120, 120, 130))
    # ship silhouette (Fifth Fleet), bottom-right
    d.rectangle([x + 205, y + 84, x + 300, y + 94], fill=(20, 24, 40))
    d.rectangle([x + 230, y + 72, x + 258, y + 84], fill=(20, 24, 40))
    d.line([x + 244, y + 72, x + 244, y + 60], fill=(20, 24, 40), width=2)
    # second, smaller ship mid-frame + more wave lines
    d.rectangle([x + 150, y + 88, x + 196, y + 95], fill=(20, 24, 40))
    d.rectangle([x + 166, y + 80, x + 182, y + 88], fill=(20, 24, 40))
    for wx, wy in [(170, 66), (220, 72), (270, 68), (185, 90), (250, 96),
                   (200, 78), (280, 92), (160, 74)]:
        d.line([x + wx, y + wy, x + wx + 18, y + wy], fill=(140, 170, 210), width=2)

# ------------------------------------------------- tile illustrations (185x48)
# v6: v3's real illustrated scenes, rank-5 style — the big anchor
# (28-32px) is overlaid on the scene with a 2px contrasting stroke, so
# it reads at 300px while the scene still reads as a scene. Each scene
# is drawn so its top-left corner (where the anchor sits) contrasts with
# the anchor colour. Anchor zone: art top-left ~120x33px.
def art_tile_benghazi(img, d, x, y, w, h):
    # Benghazi: capsized red warship in a dark strait, smoke, a small
    # drone boat. Anchor SUNK is white on the dark stormy sky.
    d.rectangle([x, y, x + w, y + 22], fill=(38, 52, 78))
    d.rectangle([x, y + 22, x + w, y + h], fill=(24, 60, 110))
    # grey smoke above the wreck
    for sx, sy, sr in [(118, 10, 6), (130, 6, 7), (142, 11, 5)]:
        d.ellipse([x + sx - sr, y + sy - sr, x + sx + sr, y + sy + sr],
                  fill=(150, 150, 160))
    # capsized hull: red, tilted, mostly submerged, bow up right
    d.polygon([(x + 92, y + 34), (x + 118, y + 26), (x + 158, y + 30),
               (x + 150, y + 40), (x + 100, y + 42)], fill=(170, 40, 30))
    d.polygon([(x + 118, y + 26), (x + 128, y + 18), (x + 140, y + 22),
               (x + 132, y + 28)], fill=(230, 230, 230))
    # flame at the waterline + orange glow
    d.polygon([(x + 138, y + 40), (x + 146, y + 28), (x + 154, y + 40)],
              fill=(255, 130, 30))
    d.ellipse([x + 140, y + 32, x + 150, y + 40], fill=(255, 200, 90))
    # small grey drone boat, left
    d.rectangle([x + 52, y + 34, x + 72, y + 40], fill=(90, 95, 105))
    d.line([x + 62, y + 34, x + 62, y + 26], fill=(90, 95, 105), width=2)
    # wave lines
    for wx, wy in [(20, 30), (60, 42), (120, 44), (160, 26)]:
        d.line([x + wx, y + wy, x + wx + 16, y + wy], fill=(140, 170, 210), width=2)


def art_tile_house(img, d, x, y, w, h):
    # Capitol: light sky, white dome and columns right of centre, two rows
    # of red/blue seat dots along the bottom. Anchor 258 is navy on light.
    d.rectangle([x, y, x + w, y + h], fill=(228, 236, 244))
    # dome: half-ellipse + drum + columns, centre-right
    d.pieslice([x + 118, y + 2, x + 168, y + 34], start=180, end=360,
               fill=(255, 255, 255))
    d.rectangle([x + 122, y + 18, x + 164, y + 34], fill=(240, 240, 240))
    for cx in [126, 136, 146, 156]:
        d.rectangle([x + cx, y + 20, x + cx + 4, y + 34], fill=(200, 205, 210))
    d.rectangle([x + 110, y + 34, x + 176, y + 38], fill=(210, 214, 220))
    d.rectangle([x + 104, y + 38, x + 182, y + 42], fill=(190, 194, 200))
    # flag on the dome
    d.line([x + 143, y + 2, x + 143, y - 8], fill=(90, 90, 90), width=1)
    # seat dots: blue then red, two rows along the bottom
    for i in range(10):
        col = (29, 53, 87) if i % 2 == 0 else (200, 50, 40)
        d.ellipse([x + 14 + i * 9, y + 40, x + 20 + i * 9, y + 46], fill=col)
    for i in range(8):
        col = (200, 50, 40) if i % 2 == 0 else (29, 53, 87)
        d.ellipse([x + 100 + i * 9, y + 43, x + 106 + i * 9, y + 47], fill=col)


def art_tile_wemby(img, d, x, y, w, h):
    # Basketball: light wood court, white lines, hoop right, ball left.
    # Anchor 50 PTS is ink on the light wood.
    d.rectangle([x, y, x + w, y + h], fill=(205, 175, 125))
    # court lines: centre circle arc + key
    d.arc([x - 30, y + 4, x + 30, y + 44], start=270, end=90, fill=(255, 255, 255),
          width=2)
    d.line([x + 120, y, x + 120, y + h], fill=(255, 255, 255), width=2)
    d.rectangle([x + 120, y + 14, x + 150, y + 34], outline=(255, 255, 255), width=2)
    # hoop: pole + backboard + orange rim + net, right
    d.line([x + 168, y + 6, x + 168, y + 34], fill=(60, 60, 60), width=3)
    d.rectangle([x + 160, y + 6, x + 176, y + 20], fill=(255, 255, 255),
                outline=(60, 60, 60), width=1)
    d.ellipse([x + 152, y + 20, x + 168, y + 26], outline=(220, 100, 20), width=3)
    d.line([x + 154, y + 26, x + 158, y + 34], fill=(255, 255, 255), width=1)
    d.line([x + 166, y + 26, x + 162, y + 34], fill=(255, 255, 255), width=1)
    # basketball, bottom-left below the anchor, with seams
    d.ellipse([x + 22, y + 30, x + 38, y + 46], fill=(220, 110, 30),
              outline=(120, 60, 10), width=1)
    d.line([x + 22, y + 38, x + 38, y + 38], fill=(120, 60, 10), width=1)
    d.arc([x + 26, y + 30, x + 38, y + 46], start=270, end=90, fill=(120, 60, 10),
          width=1)


def art_tile_alcaraz(img, d, x, y, w, h):
    # Tennis: light blue hard court, white service lines, net across the
    # middle, yellow ball. Anchor 6-2 7-6 is ink on the light court.
    d.rectangle([x, y, x + w, y + h], fill=(168, 205, 228))
    d.rectangle([x, y, x + w, y + 8], fill=(140, 185, 215))
    # service lines
    d.line([x + 10, y + 14, x + w - 10, y + 14], fill=(255, 255, 255), width=2)
    d.line([x + 10, y + 40, x + w - 10, y + 40], fill=(255, 255, 255), width=2)
    d.line([x + 92, y + 14, x + 92, y + 40], fill=(255, 255, 255), width=2)
    # net: dark band + white top tape across the middle
    d.rectangle([x, y + 22, x + w, y + 30], fill=(40, 50, 60))
    d.rectangle([x, y + 22, x + w, y + 25], fill=(255, 255, 255))
    # tennis ball, top-right, with a white curve seam
    d.ellipse([x + 148, y + 6, x + 162, y + 20], fill=(220, 230, 60),
              outline=(140, 150, 30), width=1)
    d.arc([x + 150, y + 8, x + 162, y + 20], start=300, end=120, fill=(255, 255, 255),
          width=1)


def art_tile_liverpool(img, d, x, y, w, h):
    # Football: dark green pitch with mowing stripes, white lines, goal
    # right, ball left. Anchor 4-0 is white on the dark pitch.
    d.rectangle([x, y, x + w, y + h], fill=(28, 95, 48))
    for sx in range(0, w, 36):
        d.rectangle([x + sx, y, x + sx + 18, y + h], fill=(35, 110, 55))
    # touchline + centre circle arc
    d.line([x + 8, y + 6, x + w - 8, y + 6], fill=(255, 255, 255), width=2)
    d.line([x + 8, y + h - 6, x + w - 8, y + h - 6], fill=(255, 255, 255), width=2)
    d.arc([x - 14, y + 10, x + 26, y + 38], start=270, end=90, fill=(255, 255, 255),
          width=2)
    # goal: posts + net, right
    d.rectangle([x + 158, y + 10, x + 180, y + 34], outline=(255, 255, 255), width=2)
    for gx in range(162, 180, 6):
        d.line([x + gx, y + 10, x + gx, y + 34], fill=(255, 255, 255), width=1)
    # ball, bottom-left below the anchor
    d.ellipse([x + 24, y + 34, x + 36, y + 46], fill=(255, 255, 255),
              outline=(30, 30, 30), width=1)
    d.ellipse([x + 28, y + 38, x + 32, y + 42], fill=(30, 30, 30))


def art_tile_verstappen(img, d, x, y, w, h):
    # Formula 1: dark asphalt, red/white kerb along the bottom, a low red
    # F1 car centre, chequered flag top-right. Anchor 1st is white on dark.
    d.rectangle([x, y, x + w, y + h], fill=(38, 38, 46))
    # kerb: alternating red/white blocks along the bottom edge
    for i in range(12):
        col = (200, 50, 40) if i % 2 == 0 else (255, 255, 255)
        d.rectangle([x + i * 16, y + h - 7, x + i * 16 + 16, y + h], fill=col)
    # chequered flag, top-right
    for r in range(2):
        for c in range(4):
            col = (255, 255, 255) if (r + c) % 2 == 0 else (20, 20, 20)
            d.rectangle([x + 150 + c * 8, y + 4 + r * 8,
                         x + 158 + c * 8, y + 12 + r * 8], fill=col)
    # F1 car: low sleek body, rear wing, two black wheels — shifted right
    # so the rear wing clears the "1st" anchor
    d.polygon([(x + 58, y + 30), (x + 80, y + 22), (x + 130, y + 22),
               (x + 148, y + 30), (x + 58, y + 30)], fill=(200, 40, 30))
    d.rectangle([x + 54, y + 18, x + 62, y + 30], fill=(200, 40, 30))
    d.ellipse([x + 68, y + 28, x + 84, y + 40], fill=(15, 15, 15))
    d.ellipse([x + 122, y + 28, x + 138, y + 40], fill=(15, 15, 15))
    d.ellipse([x + 74, y + 32, x + 78, y + 36], fill=(120, 120, 120))
    d.ellipse([x + 128, y + 32, x + 132, y + 36], fill=(120, 120, 120))
    # speed lines behind the car
    for sy in [24, 30, 36]:
        d.line([x + 8, y + sy, x + 38, y + sy], fill=(150, 150, 160), width=2)


def art_tile_markets(img, d, x, y, w, h):
    # Markets: light board, faint grid, a red line falling left to right
    # with candlesticks and a down arrow. Anchor -3.7% is red on light.
    d.rectangle([x, y, x + w, y + h], fill=(245, 245, 240))
    for gy in [12, 24, 36]:
        d.line([x, y + gy, x + w, y + gy], fill=(220, 220, 210), width=1)
    for gx in [40, 80, 120, 160]:
        d.line([x + gx, y, x + gx, y + h], fill=(220, 220, 210), width=1)
    # candlesticks + falling line along the BOTTOM half, clear of the
    # anchor zone (top-left); the line no longer crosses the anchor text
    for cx, cy, ch, col in [(28, 30, 6, (46, 125, 50)), (62, 33, 6, (200, 50, 40)),
                            (96, 36, 6, (200, 50, 40)), (130, 39, 6, (200, 50, 40))]:
        d.rectangle([x + cx, y + cy, x + cx + 12, y + cy + ch], fill=col)
        d.line([x + cx + 6, y + cy - 4, x + cx + 6, y + cy + ch + 4], fill=col, width=1)
    # the falling line + down arrow at the end
    d.line([x + 8, y + 30, x + 175, y + 44], fill=(200, 50, 40), width=3)
    d.polygon([(x + 175, y + 44), (x + 163, y + 38), (x + 165, y + 47)], fill=(200, 50, 40))


def art_tile_westbank(img, d, x, y, w, h):
    # West Bank hillside: light sky, two tan hills, small white houses
    # with grey roofs, olive trees. Anchor 4 KILLED is red on light sky.
    d.rectangle([x, y, x + w, y + 26], fill=(218, 230, 240))
    d.polygon([(x, y + 26), (x + 70, y + 10), (x + 140, y + 26)], fill=(190, 175, 130))
    d.polygon([(x + 60, y + h), (x + 120, y + 18), (x + 185, y + h)], fill=(170, 155, 110))
    # houses on the hills
    for hx, hy, hw2 in [(20, 22, 16), (52, 16, 14), (130, 24, 16), (158, 20, 14)]:
        d.rectangle([x + hx, y + hy, x + hx + hw2, y + hy + 10], fill=(250, 250, 245))
        d.polygon([(x + hx, y + hy), (x + hx + hw2 // 2, y + hy - 6),
                   (x + hx + hw2, y + hy)], fill=(120, 120, 120))
    # olive trees: trunk + green crown
    for tx, ty in [(96, 30), (40, 34), (170, 32)]:
        d.line([x + tx, y + ty, x + tx, y + ty + 6], fill=(110, 80, 40), width=2)
        d.ellipse([x + tx - 6, y + ty - 6, x + tx + 6, y + ty + 2], fill=(90, 130, 70))
    # dirt road across the bottom
    d.line([x, y + 42, x + w, y + 38], fill=(150, 130, 95), width=3)


def art_tile_hk(img, d, x, y, w, h):
    # Hong Kong night: dark sky, tower silhouettes with lit windows, a
    # ballot box with a green check at the foot. Anchor 98.79% is white
    # on the dark sky.
    d.rectangle([x, y, x + w, y + h], fill=(25, 40, 80))
    for sx, sy in [(14, 8), (60, 6), (120, 10), (170, 6), (90, 14)]:
        d.ellipse([x + sx, y + sy, x + sx + 2, y + sy + 2], fill=(255, 255, 255))
    # towers, back to front
    for bx, bw, bh in [(8, 22, 30), (34, 18, 38), (56, 26, 26), (86, 20, 36),
                       (110, 24, 28), (138, 18, 40), (160, 22, 30)]:
        d.rectangle([x + bx, y + h - bh, x + bx + bw, y + h], fill=(16, 24, 48))
    # lit windows (a few yellow squares per tower)
    for wx, wy in [(14, 26), (22, 32), (40, 18), (44, 28), (64, 30), (70, 24),
                   (92, 22), (98, 32), (116, 28), (144, 20), (150, 30), (166, 26)]:
        d.rectangle([x + wx, y + wy, x + wx + 3, y + wy + 4], fill=(255, 220, 120))
    # ballot box + green check, bottom-centre on the skyline base
    d.rectangle([x + 78, y + h - 14, x + 100, y + h - 2], fill=(255, 255, 255),
                outline=(200, 50, 40), width=1)
    d.rectangle([x + 78, y + h - 14, x + 100, y + h - 10], fill=(200, 50, 40))
    d.line([x + 82, y + h - 7, x + 87, y + h - 3], fill=(46, 125, 50), width=2)
    d.line([x + 87, y + h - 3, x + 96, y + h - 12], fill=(46, 125, 50), width=2)


def art_tile_sparta(img, d, x, y, w, h):
    # Gulf of Finland: orange sunset sky, dark sea, a burning cargo ship
    # with containers, a small orange lifeboat. Anchor 16 SAVED is white
    # (with a dark stroke) on the sunset.
    d.rectangle([x, y, x + w, y + 28], fill=(238, 138, 58))
    d.rectangle([x, y + 28, x + w, y + h], fill=(28, 48, 78))
    d.ellipse([x + 150, y + 4, x + 172, y + 26], fill=(250, 220, 150))
    # ship: dark hull + stacked containers, centre-right
    d.polygon([(x + 78, y + 32), (x + 160, y + 32), (x + 152, y + 42),
               (x + 86, y + 42)], fill=(18, 22, 38))
    for cx, cc in [(88, (200, 50, 40)), (104, (29, 90, 160)), (120, (46, 125, 50)),
                   (136, (200, 50, 40))]:
        d.rectangle([x + cx, y + 22, x + cx + 14, y + 32], fill=cc)
    # flames on deck + smoke
    d.polygon([(x + 108, y + 32), (x + 114, y + 18), (x + 120, y + 32)],
              fill=(255, 130, 30))
    d.polygon([(x + 122, y + 32), (x + 128, y + 22), (x + 134, y + 32)],
              fill=(255, 200, 90))
    for sx, sy, sr in [(116, 12, 6), (126, 6, 7), (136, 12, 5)]:
        d.ellipse([x + sx - sr, y + sy - sr, x + sx + sr, y + sy + sr],
                  fill=(120, 120, 130))
    # lifeboat, left on the sea + wave lines
    d.ellipse([x + 22, y + 38, x + 46, y + 44], fill=(230, 120, 30))
    for wx, wy in [(60, 38), (120, 44), (160, 36), (20, 30)]:
        d.line([x + wx, y + wy, x + wx + 14, y + wy], fill=(140, 170, 210), width=2)

# ------------------------------------------------- story data (35, Sunday 22 Nov 2026)
# v6: v1.1's verified facts, verbatim — no story, number or date changed.
# Only the COP31 stat chip is back to v1.1's full text ("48h overtime ·
# longest COP"): at 122px art height the chip sits below the NO DEAL
# stamp instead of colliding with it, so the short form v3 needed is
# no longer necessary.
HEROES = [
    dict(num=1, kicker="186 DRONES", stat="161 shot down \u00b7 18 sites hit",
         loc="1 KYIV, UKRAINE \u00b7 WAR",
         head="Russia fires 186 drones in one night",
         body="72 were jet-powered; a block in Dymer falls, 14 missing. (Ukrainian Air Force)",
         badge="OFFICIAL", badge_color=GREEN, art=art_drones),
    dict(num=2, kicker="COP31: NO DEAL", stat="48h overtime \u00b7 longest COP",
         loc="2 ANTALYA, T\u00dcRKIYE \u00b7 CLIMATE",
         head="Climate talks collapse in Antalya",
         body="EU and 130+ nations reject a text with no fossil-fuel phase-out. (Reuters, AP)",
         badge="CONFIRMED", badge_color=TEAL, art=art_cop31),
    dict(num=3, kicker="IRAN: STRIKES", stat="2 US radars claimed",
         loc="3 MANAMA, BAHRAIN \u00b7 MIDDLE EAST",
         head="Iran claims strikes on US bases",
         body="IRGC says it hit two Patriot radars; Bahrain reports a plant ablaze, 2 hurt. (Reuters, IRNA)",
         badge="CLAIM", badge_color=AMBER, art=art_bahrain),
]

# v6 tiles: v3's scenes + giant anchors, verbatim. The separate loc line
# is gone — the story number prefixes the red kicker bar
# ("4 BENGHAZI: SUNK") — and the badge sits bottom-right ON the art
# (rank 2 style). Anchors are 26-32px with a 2px contrasting stroke.
TILES = [
    dict(num=4, kicker="BENGHAZI: SUNK",
         anchor="SUNK", asize=30, art_fill=WHITE, art_stroke=INK,
         art=art_tile_benghazi,
         head="Russian warship sunk off Libya",
         body="Sea drones sank a corvette; Zelenskyy: Kyiv did it",
         badge="REPORTED", badge_color=AMBER),
    dict(num=5, kicker="HOUSE: 258",
         anchor="258", asize=32, art_fill=NAVY, art_stroke=WHITE,
         art=art_tile_house,
         head="Democrats take House, 258 seats",
         body="Recount win in N. Carolina gives them 258 seats. (AP)",
         badge="CONFIRMED", badge_color=TEAL),
    dict(num=6, kicker="WEMBY: 50 PTS",
         anchor="50 PTS", asize=30, art_fill=INK, art_stroke=WHITE,
         art=art_tile_wemby,
         head="Wembanyama drops 50",
         body="Spurs beat Pelicans 114\u201391; 19 boards, 5 blocks. (NBA)",
         badge="OFFICIAL", badge_color=GREEN),
    dict(num=7, kicker="ALCARAZ: 6\u20132, 7\u20136",
         anchor="6\u20132 7\u20136", asize=26, art_fill=INK, art_stroke=WHITE,
         art=art_tile_alcaraz,
         head="Alcaraz wins first ATP Finals",
         body="Beats No. 1 Zverev; 5\u20130 in Turin, $5.17m. (ATP)",
         badge="OFFICIAL", badge_color=GREEN),
    dict(num=8, kicker="LIVERPOOL 4\u20130",
         anchor="4\u20130", asize=32, art_fill=WHITE, art_stroke=INK,
         art=art_tile_liverpool,
         head="Liverpool thrash 10-man United",
         body="Pochettino's debut ends 4\u20130; Yoro off in 8'. (Reuters)",
         badge="OFFICIAL", badge_color=GREEN),
    dict(num=9, kicker="VERSTAPPEN WINS",
         anchor="1st", asize=32, art_fill=WHITE, art_stroke=INK,
         art=art_tile_verstappen,
         head="Verstappen wins Las Vegas GP",
         body="Third Vegas win; +0.639 over Norris. (F1)",
         badge="OFFICIAL", badge_color=GREEN),
    dict(num=10, kicker="S&P \u22123.7%",
         anchor="\u22123.7%", asize=30, art_fill=RED, art_stroke=WHITE,
         art=art_tile_markets,
         head="Stocks fall as AI sell-off deepens",
         body="S&P 500 \u22123.7%; Nikkei \u22125.06%. (Reuters)",
         badge="CONFIRMED", badge_color=TEAL),
    dict(num=11, kicker="WEST BANK: ATTACKS",
         anchor="4 KILLED", asize=28, art_fill=RED, art_stroke=WHITE,
         art=art_tile_westbank,
         head="Settler attacks called 'terrorism'",
         body="Eisenkot speaks out; 4 killed in Gaza. (AP)",
         badge="REPORTED", badge_color=AMBER),
    dict(num=12, kicker="HK: 98.79%",
         anchor="98.79%", asize=28, art_fill=WHITE, art_stroke=INK,
         art=art_tile_hk,
         head="Hong Kong votes in record turnout",
         body="98.79% pick 723 seats. (China Daily)",
         badge="OFFICIAL", badge_color=GREEN),
    dict(num=13, kicker="SPARTA II: ADRIFT",
         anchor="16 SAVED", asize=28, art_fill=WHITE, art_stroke=INK,
         art=art_tile_sparta,
         head="Russian cargo ship still burning",
         body="Hit by 2 drones; 16 crew evacuated. (Finnish officials)",
         badge="REPORTED", badge_color=AMBER),
]

INDEX = [
    (14, "Dymer block falls; 3 killed, 14 missing"),
    (15, "Ukraine hits Russian base in Krasnodar"),
    (16, "Russian missiles land in Poland"),
    (17, "Poland: 'twice tried to kill' rapper"),
    (18, "Russia grasps US security offer"),
    (19, "Paolo Bulgari dies at 89"),
    (20, "Iran claims 2 tankers hit near Hormuz"),
    (21, "Iran FM: Hormuz reopening 'not difficult'"),
    (22, "Trump dares Iran to break blockade"),
    (23, "Trump, Putin, Xi meet; back fossil fuels"),
    (24, "ICE protest in Gilroy; 2 seized at Sea-Tac"),
    (25, "Army to detonate lead azide in Iowa"),
    (26, "AI bailout floated as boom unravels"),
    (27, "St. Johns River breaks 73-year record"),
    (28, "Cartel leader captured; 11 dead"),
    (29, "Nepal PM visits India for Modi talks"),
    (30, "India, China hold Arunachal talks"),
    (31, "Toxic alcohol kills 19 in Manipur"),
    (32, "India 720/9 vs New Zealand, lead 352"),
    (33, "Thai court upholds defamation verdict"),
    (34, "Cikande factory fire: 3 dead, 36 missing"),
    (35, "Nigeria boat toll rises to 26"),
]

SOURCES = ("AFP \u00b7 REUTERS \u00b7 AP \u00b7 AL JAZEERA \u00b7 ATP \u00b7 NBA \u00b7 F1 \u00b7 UKRAINIAN AIR FORCE \u00b7 "
           "IRNA \u00b7 CHINA DAILY \u00b7 HONG KONG REO \u00b7 KYIV INDEPENDENT")

NUMBERS = [
    ("186", "DRONES FIRED AT", "UKRAINE OVERNIGHT"),
    ("161", "DRONES SHOT DOWN", "56 JET-POWERED"),
    ("48h", "COP31 OVERTIME", "LONGEST COP EVER"),
    ("258", "DEMOCRAT HOUSE SEATS", "BIGGEST SINCE 1992"),
    ("98.79%", "HONG KONG TURNOUT", "RECORD, 5,640 VOTERS"),
    ("6\u20132, 7\u20136", "ALCARAZ BEATS ZVEREV", "FIRST ATP FINALS TITLE"),
]

# region counts, must sum to 35 (matches the story list above)
REGIONS = [
    ("CLIMATE", 1, (46, 125, 50)),
    ("EUROPE", 8, (46, 90, 172)),
    ("MIDDLE EAST", 5, (200, 50, 40)),
    ("AMERICAS", 9, (14, 124, 107)),
    ("ASIA-PACIFIC", 6, (194, 94, 0)),
    ("AFRICA", 2, (123, 75, 166)),
    ("SPORT & SPACE", 4, (107, 107, 107)),
]

# map pins for v1.1's map geometry: map pasted at (28, 771), 340x123.
# v6 pastes a bigger map at (28, 781), 360x130 — the pins are rescaled
# from these base coordinates in render(), so the geography stays true.
# 1 Kyiv (drones), 2 Antalya (COP31), 3 Bahrain, 4 Benghazi,
# 5 Washington, 6 San Antonio, 7 Turin, 8 Liverpool,
# 10 New York, 11 West Bank, 12 Hong Kong, 13 Gulf of Finland
PINS_BASE = [
    (1, 234, 790), (2, 224, 810), (3, 250, 812), (4, 202, 818),
    (5, 120, 806), (6, 110, 812), (7, 212, 800), (8, 178, 782),
    (10, 134, 796), (11, 238, 826), (12, 306, 818), (13, 210, 786),
]
PIN_MAP_X0, PIN_MAP_Y0, PIN_MAP_W, PIN_MAP_H = 28, 771, 340, 123

# UTC timeline (v2): the day's beats in the order they happened.
# Times are the hour each story was first reported (UTC); the strip is
# schematic (dots evenly spaced), like ranks 1, 2, 5 and 49.
TIMELINE = [
    ("01:00", "HK polls open"),
    ("03:00", "COP31 objections close"),
    ("05:30", "Verstappen wins"),
    ("06:00", "COP31 approval due"),
    ("08:00", "161 of 186 downed"),
    ("18:00", "House majority record"),
    ("20:43", "Alcaraz wins"),
]

def index_item(d, x, y, num, text, max_w):
    """One numbered index line at 13px; every item measured to fit one line."""
    f = F(SANS, 13)
    fb = F(SANS_B, 13)
    d.text((x, y), f"{num} ", font=fb, fill=RED)
    d.text((x + d.textlength(f"{num} ", font=fb), y), text, font=f, fill=INK)


def render():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    d.rectangle([6, 6, W - 7, H - 7], outline=INK, width=2)
    problems = []

    def check(cond, msg):
        if not cond:
            problems.append(msg)

    # top bar
    d.rectangle([28, 10, W - 28, 30], fill=CRIMSON)
    d.text((34, 13), "THE WORLD IN ONE DAY", font=F(SANS_B, 14), fill=(255, 255, 255))
    d.text((W - 34, 13), "35 STORIES \u00b7 7 REGIONS \u00b7 EVERY ONE DATED SUNDAY 22 NOVEMBER 2026",
           font=F(SANS_B, 12), fill=(255, 255, 255), anchor="rt")

    # giant date masthead (auto-fit, cap 76px — the 30px timeline strip is
    # paid for here and in the numbers strip, not in the hero height)
    mast = "Sunday 22 November 2026"
    msize = 76
    while msize > 60:
        mf = ImageFont.truetype(MASTHEAD, msize)
        if d.textlength(mast, font=mf) <= 960:
            break
        msize -= 2
    d.text((512, 32), mast, font=mf, fill=INK, anchor="mt")
    check(msize >= 70, f"masthead shrank to {msize}px")
    d.text((512, 108), "186 drones over Ukraine \u00b7 COP31 collapses in Antalya \u00b7 Iran claims Bahrain strikes",
           font=F(SERIF_I, 17), fill=INK, anchor="mt")

    # numbers strip: 6 verified Sunday figures (numbers 28px, was 30)
    ny = 136
    d.line([28, ny - 6, W - 28, ny - 6], fill=INK, width=1)
    colw = (W - 56) // 6
    for i, (num, l1, l2) in enumerate(NUMBERS):
        cx = 28 + i * colw + colw // 2
        d.text((cx, ny), num, font=F(MASTHEAD_NUM, 28), fill=RED, anchor="mt")
        check(d.textlength(l1, font=F(SANS_B, 11)) <= colw, f"num strip l1 overflow: {l1}")
        check(d.textlength(l2, font=F(SANS_B, 11)) <= colw, f"num strip l2 overflow: {l2}")
        d.text((cx, ny + 30), l1, font=F(SANS_B, 11), fill=INK, anchor="mt")
        d.text((cx, ny + 43), l2, font=F(SANS_B, 11), fill=INK, anchor="mt")
        if i:
            d.line([28 + i * colw, ny, 28 + i * colw, ny + 54], fill=GREY, width=1)
    d.line([28, ny + 54, W - 28, ny + 54], fill=INK, width=1)

    # region counts bar (widths proportional to counts, total 35;
    # narrow segments get a 62px minimum so their 11px labels fit)
    ry = 194
    total = sum(c for _, c, _ in REGIONS)
    assert total == 35, total
    minw = 62
    flex = (W - 56) - minw * len(REGIONS)
    flex_total = sum(max(c - 1, 0) for _, c, _ in REGIONS)
    rx = 28
    for name, count, color in REGIONS:
        segw = minw + flex * max(count - 1, 0) / flex_total
        d.rectangle([rx, ry, rx + segw, ry + 15], fill=color)
        d.text((rx + segw / 2, ry + 2), f"{name} {count}", font=F(SANS_B, 11),
               fill=(255, 255, 255), anchor="mt")
        rx += segw

    # UTC timeline strip (v2): 7 timed beats, schematic dots on a rule.
    ty = 213
    d.line([28, ty + 14, W - 28, ty + 14], fill=GREY, width=1)
    for i, (tm, lab) in enumerate(TIMELINE):
        cx = 80 + i * 144
        check(d.textlength(lab, font=F(SANS, 11)) <= 140, f"timeline label overflow: {lab}")
        d.ellipse([cx - 4, ty + 10, cx + 4, ty + 18], fill=RED)
        d.text((cx, ty + 1), tm, font=F(SANS_B, 12), fill=NAVY, anchor="mt")
        d.text((cx, ty + 20), lab, font=F(SANS, 11), fill=INK, anchor="mt")

    # 3 big heroes (art 122px, card 232px — v1.1 had 130/240, v2/v3 had
    # 100/210; v6 keeps the tall heroes and pays for the timeline above)
    hy, hh, hart = 248, 232, 122
    hw = (W - 56 - 2 * 10) // 3
    for i, hro in enumerate(HEROES):
        x = 28 + i * (hw + 10)
        y = hy
        d.rectangle([x, y, x + hw, y + hh], outline=INK, width=1)
        hro["art"](img, d, x + 1, y + 1, hw - 2, hart)
        kicker_label(d, x + 8, y + 8, hro["kicker"], 17)
        stat_chip(d, x + 8, y + hart - 26, hro["stat"])
        badge(d, x + hw - 8, y + 8, hro["badge"], hro["badge_color"])
        check(len(wrap(d, hro["head"], F(SERIF_B, 22), hw - 16)) <= 2,
              f"hero {hro['num']} headline >2 lines")
        check(len(wrap(d, hro["body"], F(SANS, 13), hw - 16)) <= 2,
              f"hero {hro['num']} body >2 lines")
        d.text((x + 8, y + hart + 8), hro["loc"], font=F(SANS_B, 12), fill=RED)
        block(d, x + 8, y + hart + 22, hro["head"], F(SERIF_B, 22), hw - 16, 24, max_lines=2)
        block(d, x + 8, y + hart + 74, hro["body"], F(SANS, 13), hw - 16, 16, max_lines=2)

    # 10 tiles (4-13), 2 rows x 5 — v3: a real illustrated scene (48px)
    # strip WITH the big anchor kept, overlaid on the scene (rank-5
    # style) in a contrasting colour with a 2px stroke. The story number
    # prefixes the red kicker bar; the status badge sits bottom-right ON
    # the art (rank 2 style); headline + body below as in v2.
    tw = (W - 56 - 4 * 8) // 5
    th = 136
    for i, t in enumerate(TILES):
        r, c = divmod(i, 5)
        x = 28 + c * (tw + 8)
        y = 484 + r * (th + 5)
        d.rectangle([x, y, x + tw, y + th], outline=INK, width=1)
        # red kicker bar with the story number prefixed
        kb = f"{t['num']} {t['kicker']}"
        check(d.textlength(kb, font=F(SANS_B, 11)) <= tw - 8, f"tile {t['num']} kicker overflow")
        d.rectangle([x, y, x + tw, y + 17], fill=RED)
        d.text((x + 6, y + 3), kb, font=F(SANS_B, 11), fill=(255, 255, 255))
        # illustrated scene strip (48px), full tile width inside the border
        t["art"](img, d, x + 1, y + 17, tw - 2, 48)
        # big anchor overlaid on the scene, top-left, 2px contrasting
        # stroke so it reads at 300px on any background
        check(d.textlength(t["anchor"], font=F(SANS_B, t["asize"])) <= tw - 16,
              f"tile {t['num']} anchor overflow: {t['anchor']}")
        d.text((x + 8, y + 20), t["anchor"], font=F(SANS_B, t["asize"]),
               fill=t["art_fill"], stroke_width=2, stroke_fill=t["art_stroke"])
        # status badge bottom-right on the art
        badge(d, x + tw - 6, y + 48, t["badge"], t["badge_color"])
        check(len(wrap(d, t["head"], F(SANS_B, 18), tw - 12)) <= 2,
              f"tile {t['num']} headline >2 lines")
        check(len(wrap(d, t["body"], F(SANS, 12), tw - 12)) <= 2,
              f"tile {t['num']} body >2 lines")
        block(d, x + 6, y + 67, t["head"], F(SANS_B, 18), tw - 12, 18, max_lines=2)
        block(d, x + 6, y + 105, t["body"], F(SANS, 12), tw - 12, 13, max_lines=2)

    # map + numbered index (13px, index leading tightened to 14 for the
    # certainty legend line below)
    my = 765
    d.text((28, my), "WHERE IT HAPPENED", font=F(SANS_B, 13), fill=INK)
    d.text((W - 28, my), "ALSO ON SUNDAY 22 NOVEMBER \u2014 22 MORE STORIES",
           font=F(SANS_B, 13), fill=RED, anchor="rt")
    # bigger map: 360x130 (was 340x123); pins rescaled from the v1.1 base
    map_w, map_h, map_x, map_y = 360, 130, 28, 781
    map_img = Image.open(MAP_PATH).resize((map_w, map_h), Image.LANCZOS)
    img.paste(map_img, (map_x, map_y))
    d.rectangle([map_x, map_y, map_x + map_w, map_y + map_h], outline=INK, width=1)
    for num, px, py in PINS_BASE:
        nx = map_x + (px - PIN_MAP_X0) * map_w / PIN_MAP_W
        ny2 = map_y + (py - PIN_MAP_Y0) * map_h / PIN_MAP_H
        d.ellipse([nx - 8, ny2 - 8, nx + 8, ny2 + 8], fill=RED,
                  outline=(255, 255, 255), width=1)
        d.text((nx, ny2), str(num), font=F(SANS_B, 11), fill=(255, 255, 255),
               anchor="mm")
    colw2 = (W - 28 - (map_x + map_w + 8) - 8) // 2
    for i, (num, text) in enumerate(INDEX):
        col, row = divmod(i, 11)
        x = map_x + map_w + 8 + col * (colw2 + 8)
        y = map_y + row * 14
        iw = d.textlength(f"{num} ", font=F(SANS_B, 13)) + d.textlength(text, font=F(SANS, 13))
        check(iw <= colw2, f"index {num} overflow: {iw:.0f} > {colw2}")
        index_item(d, x, y, num, text, colw2)

    # region-colour key under the map (rank 5 style) — 13px pitch for all
    # four bottom lines (key rows 914/927, sources 940, legend 953) so no
    # two lines touch
    map_key(d, 28, 914, [(n, c) for n, _, c in REGIONS[:4]])
    map_key(d, 28, 927, [(n, c) for n, _, c in REGIONS[4:]])

    # one SOURCES line for the index stories (per-item sources removed)
    _sw = d.textlength("SOURCES: ", font=F(SANS_B, 11))
    _tw = _sw + d.textlength(SOURCES, font=F(SANS, 11))
    _sx = 512 - _tw / 2
    check(_tw <= 968, f"sources line overflow: {_tw:.0f}")
    d.text((_sx, 940), "SOURCES: ", font=F(SANS_B, 11), fill=INK)
    d.text((_sx + _sw, 940), SOURCES, font=F(SANS, 11), fill=INK)

    # certainty legend (v2): what each badge means, in words
    d.text((512, 953),
           "CERTAINTY \u2014 OFFICIAL = on the record \u00b7 CONFIRMED = 2+ outlets \u00b7 REPORTED = one outlet \u00b7 CLAIM = one side\u2019s account",
           font=F(SANS, 11), fill=INK, anchor="mt")

    # DATE CHECK footer (wrapped: label inline on line 1, body on lines 1-2)
    dy = 966
    d.rectangle([28, dy, W - 28, dy + 30], outline=RED, width=2)
    lab = "DATE CHECK \u2014 "
    lab_w = d.textlength(lab, font=F(SANS_B, 11))
    d.text((34, dy + 2), lab, font=F(SANS_B, 11), fill=RED)
    dc = ("Left out as other days\u2019 news: the 400-drone barrage of 19\u201320 Nov \u2014 tonight\u2019s "
          "was 186, not 400; El Chapo (20 Nov); the Peru quake (20 Nov); BepiColombo (21 Nov); "
          "the Nvidia probe (20 Nov); the Myanmar verdict (19 Nov); Houthi missiles over Riyadh (21 Nov).")
    words = dc.split()
    lines, cur, first = [], "", True
    for wd in words:
        maxw = (990 - 34 - lab_w) if first else (990 - 34)
        t = (cur + " " + wd).strip()
        if d.textlength(t, font=F(SANS, 11)) <= maxw:
            cur = t
        else:
            lines.append(cur)
            cur = wd
            first = False
    if cur:
        lines.append(cur)
    check(len(lines) == 2, f"DATE CHECK wrapped to {len(lines)} lines, expected 2")
    d.text((34 + lab_w, dy + 2), lines[0], font=F(SANS, 11), fill=INK)
    if len(lines) > 1:
        d.text((34, dy + 15), lines[1], font=F(SANS, 11), fill=INK)

    # colophon
    d.text((512, 1000),
           "Press time 24:00 UTC \u00b7 Every story here happened, or was first reported, on Sunday 22 November 2026. Index sources above \u00b7 original drawings",
           font=F(SANS, 11), fill=GREY, anchor="mt")
    check(1000 + 11 <= 1017, "colophon crosses the bottom border")

    return img, msize, problems


def save_both(img):
    """Save RGB (max compression) and a 256-colour palette version; the
    smaller of the two becomes the entry image (tie-break is bytes)."""
    img.save(OUT_RGB, optimize=True, compress_level=9)
    pal = img.convert("P", palette=Image.ADAPTIVE, colors=256)
    pal.save(OUT_PAL, optimize=True)
    srgb = os.path.getsize(OUT_RGB)
    spal = os.path.getsize(OUT_PAL)
    print("rgb bytes:", srgb, "| palette bytes:", spal)
    return srgb, spal


if __name__ == "__main__":
    im, _ms, probs = render()
    print("masthead size:", _ms)
    print("OVERFLOWS:", len(probs))
    for p in probs:
        print("  OVERFLOW:", p)
    save_both(im)
    print("saved", im.size)
    if probs:
        raise SystemExit(1)
