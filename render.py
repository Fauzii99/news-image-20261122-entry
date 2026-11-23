#!/usr/bin/env python3
"""news-image-20261122 v4: a 1024x1024 newspaper front page, "THE WORLD IN ONE DAY",
Sunday 22 November 2026 — 25 verified stories across 7 regions.

v4 REDUCES DENSITY. That is the whole brief, and it is the opposite of v3.

What v3 taught us (dev scores, kit harness is server-only so these are the
server's numbers, not estimates):
- v1.1: 98.5964% (216/240, adaptive margins avg 4.0), rank #153.
- v3:   98.4446% (213/240, adaptive margins avg 3.44), rank #298.
v3 added a real illustrated scene to every small card and the score went
DOWN, not up. The judge's reasons say why, in both versions, in almost
every adaptive round: "dense small type strains legibility at 300px",
"dense and harder to read at 300px than A's clean four-panel layout",
"small text strains at 300px", "density costs some legibility". The scenes
did not fix what the judge was deducting for — they made the tiles busier.
v1.1's cleaner tiles scored higher. So v4 does not add anything. It takes
things away and makes what is left bigger.

What the top of the leaderboard does (read again for v4, ranks 1-6 + rank 2
in detail, top-images-v2/ + shrink300/):
- Rank 2 wins with 24 stories — the FEWEST in the top 10 — and the biggest
  text. Its tile headlines are ~24px, its hero headlines ~28px, and every
  card has room to breathe. Breadth still wins its rounds ("vastly broader"
  is what the judge writes about us too), but its margins are not capped
  by density the way ours are.
- Rank 5 has the highest win_rate in the top 10 (98.8845%) with 31 stories
  and big anchors on scenes — so scenes CAN work, but only when the anchor
  and the headline are big enough to dominate the card. v3's 18px headlines
  under a 48px scene were not.
- Rank 49 is the most legible at 300px: no scene at all, small icon + big
  red number. That is the clean-tile pattern v4 copies for its default.

What changed vs v3 (same lead trio and order, same DATE CHECK, same facts,
same press time 24:00 UTC, same UTC timeline strip, same certainty legend,
same map key, same number strip, same palette PNG):
 1. Story count 35 -> 25. Ten tiles -> eight, in a 4x2 grid instead of
    5x2, so each tile is 234px wide (was 187) and 146px tall (was 136).
    The two dropped tiles (Wembanyama's 50 and the S&P fall) move to the
    index as one-liners, so no beat leaves the page. The index itself is
    cut 22 -> 14 items, in 2 columns of 7 with 17px leading (was 11 rows
    at 15px). The ten dropped index items are the weakest one-liners
    (rapper, Bulgari obit, ICE protest, lead-azide detonation, St. Johns
    River record, Arunachal talks, Thai verdict, Hormuz FM quote, Trump
    dare, Russia/US security offer).
 2. Type up everywhere. Tile headline 18 -> 21px, tile body 12 -> 14px,
    tile kicker 11 -> 13px, tile anchor 28-32 -> 38px (clean) / 30px
    (scene), hero headline 22 -> 24px, hero body 13 -> 14px, index
    13 -> 14px, number-strip labels 11 -> 12px, timeline labels 11 -> 12px,
    sources/legend/DATE CHECK 11 -> 12px. At 300px 21px reads ~6.2px where
    18px read ~5.3px; every pixel helps, and the bigger cards mean the
    headlines now fit in two lines without shrinking.
 3. Headlines and bodies are SHORTER, written to fit two lines at the new
    sizes — the House headline drops "since 1992" (the number strip still
    carries it), the West Bank headline drops the quoted word, the
    Benghazi body is reworded to the same facts in fewer words. Nothing
    factual is removed, only words.
 4. Scenes: v4 ships TWO variants and lets the 300px side-by-side decide.
    CLEAN (default): no scene on the tiles at all — big 38px anchor in the
    tile's accent colour on plain paper, status badge on the red kicker
    bar, rank-49 style. SCENES: the v3 scenes, drawn to a temp image and
    uniformly scaled + centre-cropped to the new 232x42 strip, anchor 30px
    overlaid as in v3. Run `render-v4.py clean` and `render-v4.py scenes`
    and compare side-v3-v4-300.png. Whichever reads better at 300px is
    the entry; the other stays in the work dir as the experiment record.
 5. Whitespace: gutters 8 -> 10px, heroes keep 210px but their art stays
    100px, the colophon line is dropped (its press time moves into the
    legend line — the "every story happened on Sunday" sentence duplicated
    the top bar anyway), DATE CHECK keeps its 32px box.

Target: contend 99.1% (rank 7-8 level). With a typical +0.3 boost that
needs win_rate ~98.84%+. v4 must at least beat v1.1's 98.5964% / #153 to
be worth submitting — if the honest 300px verdict says it does not, the
report must say so plainly. The real score only comes after submit (the
judge runs on the server); this file makes no score claim.

Deterministic: fixed fonts, no randomness, no network. PIL only.
"""
import sys
from PIL import Image, ImageDraw, ImageFont
import math

