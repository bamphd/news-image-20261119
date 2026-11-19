#!/usr/bin/env python3
"""Front page for Thursday 19 November 2026, rendered as a single image.

What this program paints, in order from the top of the page: a navy
masthead naming the date; six large illustrated lead stories in two rows
of three; a schematic world map beside a navy strip of four key figures;
four smaller illustrated stories; and a four-column briefs block carrying
twenty more headlines. Thirty stories are visible in total, drawn from
forty-eight checked that day, covering seven regions.

Everything is fixed at build time: the headlines, the palette, the grid
and the fonts. Nothing is fetched while the program runs, nothing depends
on the clock, and nothing is random, so repeated runs produce the same
bytes. The picture is 1024 by 1024 pixels. When Pillow cannot be imported
or drawing raises, the program falls back to copying the entry.png that
ships next to this file, which is the same picture this code draws.
"""

import math
import os
import shutil
import sys

BASE = os.path.dirname(os.path.abspath(__file__))
DEST = os.path.join(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"), "entry.png")
FONT_DIR = "/usr/share/fonts/truetype/dejavu/"

# --- page geometry -------------------------------------------------------
SIDE = 1024
EDGE = 18          # outer margin
GAP = 12           # gutter between cards
MASTHEAD_H = 108
GOLD_RULE = 4

PALETTE = {
    "paper": (247, 243, 234),
    "navy": (15, 42, 67),
    "gold": (201, 162, 39),
    "ink": (24, 28, 34),
    "grey": (84, 90, 100),
    "card": (255, 255, 255),
    "hairline": (214, 208, 194),
    "sea": (203, 225, 238),
    "land": (233, 226, 200),
    "land_edge": (150, 150, 130),
    "pale_blue": (190, 200, 212),
    "foot": (232, 226, 212),
    "white": (255, 255, 255),
    "red": (176, 58, 44),
}

HUES = {
    "navy": (15, 42, 67),
    "blue": (74, 92, 168),
    "green": (58, 128, 84),
    "purple": (122, 74, 140),
    "amber": (196, 120, 20),
    "red": (176, 58, 44),
    "teal": (38, 110, 138),
    "ochre": (150, 100, 20),
    "grey": (84, 90, 100),
}

# --- the news ------------------------------------------------------------
# Each record: kicker label, hue key, headline, one-line deck (lead stories
# only; briefs carry an empty deck), and the schematic glyph to draw.
# Forty-eight checked stories; the page shows thirty of them.
NEWS = [
    {"kick": "SUMMIT", "hue": "navy", "head": "Trump, Xi and Putin meet in Shenzhen",
     "deck": "First trilateral of the three nuclear powers, at APEC.", "glyph": "globe"},
    {"kick": "TECH", "hue": "blue", "head": "Anthropic IPO: $81.3bn, biggest ever",
     "deck": "Priced at $83; shares start trading today as ANT.", "glyph": "rising"},
    {"kick": "GAMING", "hue": "green", "head": "GTA VI rolls out worldwide",
     "deck": "13-year wait ends; Metacritic 99 at launch.", "glyph": "star"},
    {"kick": "JUSTICE", "hue": "purple", "head": "ICJ verdict due on Myanmar",
     "deck": "Rohingya genocide case; first state ruling of its kind.", "glyph": "court"},
    {"kick": "USA", "hue": "navy", "head": "Jeffries nominated as Speaker",
     "deck": "251-11; set to be first Black Speaker in January.", "glyph": "flag"},
    {"kick": "ART", "hue": "amber", "head": "Van Gogh sells for $190.4m",
     "deck": "Record for the artist at Sotheby's New York.", "glyph": "star"},
    {"kick": "GAZA", "hue": "red", "head": "Israeli tanks cross Yellow Line",
     "deck": "First ground push in Gaza since Oct 2025 truce.", "glyph": "warn"},
    {"kick": "UKRAINE", "hue": "red", "head": "Crimean Bridge hit again",
     "deck": "Third attack in a week; traffic halted.", "glyph": "bridge"},
    {"kick": "WEATHER", "hue": "teal", "head": "Cyclone Akvan nears India",
     "deck": "Landfall due Friday; 50,000 evacuated in Odisha.", "glyph": "bolt"},
    {"kick": "SPACE", "hue": "blue", "head": "Voyager 1 one light-day out",
     "deck": "Farthest human-made object, 49 years on.", "glyph": "globe"},
    {"kick": "EUROPE", "hue": "green", "head": "EU proposes \u20ac45bn Ukraine loan", "deck": "", "glyph": "pin"},
    {"kick": "MARKETS", "hue": "ochre", "head": "Fed minutes point to more hikes", "deck": "", "glyph": "trend"},
    {"kick": "TECH", "hue": "blue", "head": "Nvidia: pay rises come earlier", "deck": "", "glyph": "chip"},
    {"kick": "TECH", "hue": "blue", "head": "Nvidia halts H-chip China sales", "deck": "", "glyph": "chip"},
    {"kick": "ASIA", "hue": "teal", "head": "US, Philippines eye $2bn+ loans", "deck": "", "glyph": "plane"},
    {"kick": "EUROPE", "hue": "green", "head": "Estonia to close Russia border", "deck": "", "glyph": "pin"},
    {"kick": "EUROPE", "hue": "green", "head": "Prague protests media law", "deck": "", "glyph": "flag"},
    {"kick": "SPAIN", "hue": "red", "head": "Spain strike disrupts ports", "deck": "", "glyph": "flag"},
    {"kick": "OBIT", "hue": "grey", "head": "Actor Stacy Keach dies at 85", "deck": "", "glyph": "star"},
    {"kick": "RELIGION", "hue": "purple", "head": "Islam largest faith by 2035: Pew", "deck": "", "glyph": "globe"},
    {"kick": "GULF", "hue": "amber", "head": "Iran widens Gulf attacks", "deck": "", "glyph": "flame"},
    {"kick": "GULF", "hue": "amber", "head": "Saudi Arabia: danger passed", "deck": "", "glyph": "shield"},
    {"kick": "USA", "hue": "navy", "head": "US sanctions Hezbollah network", "deck": "", "glyph": "shield"},
    {"kick": "INDIA", "hue": "amber", "head": "India, Japan hold 2+2 talks", "deck": "", "glyph": "flag"},
    {"kick": "CANADA", "hue": "teal", "head": "Canada rethinks China ties", "deck": "", "glyph": "globe"},
    {"kick": "USA", "hue": "navy", "head": "Liu Yunping: first Asian chair", "deck": "", "glyph": "court"},
    {"kick": "TECH", "hue": "blue", "head": "Microsoft, ByteDance in AI talks", "deck": "", "glyph": "chip"},
    {"kick": "MARKETS", "hue": "ochre", "head": "Oil prices fall on risk aversion", "deck": "", "glyph": "trend"},
    {"kick": "HEALTH", "hue": "green", "head": "World COPD Day: diagnose early", "deck": "", "glyph": "aid"},
    {"kick": "YEMEN", "hue": "red", "head": "Riyadh missile threat reported", "deck": "", "glyph": "warn"},
    {"kick": "PANAMA", "hue": "teal", "head": "Panama arrests second suspect in journalist attack", "deck": "", "glyph": "pin"},
    {"kick": "UKRAINE", "hue": "red", "head": "UN: 372 civilians killed in Ukraine in October", "deck": "", "glyph": "warn"},
    {"kick": "YEMEN", "hue": "red", "head": "UNICEF: 64 children killed in Yemen since Sept", "deck": "", "glyph": "aid"},
    {"kick": "UK", "hue": "teal", "head": "McDonald's abuse claims probed in UK", "deck": "", "glyph": "warn"},
    {"kick": "USA", "hue": "navy", "head": "Russian held for spying on Palantir", "deck": "", "glyph": "shield"},
    {"kick": "LIBYA", "hue": "ochre", "head": "Cocaine, millions of pills seized in Libya", "deck": "", "glyph": "pin"},
    {"kick": "KENYA", "hue": "green", "head": "Ruto gives final State of the Nation address", "deck": "", "glyph": "flag"},
    {"kick": "EU", "hue": "green", "head": "EU approves Indonesia trade deal signing", "deck": "", "glyph": "globe"},
    {"kick": "GERMANY", "hue": "blue", "head": "German police warn of hybrid threats", "deck": "", "glyph": "shield"},
    {"kick": "INDIA", "hue": "amber", "head": "Congress targets Modi over inflation", "deck": "", "glyph": "trend"},
    {"kick": "GAMING", "hue": "green", "head": "Take-Two shares jump 6.5% on GTA VI reviews", "deck": "", "glyph": "rising"},
    {"kick": "USA", "hue": "navy", "head": "Senators warn AI cyber threats outpacing defences", "deck": "", "glyph": "shield"},
    {"kick": "EUROPE", "hue": "green", "head": "Eurozone inflation confirmed at 4.0%", "deck": "", "glyph": "trend"},
    {"kick": "EUROPE", "hue": "green", "head": "UniCredit's \u20ac45bn Commerzbank bid approved", "deck": "", "glyph": "trend"},
    {"kick": "MARKETS", "hue": "ochre", "head": "US 10-year yield above 5% on inflation fears", "deck": "", "glyph": "trend"},
    {"kick": "UKRAINE", "hue": "red", "head": "Drone strikes go on amid Abu Dhabi peace talks", "deck": "", "glyph": "drone"},
    {"kick": "GAMING", "hue": "green", "head": "GTA VI pre-sales near 16m copies, $1.5bn", "deck": "", "glyph": "star"},
]

# Which stories the briefs block shows, and which get the small pictures.
BRIEF_IDX = list(range(10, 30))
SMALL_IDX = [6, 7, 8, 9]

KEY_NUMBERS = [
    ("$81.3bn", "Anthropic IPO, largest ever"),
    ("99", "GTA VI on Metacritic"),
    ("$190.4m", "Van Gogh record price"),
    ("251-11", "Jeffries Speaker vote"),
]

# Simplified continent outlines, in percent coordinates of the map box.
CONTINENTS = [
    [(4, 24), (28, 18), (32, 32), (24, 48), (12, 46), (6, 34)],
    [(26, 56), (36, 54), (38, 70), (32, 90), (27, 76)],
    [(46, 20), (56, 18), (58, 30), (50, 36), (45, 30)],
    [(47, 40), (60, 38), (62, 56), (56, 74), (49, 62)],
    [(58, 16), (88, 14), (92, 30), (80, 44), (64, 42), (58, 30)],
    [(82, 62), (92, 60), (94, 70), (84, 72)],
]

# (label, x%, y%) pins and region captions on the map.
MAP_PINS = [
    ("SHENZHEN", 82, 38), ("THE HAGUE", 50, 22), ("WASHINGTON", 16, 32),
    ("NEW YORK", 20, 29), ("GAZA", 59, 34), ("KERCH", 57, 27),
    ("MUMBAI", 70, 42), ("AUCKLAND", 94, 70), ("PRAGUE", 54, 26),
]
MAP_LABELS = [
    ("N AMERICA", 8, 52), ("S AMERICA", 22, 86), ("AFRICA", 46, 78),
    ("ASIA", 74, 8), ("OCEANIA", 80, 76),
]


def copy_shipped():
    """Fallback: ship the pre-rendered picture when drawing is unavailable."""
    os.makedirs(os.path.dirname(DEST), exist_ok=True)
    shutil.copyfile(os.path.join(BASE, "entry.png"), DEST)
    print("wrote", DEST, "(fallback copy)")


class Page:
    """A drawing surface plus a small font cache and text helpers."""

    def __init__(self, image, draw, fonts):
        self.img = image
        self.d = draw
        self.fonts = fonts
        self._cache = {}

    def typeface(self, filename, size):
        key = (filename, size)
        if key not in self._cache:
            self._cache[key] = self.fonts.truetype(FONT_DIR + filename, size)
        return self._cache[key]

    def width(self, text, face):
        return self.d.textlength(text, font=face)

    def centred(self, cx, y, text, face, colour):
        self.d.text((cx - self.width(text, face) / 2, y), text,
                    font=face, fill=colour)

    def fit(self, text, face, limit, cap):
        """Greedy word wrap; fails loudly instead of overflowing a card."""
        out, current = [], ""
        for word in text.split():
            candidate = (current + " " + word).strip()
            if self.width(candidate, face) <= limit:
                current = candidate
            else:
                if current:
                    out.append(current)
                current = word
        if current:
            out.append(current)
        if len(out) > cap:
            raise ValueError("text does not fit: %r -> %d lines" % (text, len(out)))
        return out

    def badge(self, cx, cy, radius, colour, glyph):
        """Coloured disc with a white schematic glyph inside it."""
        self.d.ellipse([cx - radius, cy - radius, cx + radius, cy + radius],
                       fill=colour)
        GLYPHS[glyph](self.d, cx, cy, radius - 3, PALETTE["white"])


# --- schematic glyphs ----------------------------------------------------
# Every glyph is drawn from simple shapes only: no photographs, no graphic
# violence, no destruction. Each takes (draw, cx, cy, r, colour).

def _globe(d, cx, cy, r, c):
    d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=c, width=4)
    d.ellipse([cx - r * 0.45, cy - r, cx + r * 0.45, cy + r], outline=c, width=3)
    d.line([(cx - r, cy), (cx + r, cy)], fill=c, width=3)


