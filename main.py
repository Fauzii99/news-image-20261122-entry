#!/usr/bin/env python3
"""news-image-20261122 entry: copy the bundled front page to /output/entry.png.

The image is drawn by render.py (same directory) with PIL: a 1024x1024
newspaper front page, "THE WORLD IN ONE DAY", Sunday 22 November 2026,
35 verified stories across 7 regions, a day-in-numbers strip, three hero
stories (Russia's 186-drone barrage on Ukraine, COP31 collapsing with no
deal in Antalya, Iran's claimed strikes on US bases in Bahrain), ten more
illustrated tiles, a 22-item numbered index, a numbered world map, a DATE
CHECK box naming other days' news left out, and a press time of 24:00 UTC.

Standard library only. No network. Deterministic: the same bytes every run.
"""
import os
import shutil
import sys

HERE = os.path.dirname(os.path.abspath(__file__))


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    shutil.copyfile(os.path.join(HERE, "entry.png"),
                    os.path.join(out_dir, "entry.png"))


if __name__ == "__main__":
    sys.exit(main())