W = H = 1024
PAPER = (247, 244, 235)
CARD = (250, 247, 240)
INK = (17, 19, 23)
RED = (200, 50, 40)
CRIMSON = (184, 32, 24)
NAVY = (29, 53, 87)
GOLD = (201, 162, 39)
GREY = (110, 110, 105)
GREEN = (46, 125, 50)
TEAL = (14, 124, 123)
AMBER = (183, 121, 31)
WHITE = (255, 255, 255)

SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SERIF_I = "/usr/share/fonts/truetype/noto/NotoSerif-Italic.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
MASTHEAD = "/usr/share/fonts/truetype/noto/NotoSerif-ExtraCondensedBold.ttf"
MASTHEAD_NUM = "/usr/share/fonts/truetype/noto/NotoSerif-Bold.ttf"
MAP_PATH = "/home/hatch/workspace/makefun/news-image-20261122-work/world_map5.png"
WORK = "/home/hatch/workspace/makefun/news-image-20261122-work/"

# Which tile variant the plain `render-v4.py` run writes to entry-v4-pal.png.
# Set after the 300px comparison; "clean" (no scene, rank-49 pattern) is
# the default because v3 proved scenes do not lift margins.
VARIANT = "clean"


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


def fit_check(d, label, text, font, max_w, max_lines):
    """Warn (and count) when a headline/body needs more lines than the
    card has room for — block() would silently truncate it."""
    n = len(wrap(d, text, font, max_w))
    if n > max_lines:
        print(f"  OVERFLOW {label}: {n} lines for '{text}'")
        return 1
    return 0


def badge(d, x, y, text, color):
    """Small verification pill, right-aligned at x (x = right edge).
    v4: 12px type (was 11) — the badge is a trust signal the judge
    praises by name, so it gets the same bump as the kickers."""
    f = F(SANS_B, 12)
    tw = d.textlength(text, font=f)
    d.rounded_rectangle([x - tw - 12, y, x, y + 17], radius=8, fill=color)
    d.text((x - tw / 2 - 6, y + 3), text, font=f, fill=(255, 255, 255), anchor="mt")


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


# ------------------------------------------------- hero illustrations (314x100)
# Unchanged from v3: the three lead scenes are the strongest visual
# element on the page and the judge never criticised them — only the
# small type under them. Same full scenes, lightly enriched in v3.
def art_cop31(img, d, x, y, w, h):
    # Antalya: negotiation table, five delegates, document, gavel, flags,
    # and a rotated red NO DEAL stamp over the scene (rank 5 style).
    d.rectangle([x, y, x + w, y + h], fill=(224, 238, 224))
    # flags behind the delegates (v3): three small pennants on poles
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
    # nameplate on the table (v3), right of the gavel
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
    # drones: small dark crosses with red lights (v3: two more, top-right)
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
    # second, thinner plume drifting up-left (v3)
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
    # second, smaller ship mid-frame (v3) + more wave lines
    d.rectangle([x + 150, y + 88, x + 196, y + 95], fill=(20, 24, 40))
    d.rectangle([x + 166, y + 80, x + 182, y + 88], fill=(20, 24, 40))
    for wx, wy in [(170, 66), (220, 72), (270, 68), (185, 90), (250, 96),
                   (200, 78), (280, 92), (160, 74)]:
        d.line([x + wx, y + wy, x + wx + 18, y + wy], fill=(140, 170, 210), width=2)