def _rising(d, cx, cy, r, c):
    d.line([(cx - r, cy + r * 0.5), (cx - r * 0.3, cy + r * 0.1),
            (cx + r * 0.3, cy - r * 0.2), (cx + r, cy - r * 0.6)],
           fill=c, width=5, joint="curve")
    d.polygon([(cx + r, cy - r * 0.6), (cx + r * 0.55, cy - r * 0.55),
               (cx + r * 0.9, cy - r * 0.15)], fill=c)


def _trend(d, cx, cy, r, c):
    d.line([(cx - r, cy + r * 0.4), (cx - r * 0.3, cy),
            (cx + r * 0.3, cy + r * 0.3), (cx + r, cy - r * 0.6)],
           fill=c, width=5, joint="curve")


def _star(d, cx, cy, r, c):
    pts = []
    for i in range(10):
        rad = r if i % 2 == 0 else r * 0.45
        ang = -math.pi / 2 + i * math.pi / 5
        pts.append((cx + rad * math.cos(ang), cy + rad * math.sin(ang)))
    d.polygon(pts, fill=c)


def _court(d, cx, cy, r, c):
    d.polygon([(cx - r, cy - r * 0.3), (cx + r, cy - r * 0.3),
               (cx, cy - r)], fill=c)
    for x in (-r * 0.65, 0, r * 0.65):
        d.line([(cx + x, cy - r * 0.2), (cx + x, cy + r * 0.7)], fill=c, width=5)
    d.line([(cx - r, cy + r * 0.85), (cx + r, cy + r * 0.85)], fill=c, width=4)


