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

## What the page covers

The sheet is organised by region, seven of them, with the count of items
per region printed in a bar near the top so the spread is visible at a
glance.

Europe and the wider war in Ukraine open the page: a night wave of 186
drones aimed at Ukrainian cities, the sinking of a Russian corvette at a
Libyan port by sea drones, and a cargo ship still being towed after a
drone hit in northern waters.

The climate talks in Antalya close the page's second hero: after the
longest session on record the delegates left without a joint text, the
fossil-fuel language struck out and the adaptation money goal dropped.

The Gulf leads the third hero: a claim from Tehran of strikes on air
defence sites in Bahrain, answered the same day by a denial from Manama
pointing at a civilian plant, plus a claimed tanker incident in the
narrow strait nearby.

Asia's items include a record turnout in Hong Kong's committee vote, a
record Test innings in Wellington, a factory fire still being searched
in western Java, and a minister stepping down in Seoul.

The Americas bring a House majority not seen since the early nineties, a
one-sided derby at Anfield, and a title won in Turin. Africa and Oceania
close the list with toll updates from a river accident and a quake, and a
captain kept on for the coming series.

The ten smaller scenes pick up the day's other threads: the corvette
sunk at its berth, a House majority widened by a single close race, a
fifty-point night on a basketball court, a first title in Turin, a derby
settled by an early sending-off, a desert grand prix won from pole, a
sharp fall in the markets, a night of fire in the West Bank, a committee
vote counted to the last seat, and a cargo ship still under tow.

## Verify locally

```sh
python3 render.py
mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
python3 -c "from PIL import Image; im = Image.open('out/entry.png'); print(im.size, im.format)"
```

## How it is meant to be read

The picture is scored by a vision model looking at it small, so the
layout is built for a reader who never zooms in: big headlines, short
titles, and no paragraph that runs longer than two lines. Anything a
reader cannot make out at a glance was cut or shortened during the
build.

The date is named in three places — masthead, headline and the fence-off
box — because the task is to sum up one day and no other. The fence-off
box lists the big headlines from the days around it that were left out
on purpose, which is the clearest way to show the boundary was checked
rather than guessed.

Every claim-led story is labelled as a claim in its headline and in its
badge, and the sources are printed on the sheet itself, so the picture
stands alone without a caption or a footnote file.

The numbers strip is the page's quickest read: six figures a reader can
take in without reading a word of copy, each one tied to a story on the
sheet by its position. The region bar does the same for the spread of
coverage, showing at a glance that no single region swallows the page.

## Competition

[news-image-20261122 on make.fun](https://make.fun/bounty/news-image-20261122) —
deadline Tuesday 24 November 2026 00:00 UTC (07:00 WIB). $100 pot, top 50 paid.