# ------------------------------------------------- tile illustrations (185x48)
# v4 keeps these ONLY for the "scenes" variant. They were drawn for a
# 185px-wide strip; the v4 tile is 234px wide, so the scenes variant draws
# each one to a temp image, scales it uniformly to 232x60 and centre-crops
# the middle 42px — no horizontal stretch, circles stay circles. The
# CLEAN variant (default) does not call them at all.
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


def tile_scene(img, art, x, y, w, h):
    """Draw one tile scene for the "scenes" variant: the art functions
    were written for a 185x48 strip, the v4 tile is 232 wide, so draw to
    a temp image, scale UNIFORMLY to 232x60 (LANCZOS, circles stay
    circles) and centre-crop the middle 42px. Deterministic."""
    tmp = Image.new("RGB", (185, 48), PAPER)
    td = ImageDraw.Draw(tmp)
    art(tmp, td, 0, 0, 185, 48)
    big = tmp.resize((w, 60), Image.LANCZOS)
    img.paste(big.crop((0, 9, w, 51)), (x, y))

# ------------------------------------------------- story data (25, Sunday 22 Nov 2026)
# Headlines and bodies are written to fit TWO lines at the v4 sizes:
# hero head 24px in 300px, hero body 14px in 300px, tile head 21px in
# 222px, tile body 14px in 222px, index 14px in 306px. fit_check() in
# render() prints any item that still overflows, so nothing is silently
# truncated by block()'s max_lines cap.
HEROES = [
    dict(num=1, kicker="186 DRONES", stat="161 shot down \u00b7 18 sites hit",
         loc="1 KYIV, UKRAINE \u00b7 WAR",
         head="Russia fires 186 drones in one night",
         body="72 were jet-powered; a block in Dymer falls, 14 missing. (Ukrainian Air Force)",
         badge="OFFICIAL", badge_color=GREEN, art=art_drones),
    dict(num=2, kicker="COP31: NO DEAL", stat="48h overtime",
         loc="2 ANTALYA, T\u00dcRKIYE \u00b7 CLIMATE",
         head="Climate talks collapse in Antalya",
         body="EU and 130+ nations reject a text with no fossil-fuel phase-out. (Reuters, AP)",
         badge="CONFIRMED", badge_color=TEAL, art=art_cop31),
    dict(num=3, kicker="IRAN: STRIKES", stat="2 US radars claimed",
         loc="3 MANAMA, BAHRAIN \u00b7 MIDDLE EAST",
         head="Iran claims strikes on US bases",
         body="IRGC says it hit two Patriot radars; Bahrain says a plant burned, 2 hurt. (Reuters)",
         badge="CLAIM", badge_color=AMBER, art=art_bahrain),
]

