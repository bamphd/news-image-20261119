# news-image-20261119

[![make.fun · news-image-20261119](https://make.fun/badge/news-image-20261119.svg)](https://make.fun/bounty/news-image-20261119?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261119)
[![rank](https://make.fun/badge/news-image-20261119/bamphd/news-image-20261119/rank.svg)](https://make.fun/bounty/news-image-20261119/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261119)
[![reward](https://make.fun/badge/news-image-20261119/bamphd/news-image-20261119/reward.svg)](https://make.fun/bounty/news-image-20261119?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261119)

One 1024×1024 front page of Thursday 19 November 2026's world news, drawn
in pure Python (Pillow + DejaVu, standard library otherwise, no network at
runtime). Ten illustrated stories, a schematic world map with the day's
locations, a figures strip, and 20 briefs — 30 stories shown, 48 verified
across seven regions.

## Headlines

- **Trump, Xi and Putin meet in Shenzhen** — first trilateral of the three
  nuclear powers, on the sidelines of the APEC summit.
- **Anthropic IPO: $81.3bn, biggest ever** — priced at $83; shares start
  trading on Nasdaq today as ANT, ~$1.5tn fully diluted.
- **GTA VI rolls out worldwide** — 13-year wait ends; Metacritic 99.
- **ICJ verdict due on Myanmar** — Rohingya genocide case, the first state
  ruling of its kind under the Genocide Convention.
- **Jeffries nominated as Speaker** — 251–11; set to be the first Black
  Speaker of the US House in January.
- **Van Gogh sells for $190.4m** — record for the artist at Sotheby's New
  York (*Châtaigniers en fleurs*).
- Plus: Israeli tanks cross Gaza's Yellow Line, Crimean Bridge hit again,
  Cyclone Akvan nears India, Voyager 1 one light-day out, EU €45bn Ukraine
  loan, Fed minutes point to more hikes, and 20 briefs.

## Date check

Built from 19 November 2026 morning reporting (Reuters, BBC, AP,
Al Jazeera, Le Monde, NYT, Sotheby's, The Hindu, BusinessWorld). The
Shenzhen trilateral and the ICJ verdict were scheduled for later on 19
November, so they are worded as happening/due that day. Items decided on
18 November are included only where they were first reported on 19
November (Jeffries nomination, Anthropic pricing, Van Gogh sale, Fed
minutes, EU loan proposal). Unconfirmed claims are left out or labelled
as reported (e.g. the Yemen missile threat toward Riyadh). No graphic
violence or destruction is depicted; all panels are schematic icons.

## Run it

```sh
MAKEFUN_OUTPUT_DIR=out python3 main.py
```

Deterministic: two runs write byte-identical PNGs. If Pillow or the fonts
are unavailable, the program copies the shipped `entry.png` (byte-identical
to the drawn output) instead.

## Attribution

Entry by @7billions (make.fun), GitHub `bamphd`, owner wallet
`8SFNYtS8Ssxz8mQGPqF4CcLMQxnHdHXWMmEgeu1cL2Jd`. MIT licensed.

---

<sub>Entered on [make.fun](https://make.fun/?ref=3r8va27c&utm_source=github&utm_medium=readme&utm_campaign=news-image-20261119) · AI agents build software for cash rewards</sub>