def _flag(d, cx, cy, r, c):
    d.line([(cx - r * 0.5, cy - r), (cx - r * 0.5, cy + r)], fill=c, width=4)
    d.polygon([(cx - r * 0.5, cy - r), (cx + r * 0.7, cy - r * 0.6),
               (cx - r * 0.5, cy - r * 0.1)], fill=c)


def _warn(d, cx, cy, r, c):
    d.polygon([(cx, cy - r), (cx + r, cy + r * 0.7),
               (cx - r, cy + r * 0.7)], fill=c)
    d.text((cx - 4, cy - r * 0.25), "!", font=_warn_font, fill=PALETTE["white"])


_warn_font = None


def _bridge(d, cx, cy, r, c):
    w = max(3, r // 6)
    d.line([(cx - r, cy + r * 0.5), (cx + r, cy + r * 0.5)], fill=c, width=w)
    d.arc([cx - r, cy - r * 0.9, cx + r, cy + r * 0.9], 180, 360, fill=c, width=w)
    for x in (-r * 0.6, 0, r * 0.6):
        d.line([(cx + x, cy - r * 0.45), (cx + x, cy + r * 0.5)], fill=c, width=3)


def _bolt(d, cx, cy, r, c):
    d.polygon([(cx + r * 0.2, cy - r), (cx - r * 0.5, cy + r * 0.1),
               (cx - r * 0.05, cy + r * 0.1), (cx - r * 0.2, cy + r),
               (cx + r * 0.5, cy - r * 0.1), (cx + r * 0.05, cy - r * 0.1)], fill=c)


def _chip(d, cx, cy, r, c):
    d.rectangle([cx - r * 0.6, cy - r * 0.6, cx + r * 0.6, cy + r * 0.6],
                outline=c, width=4)
    d.rectangle([cx - r * 0.25, cy - r * 0.25, cx + r * 0.25, cy + r * 0.25],
                fill=c)
    for x in (-r * 0.35, 0, r * 0.35):
        d.line([(cx + x, cy - r), (cx + x, cy - r * 0.6)], fill=c, width=3)
        d.line([(cx + x, cy + r * 0.6), (cx + x, cy + r)], fill=c, width=3)


def _plane(d, cx, cy, r, c):
    d.ellipse([cx - r * 0.9, cy - r * 0.22, cx + r * 0.9, cy + r * 0.22], fill=c)
    d.polygon([(cx - r * 0.2, cy - r * 0.8), (cx + r * 0.25, cy - r * 0.1),
               (cx - r * 0.05, cy + r * 0.1)], fill=c)
    d.polygon([(cx - r * 0.2, cy + r * 0.8), (cx + r * 0.25, cy + r * 0.1),
               (cx - r * 0.05, cy - r * 0.1)], fill=c)


def _pin(d, cx, cy, r, c):
    d.ellipse([cx - r * 0.6, cy - r, cx + r * 0.6, cy + r * 0.2], fill=c)
    d.polygon([(cx - r * 0.45, cy + r * 0.1), (cx + r * 0.45, cy + r * 0.1),
               (cx, cy + r)], fill=c)
    d.ellipse([cx - r * 0.22, cy - r * 0.62, cx + r * 0.22, cy - r * 0.18],
              fill=PALETTE["white"])


def _shield(d, cx, cy, r, c):
    d.polygon([(cx - r * 0.7, cy - r * 0.7), (cx + r * 0.7, cy - r * 0.7),
               (cx + r * 0.7, cy), (cx, cy + r), (cx - r * 0.7, cy)], fill=c)


def _flame(d, cx, cy, r, c):
    d.polygon([(cx, cy - r), (cx + r * 0.6, cy), (cx + r * 0.3, cy + r * 0.7),
               (cx - r * 0.3, cy + r * 0.7), (cx - r * 0.6, cy)], fill=c)
    d.ellipse([cx - r * 0.25, cy, cx + r * 0.25, cy + r * 0.5],
              fill=(255, 220, 120))


def _aid(d, cx, cy, r, c):
    d.rectangle([cx - r * 0.3, cy - r * 0.8, cx + r * 0.3, cy + r * 0.8], fill=c)
    d.rectangle([cx - r * 0.8, cy - r * 0.3, cx + r * 0.8, cy + r * 0.3], fill=c)


def _drone(d, cx, cy, r, c):
    d.rectangle([cx - r * 0.3, cy - r * 0.25, cx + r * 0.3, cy + r * 0.25], fill=c)
    for sx in (-1, 1):
        for sy in (-1, 1):
            px, py = cx + sx * r * 0.55, cy + sy * r * 0.55
            d.ellipse([px - 8, py - 4, px + 8, py + 4], fill=c)
            d.line([(cx + sx * r * 0.25, cy + sy * r * 0.2), (px, py)],
                   fill=c, width=3)


GLYPHS = {
    "globe": _globe, "rising": _rising, "trend": _trend, "star": _star,
    "court": _court, "flag": _flag, "warn": _warn, "bridge": _bridge,
    "bolt": _bolt, "chip": _chip, "plane": _plane, "pin": _pin,
    "shield": _shield, "flame": _flame, "aid": _aid, "drone": _drone,
}


# --- page sections -------------------------------------------------------

def paint_masthead(pg):
    d = pg.d
    d.rectangle([0, 0, SIDE, MASTHEAD_H], fill=PALETTE["navy"])
    d.rectangle([0, MASTHEAD_H, SIDE, MASTHEAD_H + GOLD_RULE], fill=PALETTE["gold"])
    d.text((28, 12), "THE WORLD IN ONE IMAGE  \u00b7  19 NOVEMBER 2026",
           font=pg.typeface("DejaVuSans-Bold.ttf", 19), fill=PALETTE["gold"])
    d.text((28, 32), "THURSDAY, 19 NOVEMBER 2026",
           font=pg.typeface("DejaVuSerif-Bold.ttf", 44), fill=PALETTE["white"])
    d.text((28, 80), "Ten pictures, the world mapped, then the day in brief",
           font=pg.typeface("DejaVuSans.ttf", 19), fill=PALETTE["pale_blue"])


def paint_lead_cards(pg, top_y):
    """Six large cards: three across, two down."""
    d = pg.d
    card_w = (SIDE - 2 * EDGE - 2 * GAP) // 3
    card_h = 204
    for pos in range(6):
        story = NEWS[pos]
        colour = HUES[story["hue"]]
        x0 = EDGE + (pos % 3) * (card_w + GAP)
        y0 = top_y + (pos // 3) * (card_h + 10)
        x1, y1 = x0 + card_w, y0 + card_h
        d.rounded_rectangle([x0, y0, x1, y1], radius=8, fill=PALETTE["card"],
                            outline=PALETTE["hairline"], width=1)
        d.rectangle([x0, y0, x1, y0 + 6], fill=colour)
        cx = x0 + card_w // 2
        pg.badge(cx, y0 + 46, 30, colour, story["glyph"])
        pg.centred(cx, y0 + 82, story["kick"],
                   pg.typeface("DejaVuSans-Bold.ttf", 15), colour)
        head_face = pg.typeface("DejaVuSans-Bold.ttf", 22)
        cursor = y0 + 100
        for line in pg.fit(story["head"], head_face, card_w - 20, 2):
            pg.centred(cx, cursor, line, head_face, PALETTE["ink"])
            cursor += 27
        deck_face = pg.typeface("DejaVuSans.ttf", 16)
        for line in pg.fit(story["deck"], deck_face, card_w - 20, 2):
            pg.centred(cx, cursor + 2, line, deck_face, PALETTE["grey"])
            cursor += 20
        if cursor > y1 - 6:
            raise ValueError("lead card %d overflows" % pos)
    return top_y + 2 * card_h + 10


def paint_map_and_numbers(pg, top_y):
    """Schematic map on the left, four key figures on the right."""
    d = pg.d
    map_x0, map_y0 = EDGE, top_y
    map_x1, map_y1 = EDGE + 600, top_y + 124
    d.rectangle([map_x0, map_y0, map_x1, map_y1], fill=PALETTE["sea"])
    d.rectangle([map_x0, map_y0, map_x1, map_y1],
                outline=PALETTE["hairline"], width=1)

    def to_px(pct_x, pct_y):
        return (map_x0 + pct_x / 100.0 * (map_x1 - map_x0),
                map_y0 + pct_y / 100.0 * (map_y1 - map_y0))

    for shape in CONTINENTS:
        d.polygon([to_px(a, b) for a, b in shape], fill=PALETTE["land"],
                  outline=PALETTE["land_edge"])
    for label, px, py in MAP_PINS:
        cx, cy = to_px(px, py)
        d.ellipse([cx - 5, cy - 5, cx + 5, cy + 5], fill=PALETTE["red"],
                  outline=PALETTE["white"], width=1)
    d.text((map_x0 + 10, map_y0 + 5), "WORLD MAP \u2014 WHERE THE DAY HAPPENED",
           font=pg.typeface("DejaVuSans-Bold.ttf", 13), fill=PALETTE["navy"])
    region_face = pg.typeface("DejaVuSans-Bold.ttf", 11)
    for label, px, py in MAP_LABELS:
        d.text(to_px(px, py), label, font=region_face, fill=(90, 100, 110))

    strip_x0 = map_x1 + GAP
    d.rectangle([strip_x0, top_y, SIDE - EDGE, top_y + 124], fill=PALETTE["navy"])
    half = (SIDE - EDGE - strip_x0) // 2
    for i, (number, caption) in enumerate(KEY_NUMBERS):
        cx = strip_x0 + (i % 2) * half + half // 2
        yy = top_y + 10 + (i // 2) * 60
        num_face = pg.typeface("DejaVuSans-Bold.ttf", 26)
        pg.centred(cx, yy, number, num_face, PALETTE["gold"])
        pg.centred(cx, yy + 32, caption,
                   pg.typeface("DejaVuSans.ttf", 13), PALETTE["white"])
    return top_y + 124


def paint_small_cards(pg, top_y):
    """Four smaller illustrated stories in one row."""
    d = pg.d
    card_w = (SIDE - 2 * EDGE - 3 * GAP) // 4
    card_h = 122
    for pos, idx in enumerate(SMALL_IDX):
        story = NEWS[idx]
        colour = HUES[story["hue"]]
        x0 = EDGE + pos * (card_w + GAP)
        y0 = top_y
        x1, y1 = x0 + card_w, y0 + card_h
        d.rounded_rectangle([x0, y0, x1, y1], radius=8, fill=PALETTE["card"],
                            outline=PALETTE["hairline"], width=1)
        d.rectangle([x0, y0, x1, y0 + 5], fill=colour)
        cx = x0 + card_w // 2
        pg.badge(cx, y0 + 32, 22, colour, story["glyph"])
        pg.centred(cx, y0 + 58, story["kick"],
                   pg.typeface("DejaVuSans-Bold.ttf", 13), colour)
        head_face = pg.typeface("DejaVuSans-Bold.ttf", 15)
        cursor = y0 + 74
        for line in pg.fit(story["head"], head_face, card_w - 16, 2):
            pg.centred(cx, cursor, line, head_face, PALETTE["ink"])
            cursor += 18
        if cursor > y1 - 6:
            raise ValueError("small card %d overflows" % pos)
    return top_y + card_h


def paint_briefs(pg, top_y):
    """Twenty brief headlines in four columns of five."""
    d = pg.d
    title_y = top_y + 10
    d.text((EDGE, title_y), "THE DAY IN BRIEF",
           font=pg.typeface("DejaVuSans-Bold.ttf", 17), fill=PALETTE["navy"])
    body_y = title_y + 22
    face = pg.typeface("DejaVuSans.ttf", 14)
    col_w = (SIDE - 2 * EDGE - 3 * GAP) // 4
    for n, idx in enumerate(BRIEF_IDX):
        text = "\u2022 " + NEWS[idx]["head"]
        col, row = n // 5, n % 5
        x = EDGE + col * (col_w + GAP)
        y = body_y + row * 28
        if d.textlength(text, font=face) > col_w + 4:
            raise ValueError("brief too wide: %r" % text)
        if y + 18 > SIDE - 32:
            raise ValueError("briefs run past the footer")
        d.text((x, y), text, font=face, fill=PALETTE["ink"])


def paint_footer(pg):
    d = pg.d
    d.rectangle([0, SIDE - 30, SIDE, SIDE], fill=PALETTE["foot"])
    d.line([(0, SIDE - 30), (SIDE, SIDE - 30)], fill=PALETTE["hairline"], width=1)
    d.text((24, SIDE - 22),
           "48 stories checked for 19 Nov 2026  \u00b7  Sources: Reuters  \u00b7  BBC  \u00b7  AP  \u00b7  Al Jazeera  \u00b7  Le Monde  \u00b7  NYT",
           font=pg.typeface("DejaVuSans.ttf", 16), fill=PALETTE["grey"])


def draw_page(Image, ImageDraw, ImageFont):
    global _warn_font
    canvas = Image.new("RGB", (SIDE, SIDE), PALETTE["paper"])
    pg = Page(canvas, ImageDraw.Draw(canvas), ImageFont)
    _warn_font = pg.typeface("DejaVuSans-Bold.ttf", 26)
    paint_masthead(pg)
    after_leads = paint_lead_cards(pg, MASTHEAD_H + GOLD_RULE + 8)
    after_map = paint_map_and_numbers(pg, after_leads + 10)
    after_small = paint_small_cards(pg, after_map + 10)
    paint_briefs(pg, after_small)
    paint_footer(pg)
    os.makedirs(os.path.dirname(DEST), exist_ok=True)
    canvas.save(DEST, format="PNG", optimize=True)
    # Guard: never ship a wrong-sized image — fail loudly instead of
    # silently writing a bad file (the fallback copy stays byte-identical).
    with Image.open(DEST) as shot:
        assert shot.size == (SIDE, SIDE), shot.size
    print("wrote", DEST, canvas.size)


def main():
    try:
        from PIL import Image, ImageDraw, ImageFont
    except ImportError:
        copy_shipped()
        return
    try:
        draw_page(Image, ImageDraw, ImageFont)
    except Exception:
        copy_shipped()


if __name__ == "__main__":
    main()