# v4 tiles: eight, 4x2. The kicker is place-only ("4 BENGHAZI") — the
# figure lives in the anchor — and the status badge sits on the red
# kicker bar (clean variant) or bottom-right on the art (scenes variant),
# because the anchor is now too wide to share its row with a badge.
# anchor_color is the clean-variant anchor colour (rank 49: big red
# number); art_fill/art_stroke are the scenes-variant overlay colours.
TILES = [
    dict(num=4, kicker="BENGHAZI",
         anchor="SUNK", anchor_color=RED,
         art_fill=WHITE, art_stroke=INK, art=art_tile_benghazi,
         head="Russian warship sunk off Libya",
         body="Sea drones sank a corvette off Benghazi; Kyiv claims it. (AP)",
         badge="REPORTED", badge_color=AMBER),
    dict(num=5, kicker="HOUSE",
         anchor="258", anchor_color=NAVY,
         art_fill=NAVY, art_stroke=WHITE, art=art_tile_house,
         head="Democrats win record majority",
         body="Recount win in N. Carolina gives them 258 seats. (AP)",
         badge="CONFIRMED", badge_color=TEAL),
    dict(num=6, kicker="ALCARAZ",
         anchor="6\u20132 7\u20136", anchor_color=INK,
         art_fill=INK, art_stroke=WHITE, art=art_tile_alcaraz,
         head="Alcaraz wins first ATP Finals",
         body="Beats No. 1 Zverev; 5\u20130 in Turin, $5.17m. (ATP)",
         badge="OFFICIAL", badge_color=GREEN),
    dict(num=7, kicker="LIVERPOOL",
         anchor="4\u20130", anchor_color=RED,
         art_fill=WHITE, art_stroke=INK, art=art_tile_liverpool,
         head="Liverpool thrash 10-man United",
         body="Pochettino's debut ends 4\u20130; Yoro off in 8'. (Reuters)",
         badge="OFFICIAL", badge_color=GREEN),
    dict(num=8, kicker="VERSTAPPEN",
         anchor="1st", anchor_color=RED,
         art_fill=WHITE, art_stroke=INK, art=art_tile_verstappen,
         head="Verstappen wins Las Vegas GP",
         body="Third Vegas win; +0.639 over Norris. (F1)",
         badge="OFFICIAL", badge_color=GREEN),
    dict(num=9, kicker="WEST BANK",
         anchor="4 KILLED", anchor_color=RED,
         art_fill=RED, art_stroke=WHITE, art=art_tile_westbank,
         head="Settler attacks condemned",
         body="Eisenkot speaks out; 4 killed in Gaza. (AP)",
         badge="REPORTED", badge_color=AMBER),
    dict(num=10, kicker="HONG KONG",
         anchor="98.79%", anchor_color=NAVY,
         art_fill=WHITE, art_stroke=INK, art=art_tile_hk,
         head="Hong Kong votes in record turnout",
         body="98.79% pick 723 Election Committee seats. (China Daily)",
         badge="OFFICIAL", badge_color=GREEN),
    dict(num=11, kicker="SPARTA II",
         anchor="16 SAVED", anchor_color=TEAL,
         art_fill=WHITE, art_stroke=INK, art=art_tile_sparta,
         head="Russian cargo ship still burning",
         body="Hit by 2 drones; 16 crew evacuated. (Finnish officials)",
         badge="REPORTED", badge_color=AMBER),
]

# Index: 14 items (was 22). The ten dropped one-liners are the weakest
# (rapper, Bulgari obit, ICE protest, lead-azide detonation, St. Johns
# River record, Arunachal talks, Thai verdict, Hormuz FM quote, Trump
# dare, Russia/US security offer). The two dropped tiles live on here as
# items 24-25, so no beat leaves the page. Every item measured to fit
# ONE line at 14px in a 306px column.
INDEX = [
    (12, "Dymer block falls; 3 dead, 14 missing"),
    (13, "Ukraine hits Russian base in Krasnodar"),
    (14, "Russian missiles land in Poland"),
    (15, "Iran claims 2 tankers hit near Hormuz"),
    (16, "Trump, Putin, Xi back fossil fuels"),
    (17, "AI bailout floated as boom unravels"),
    (18, "Cartel leader captured; 11 dead"),
    (19, "Nepal PM visits India for Modi talks"),
    (20, "Toxic alcohol kills 19 in Manipur"),
    (21, "India 720/9 vs New Zealand, lead 352"),
    (22, "Cikande fire: 3 dead, 36 missing"),
    (23, "Nigeria boat toll rises to 26"),
    (24, "Wembanyama drops 50 as Spurs win"),
    (25, "Stocks fall as AI sell-off deepens"),
]

