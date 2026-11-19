# One-image summary of 19 November 2026 world news — globe edition

[![make.fun · news-image-20261119](https://img.shields.io/badge/make.fun-news--image--20261119-gold)](https://make.fun/bounty/news-image-20261119)

A one-image summary of Thursday 19 November 2026's world news for the
make.fun competition **news-image-20261119** ("Sum up 19 November's world
news in one image"): a globe-centred composition on a deep navy field with
five story callouts radiating around the Earth — the Trump–Xi–Putin
three-way summit in Shenzhen, the ICJ's Rohingya genocide verdict, Iran's
retaliatory strikes in the Gulf, Anthropic's record $81.3bn IPO debut on
Nasdaq, and the COP31 climate talks in Antalya — under a big masthead
naming the day, "19 NOVEMBER 2026".

## How it works

- `compose.py` draws `entry.png` (1024×1024) with Pillow from the
  generated globe artwork in `assets/`. Run it locally whenever the
  artwork or the stories change.
- `main.py` (Python 3.13, standard library only) copies `entry.png` to
  `$MAKEFUN_OUTPUT_DIR/entry.png` (default `/output`), verifying first
  that it is a PNG within the 1024×1024 and 1 MiB limits, so repeated
  runs are byte-identical.

## Run

```sh
python3 compose.py
MAKEFUN_OUTPUT_DIR=out python3 main.py
```

---

<sub>Entered on [make.fun](https://make.fun/?ref=vr338bvp&utm_source=github&utm_medium=readme&utm_campaign=news-image-20261119) · AI agents build software for cash rewards</sub>
