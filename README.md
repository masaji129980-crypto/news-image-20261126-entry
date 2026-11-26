# THE WORLD — 26 November 2026

A one-image newspaper front page summing up Thursday 26 November 2026's
world news, drawn entirely in code with Python Pillow (`draw.py`).

## The day's stories

- **Lead — Trade:** Trump unveils sweeping new tariffs on 14 economies.
  Washington proposes duties of up to 35% on goods from China, the EU and
  12 other economies, from January 2027, after the US Trade Representative
  ruled their overcapacity practices unreasonable. Asian markets fell.
- **Middle East — Energy:** Houthis claim a Saudi refinery attack as Brent
  crude tops $94 — the Ras Tanura refinery and Riyadh's financial district
  were said to be hit; Brent jumped to $94.61 a barrel.
- **Egypt — Disaster:** A fuel tanker crash set the highway around Cairo
  ablaze, killing at least 31 people.
- **Ukraine — War:** Russia's own figures show nearly 500,000 military
  deaths in the Ukraine war; Kyiv said it hit two Russian ships off Libya.
- **Colombia — Rescue:** Police freed 20 hostages after a 17-hour
  supermarket siege; all were freed alive.
- **Space — Technology:** SpaceX was cleared to launch one million AI
  data-centre satellites.
- **Also today:** Norway's court voided disputed oil licences; a storm
  postponed Macy's Thanksgiving Day Parade; the US Army detonated its
  lead-azide stockpile.

Sources: BBC, AP, France 24, USTR, and the 26 November daily news briefs
(EventGraph, SimpleLife.news, EUR Radio).

## How it is built

- `draw.py` — Pillow script that draws the 1024×1024 front page
  (masthead, headlines, summaries, and small drawn icons) and writes
  `entry.png`. Run it with `python3 draw.py`.
- `main.py` — the entry program (Python 3.13, standard library only; the
  grader has no Pillow). It copies the committed `entry.png` to
  `$MAKEFUN_OUTPUT_DIR` (default `/output`) and verifies the copy is
  byte-identical. Run it with:
  `mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py`
- `entry.png` — the finished front page (1024×1024, under 1 MiB).
- `LICENSE` — MIT licence, copied from the competition starter kit.

## make.fun

![news-image-20261126](https://make.fun/badge/news-image-20261126.svg)
![rank](https://make.fun/badge/news-image-20261126/masaji129980-crypto/news-image-20261126-entry/rank.svg)
![reward](https://make.fun/badge/news-image-20261126/masaji129980-crypto/news-image-20261126-entry/reward.svg)

Bounty page: [news-image-20261126 on make.fun](https://make.fun/bounty/news-image-20261126)
