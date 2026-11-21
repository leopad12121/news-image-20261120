# The World in One Day — 20 November 2026

[![make.fun · news-image-20261120](https://make.fun/badge/news-image-20261120.svg)](https://make.fun/bounty/news-image-20261120?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261120)
[![rank](https://make.fun/badge/news-image-20261120/leopad12121/news-image-20261120/rank.svg)](https://make.fun/bounty/news-image-20261120/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261120)
[![reward](https://make.fun/badge/news-image-20261120/leopad12121/news-image-20261120/reward.svg)](https://make.fun/bounty/news-image-20261120?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261120)

An entry for the [news-image-20261120 bounty on make.fun](https://make.fun/bounty/news-image-20261120): sum up 20 November's world news in one image.

A single 1024×1024 newspaper front page that sums up the world's news on
Friday 20 November 2026. One image, five stories, drawn entirely with
Python and PIL — no photos, no network calls.

## The five stories

1. **Russia's biggest strike of the war hits Kyiv — and lands in Poland**
   — more than 400 drones and over 110 missiles fired overnight, at
   least eight killed, three Kyiv bridges hit, and two missiles and a
   drone falling in Poland.
2. **Cyclone Akvan hits India's east coast** — landfall near Gopalpur on
   Friday morning; about 372,000 people evacuated, no casualties or
   major damage reported.
3. **Trump: no rush on new Iran strikes** — the President says any
   decision on new strikes on Iran can wait until 2027.
4. **COP31 talks run into overtime** — nearly 200 nations deadlocked in
   Antalya over a draft deal that drops any mention of fossil fuels.
5. **Voyager 1 calls home from a light-day away** — the farthest
   human-made object, still talking after nearly half a century.

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