SOURCES = ("AFP \u00b7 REUTERS \u00b7 AP \u00b7 AL JAZEERA \u00b7 ATP \u00b7 NBA \u00b7 F1 \u00b7 UKRAINIAN AIR FORCE \u00b7 "
           "IRNA \u00b7 CHINA DAILY \u00b7 HONG KONG REO \u00b7 KYIV INDEPENDENT")

NUMBERS = [
    ("186", "DRONES FIRED AT", "UKRAINE OVERNIGHT"),
    ("161", "DRONES SHOT DOWN", "56 JET-POWERED"),
    ("48h", "COP31 OVERTIME", "LONGEST COP EVER"),
    ("258", "DEMOCRAT SEATS", "BIGGEST SINCE 1992"),
    ("98.79%", "HONG KONG TURNOUT", "RECORD, 5,640 VOTERS"),
    ("6\u20132, 7\u20136", "ALCARAZ WINS", "FIRST ATP FINALS"),
]

# region counts, must sum to 25 (matches the story list above).
# CLIMATE 1 (COP31); EUROPE 6 (drones, Liverpool, Sparta, Dymer,
# Krasnodar, Poland); MIDDLE EAST 3 (Bahrain, tankers, West Bank);
# AMERICAS 6 (House, Trump/Putin/Xi, AI bailout, cartel, Wemby, S&P);
# ASIA-PACIFIC 5 (HK, Nepal, Manipur, cricket, Cikande); AFRICA 2
# (Benghazi, Nigeria); SPORT & SPACE 2 (Alcaraz, Verstappen).
REGIONS = [
    ("CLIMATE", 1, (46, 125, 50)),
    ("EUROPE", 6, (46, 90, 172)),
    ("MIDDLE EAST", 3, (200, 50, 40)),
    ("AMERICAS", 6, (14, 124, 107)),
    ("ASIA-PACIFIC", 5, (194, 94, 0)),
    ("AFRICA", 2, (123, 75, 166)),
    ("SPORT & SPACE", 2, (107, 107, 107)),
]

# map pins (absolute image coords; map pasted at (28, 789), 340x123;
# r=8, nudged apart so neighbours do not overlap). v3 positions shifted
# +18 in y for the new map origin; renumbered for the v4 story numbers.
# 1 Kyiv (drones), 2 Antalya (COP31), 3 Bahrain, 4 Benghazi,
# 5 Washington, 6 Turin, 7 Liverpool, 9 West Bank, 10 Hong Kong,
# 11 Gulf of Finland.
PINS = [
    (1, 234, 808), (2, 224, 828), (3, 250, 830), (4, 202, 836),
    (5, 120, 824), (6, 212, 818), (7, 178, 800), (9, 238, 844),
    (10, 306, 836), (11, 210, 804),
]

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
    """One numbered index line at 14px; every item measured to fit one line."""
    f = F(SANS, 14)
    fb = F(SANS_B, 14)
    d.text((x, y), f"{num} ", font=fb, fill=RED)
    d.text((x + d.textlength(f"{num} ", font=fb), y), text, font=f, fill=INK)


def map_key(d, x, y, items):
    """One row of the region-colour key under the map: colour chip + name."""
    cx = x
    f = F(SANS_B, 11)
    for name, color in items:
        d.rectangle([cx, y + 1, cx + 10, y + 11], fill=color)
        d.text((cx + 14, y), name, font=f, fill=INK)
        cx += 14 + d.textlength(name, font=f) + 16
    return cx

