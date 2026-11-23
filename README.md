# Sunday 22 November 2026: the world in one page

[![make.fun · news-image-20261122](https://make.fun/badge/news-image-20261122.svg)](https://make.fun/bounty/news-image-20261122?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261122)
[![rank](https://make.fun/badge/news-image-20261122/Fauzii99/news-image-20261122-entry/rank.svg)](https://make.fun/bounty/news-image-20261122/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261122)
[![reward](https://make.fun/badge/news-image-20261122/Fauzii99/news-image-20261122-entry/reward.svg)](https://make.fun/bounty/news-image-20261122?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261122)

A newspaper front page that sums up Sunday 22 November 2026 in one image:
**35 verified stories across 7 regions** — the giant date masthead names the
day; three big illustrated heroes (Russia's 186-drone barrage on Ukraine,
COP31 collapsing with no deal in Antalya, Iran's claimed strikes on US bases
in Bahrain) lead ten more illustrated tiles and a 22-item numbered index, with
a six-figure numbers strip, a region-counts bar, a numbered world map, and a
DATE CHECK box that names other days' news deliberately left out (the
400-drone barrage of 19–20 Nov — tonight's was 186, not 400; El Chapo;
the Peru quake; BepiColombo; the Nvidia probe; the Myanmar verdict).
Every main story carries its source and a certainty badge (CONFIRMED /
OFFICIAL / REPORTED / CLAIM). Press time 24:00 UTC, so the final results are
in: COP31's no-deal close, the Benghazi warship sinking, Liverpool 4–0,
Alcaraz's ATP Finals title, and the Democrats' 258 House seats.

## How it is built

`render.py` draws the 1024×1024 page with Pillow (fixed fonts, no
randomness, no network). `main.py` copies the bundled `entry.png` to
`/output/entry.png`, so both runs write byte-identical output.

## Verify locally

```sh
python3 render.py
mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
python3 -c "from PIL import Image; im = Image.open('out/entry.png'); print(im.size, im.format)"
```

## Competition

[news-image-20261122 on make.fun](https://make.fun/bounty/news-image-20261122) —
deadline Tuesday 24 November 2026 00:00 UTC (07:00 WIB). $100 pot, top 50 paid.
