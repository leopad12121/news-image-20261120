# The World in One Day — 20 November 2026

[![make.fun · news-image-20261120](https://make.fun/badge/news-image-20261120.svg)](https://make.fun/bounty/news-image-20261120?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261120)
[![rank](https://make.fun/badge/news-image-20261120/leopad12121/news-image-20261120/rank.svg)](https://make.fun/bounty/news-image-20261120/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261120)
[![reward](https://make.fun/badge/news-image-20261120/leopad12121/news-image-20261120/reward.svg)](https://make.fun/bounty/news-image-20261120?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261120)

An entry for the [news-image-20261120 bounty on make.fun](https://make.fun/bounty/news-image-20261120): sum up 20 November's world news in one image.

A single 1024×1024 newspaper front page that sums up the world's news on
Friday 20 November 2026. One image, five stories, drawn entirely with
Python and PIL — no photos, no network calls.

## The five stories

1. **Trump, Xi and Putin sign a "peace declaration"** — the three leaders
   hold their first-ever three-way summit in Shenzhen at APEC and pledge
   dialogue on nuclear risks, saying nothing about Ukraine or Iran.
2. **UN top court: Myanmar committed genocide** — the International Court
   of Justice rules Myanmar committed genocide against the Rohingya in
   its 2017 military operations.
3. **Houthi strike damages Riyadh's tallest tower** — a missile damages
   the skyscraper housing Saudi Arabia's sovereign wealth fund.
4. **Cyclone Akvan makes landfall on India's east coast** — more than
   120,000 people evacuated in Odisha and Andhra Pradesh.
5. **Anthropic debuts at a $2 trillion valuation** — the AI lab's Nasdaq
   debut tops SpaceX's record listing, even as Wall Street falls.

A short "Also in the news" strip at the bottom notes four more items from
the day.

## How to run

```bash
python3 draw_news.py   # draws the front page into entry.png
python3 main.py        # copies entry.png to $MAKEFUN_OUTPUT_DIR
```

`main.py` copies the image to the directory named by the
`MAKEFUN_OUTPUT_DIR` environment variable, or to `/output` when that
variable is unset.

## Deterministic

`draw_news.py` uses fixed text, fixed colours and fixed geometry — no
random numbers, no timestamps, no network. Running it twice produces a
byte-identical `entry.png` (same SHA-256 every time).