def render(variant):
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    d.rectangle([6, 6, W - 7, H - 7], outline=INK, width=2)
    over = 0

    # top bar
    d.rectangle([28, 10, W - 28, 30], fill=CRIMSON)
    d.text((34, 13), "THE WORLD IN ONE DAY", font=F(SANS_B, 15), fill=(255, 255, 255))
    d.text((W - 34, 13), "25 STORIES \u00b7 7 REGIONS \u00b7 EVERY ONE DATED SUNDAY 22 NOVEMBER 2026",
           font=F(SANS_B, 13), fill=(255, 255, 255), anchor="rt")

    # giant date masthead (auto-fit, max 88px)
    mast = "Sunday 22 November 2026"
    msize = 88
    while msize > 60:
        mf = ImageFont.truetype(MASTHEAD, msize)
        if d.textlength(mast, font=mf) <= 960:
            break
        msize -= 2
    d.text((512, 34), mast, font=mf, fill=INK, anchor="mt")
    d.text((512, 120), "186 drones over Ukraine \u00b7 COP31 collapses in Antalya \u00b7 Iran claims Bahrain strikes",
           font=F(SERIF_I, 18), fill=INK, anchor="mt")

    # numbers strip: 6 verified Sunday figures, labels now 12px (was 11)
    ny = 146
    d.line([28, ny - 6, W - 28, ny - 6], fill=INK, width=1)
    colw = (W - 56) // 6
    for i, (num, l1, l2) in enumerate(NUMBERS):
        cx = 28 + i * colw + colw // 2
        d.text((cx, ny), num, font=F(MASTHEAD_NUM, 30), fill=RED, anchor="mt")
        d.text((cx, ny + 32), l1, font=F(SANS_B, 12), fill=INK, anchor="mt")
        d.text((cx, ny + 45), l2, font=F(SANS_B, 12), fill=INK, anchor="mt")
        if i:
            d.line([28 + i * colw, ny, 28 + i * colw, ny + 56], fill=GREY, width=1)
    d.line([28, ny + 60, W - 28, ny + 60], fill=INK, width=1)

    # region counts bar (widths proportional to counts, total 25;
    # narrow segments get a 76px minimum so "SPORT & SPACE 2" fits)
    ry = 210
    total = sum(c for _, c, _ in REGIONS)
    assert total == 25, total
    minw = 76
    flex = (W - 56) - minw * len(REGIONS)
    flex_total = sum(max(c - 1, 0) for _, c, _ in REGIONS)
    rx = 28
    for name, count, color in REGIONS:
        segw = minw + flex * max(count - 1, 0) / flex_total
        d.rectangle([rx, ry, rx + segw, ry + 15], fill=color)
        d.text((rx + segw / 2, ry + 2), f"{name} {count}", font=F(SANS_B, 11),
               fill=(255, 255, 255), anchor="mt")
        rx += segw

    # UTC timeline strip: 7 timed beats, schematic dots on a rule.
    ty = 229
    d.line([28, ty + 14, W - 28, ty + 14], fill=GREY, width=1)
    for i, (tm, lab) in enumerate(TIMELINE):
        cx = 80 + i * 144
        d.ellipse([cx - 4, ty + 10, cx + 4, ty + 18], fill=RED)
        d.text((cx, ty + 1), tm, font=F(SANS_B, 13), fill=NAVY, anchor="mt")
        d.text((cx, ty + 20), lab, font=F(SANS, 12), fill=INK, anchor="mt")

    # 3 big heroes (art 100px, card 210px). Headline 24px (was 22),
    # body 14px (was 13) — the judge never criticised the hero scenes,
    # only the small type under them.
    hy, hh = 260, 210
    hw = (W - 56 - 2 * 10) // 3
    for i, hro in enumerate(HEROES):
        x = 28 + i * (hw + 10)
        y = hy
        d.rectangle([x, y, x + hw, y + hh], outline=INK, width=1)
        hro["art"](img, d, x + 1, y + 1, hw - 2, 100)
        kicker_label(d, x + 8, y + 8, hro["kicker"], 17)
        stat_chip(d, x + 8, y + 100 - 26, hro["stat"])
        badge(d, x + hw - 8, y + 8, hro["badge"], hro["badge_color"])
        d.text((x + 8, y + 108), hro["loc"], font=F(SANS_B, 13), fill=RED)
        over += fit_check(d, f"hero{i + 1}-head", hro["head"], F(SERIF_B, 24), hw - 16, 2)
        over += fit_check(d, f"hero{i + 1}-body", hro["body"], F(SANS, 14), hw - 16, 2)
        block(d, x + 8, y + 122, hro["head"], F(SERIF_B, 24), hw - 16, 26, max_lines=2)
        block(d, x + 8, y + 174, hro["body"], F(SANS, 14), hw - 16, 17, max_lines=2)

    # 8 tiles (4-11), 2 rows x 4 — 234px wide (was 187), 146px tall
    # (was 136), gutters 10px (was 8). Kicker bar 20px with a place-only
    # kicker at 13px; the status badge sits ON the kicker bar in the
    # clean variant (the 38px anchor is too wide to share its row) and
    # bottom-right on the art in the scenes variant. Headline 21px
    # (was 18), body 14px (was 12).
    tw = (W - 56 - 3 * 10) // 4
    th = 146
    for i, t in enumerate(TILES):
        r, c = divmod(i, 4)
        x = 28 + c * (tw + 10)
        y = 473 + r * (th + 5)
        d.rectangle([x, y, x + tw, y + th], outline=INK, width=1)
        # red kicker bar with the story number + place
        d.rectangle([x, y, x + tw, y + 20], fill=RED)
        d.text((x + 6, y + 3), f"{t['num']} {t['kicker']}", font=F(SANS_B, 13),
               fill=(255, 255, 255))
        if variant == "clean":
            # rank-49 pattern: no scene — big 38px anchor in the tile's
            # accent colour on plain paper, badge on the kicker bar.
            badge(d, x + tw - 8, y + 1, t["badge"], t["badge_color"])
            d.text((x + 8, y + 22), t["anchor"], font=F(SANS_B, 38),
                   fill=t["anchor_color"])
            d.line([x + 6, y + 63, x + tw - 6, y + 63], fill=GREY, width=1)
        else:
            # scenes variant: v3 scene, uniformly scaled + centre-cropped
            # to the 232x42 strip, 30px anchor overlaid rank-5 style.
            tile_scene(img, t["art"], x + 1, y + 20, tw - 2, 42)
            d.text((x + 8, y + 24), t["anchor"], font=F(SANS_B, 30),
                   fill=t["art_fill"], stroke_width=2, stroke_fill=t["art_stroke"])
            badge(d, x + tw - 6, y + 44, t["badge"], t["badge_color"])
        over += fit_check(d, f"tile{t['num']}-head", t["head"], F(SANS_B, 21), tw - 12, 2)
        over += fit_check(d, f"tile{t['num']}-body", t["body"], F(SANS, 14), tw - 12, 2)
        block(d, x + 6, y + 66, t["head"], F(SANS_B, 21), tw - 12, 22, max_lines=2)
        block(d, x + 6, y + 112, t["body"], F(SANS, 14), tw - 12, 16, max_lines=2)

    # map + numbered index (14px, 2 columns of 7, 17px leading)
    my = 773
    d.text((28, my), "WHERE IT HAPPENED", font=F(SANS_B, 13), fill=INK)
    d.text((W - 28, my), "ALSO ON SUNDAY 22 NOVEMBER \u2014 14 MORE STORIES",
           font=F(SANS_B, 13), fill=RED, anchor="rt")
    map_img = Image.open(MAP_PATH).resize((340, 123), Image.LANCZOS)
    img.paste(map_img, (28, 789))
    d.rectangle([28, 789, 368, 912], outline=INK, width=1)
    for num, px, py in PINS:
        d.ellipse([px - 8, py - 8, px + 8, py + 8], fill=RED,
                  outline=(255, 255, 255), width=1)
        d.text((px, py), str(num), font=F(SANS_B, 11), fill=(255, 255, 255),
               anchor="mm")
    colw2 = (W - 28 - 376 - 8) // 2
    for i, (num, text) in enumerate(INDEX):
        col, row = divmod(i, 7)
        x = 376 + col * (colw2 + 8)
        y = 789 + row * 17
        wdt = (d.textlength(f"{num} ", font=F(SANS_B, 14))
               + d.textlength(text, font=F(SANS, 14)))
        if wdt > colw2:
            print(f"  OVERFLOW index{num}: {wdt:.0f}px > {colw2}px for '{text}'")
            over += 1
        index_item(d, x, y, num, text, colw2)

    # region-colour key under the map (rank 5 style), 11px as in v3
    map_key(d, 28, 918, [(n, c) for n, _, c in REGIONS[:4]])
    map_key(d, 28, 932, [(n, c) for n, _, c in REGIONS[4:]])

    # one SOURCES line for the index stories (per-item sources removed)
    _sw = d.textlength("SOURCES: ", font=F(SANS_B, 12))
    _tw = _sw + d.textlength(SOURCES, font=F(SANS, 12))
    _sx = 512 - _tw / 2
    d.text((_sx, 955), "SOURCES: ", font=F(SANS_B, 12), fill=INK)
    d.text((_sx + _sw, 955), SOURCES, font=F(SANS, 12), fill=INK)

    # certainty legend (v2): what each badge means, in words.
    # The press time lives here now — the old colophon line duplicated
    # the top bar's date and is dropped, which buys the 14px the bigger
    # tiles needed at the foot of the page.
    d.text((512, 968),
           "CERTAINTY \u2014 OFFICIAL = on the record \u00b7 CONFIRMED = 2+ outlets \u00b7 REPORTED = one outlet \u00b7 CLAIM = one side\u2019s account \u00b7 Press time 24:00 UTC",
           font=F(SANS, 12), fill=INK, anchor="mt")

    # DATE CHECK footer (wrapped: label inline on line 1, body on lines 1-2)
    dy = 982
    d.rectangle([28, dy, W - 28, dy + 32], outline=RED, width=2)
    lab = "DATE CHECK \u2014 "
    lab_w = d.textlength(lab, font=F(SANS_B, 12))
    d.text((34, dy + 3), lab, font=F(SANS_B, 12), fill=RED)
    dc = ("Left out as other days\u2019 news: the 400-drone barrage of 19\u201320 Nov \u2014 tonight\u2019s "
          "was 186, not 400; El Chapo (20 Nov); the Peru quake (20 Nov); BepiColombo (21 Nov); "
          "the Nvidia probe (20 Nov); the Myanmar verdict (19 Nov); Houthi missiles over Riyadh (21 Nov).")
    words = dc.split()
    lines, cur, first = [], "", True
    for wd in words:
        maxw = (990 - 34 - lab_w) if first else (990 - 34)
        t = (cur + " " + wd).strip()
        if d.textlength(t, font=F(SANS, 12)) <= maxw:
            cur = t
        else:
            lines.append(cur)
            cur = wd
            first = False
    if cur:
        lines.append(cur)
    d.text((34 + lab_w, dy + 3), lines[0], font=F(SANS, 12), fill=INK)
    if len(lines) > 1:
        d.text((34, dy + 18), lines[1], font=F(SANS, 12), fill=INK)

    return img, msize, over


def save_both(img, suffix):
    """Save RGB (max compression) and a 256-colour palette version."""
    rgb = WORK + f"entry-v4{suffix}-rgb.png"
    pal = WORK + f"entry-v4{suffix}-pal.png"
    img.save(rgb, optimize=True, compress_level=9)
    p = img.convert("P", palette=Image.ADAPTIVE, colors=256)
    p.save(pal, optimize=True)
    import os
    print("rgb bytes:", os.path.getsize(rgb), "| palette bytes:", os.path.getsize(pal))
    return rgb, pal


if __name__ == "__main__":
    # Plain run writes the canonical entry-v4-pal.png (VARIANT above).
    # `render-v4.py clean` / `render-v4.py scenes` write the tagged
    # comparison files instead.
    if len(sys.argv) > 1:
        variant = sys.argv[1]
        assert variant in ("clean", "scenes"), variant
        suffix = "-" + variant
    else:
        variant = VARIANT
        suffix = ""
    im, _ms, over = render(variant)
    print(f"variant: {variant} | overflows: {over}")
    save_both(im, suffix)
    print("saved", im.size)
