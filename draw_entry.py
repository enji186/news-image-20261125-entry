#!/usr/bin/env python3
"""Build-time script: draw entry.png for news-image-20261125.

Draws a 1024x1024 PNG summing up the world news of Wednesday
25 November 2026. Run once to produce entry.png; main.py only
verifies and copies the bundled image (no drawing at run time).
"""
import os

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")

NAVY = (13, 27, 46)
CARD = (24, 42, 66)
CARD_EDGE = (52, 84, 120)
WHITE = (245, 247, 250)
MUTED = (178, 196, 214)
GOLD = (212, 175, 55)
TEAL = (45, 190, 178)
AMBER = (232, 158, 46)
GREEN = (96, 190, 110)
RED = (226, 92, 92)
BLUE = (96, 158, 232)

FONT_DIR = "/usr/share/fonts/truetype/dejavu"
BOLD = os.path.join(FONT_DIR, "DejaVuSans-Bold.ttf")
REG = os.path.join(FONT_DIR, "DejaVuSans.ttf")


def font(path, size):
    return ImageFont.truetype(path, size)


def draw_globe(d, cx, cy, r):
    """Simple wireframe globe in the header."""
    d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=GOLD, width=4)
    d.ellipse([cx - r // 2, cy - r, cx + r // 2, cy + r], outline=GOLD, width=2)
    d.line([cx - r, cy, cx + r, cy], fill=GOLD, width=2)
    d.arc([cx - r, cy - r // 2, cx + r, cy + r // 2], 0, 360, fill=GOLD, width=2)
    d.arc([cx - r, cy - r, cx + r, cy + r], 200, 340, fill=GOLD, width=2)


def main():
    img = Image.new("RGB", (W, H), NAVY)
    d = ImageDraw.Draw(img)

    # Header
    d.text((48, 44), "THE WORLD IN ONE DAY", font=font(BOLD, 30), fill=GOLD)
    draw_globe(d, 930, 62, 38)
    d.text((48, 82), "25 NOVEMBER 2026", font=font(BOLD, 70), fill=WHITE)
    d.text(
        (48, 172),
        "Wednesday  \u00b7  Early edition \u2014 news reported by 15:45 CST",
        font=font(REG, 26),
        fill=MUTED,
    )
    d.line([48, 216, 976, 216], fill=GOLD, width=3)

    stories = [
        ("SPACE", TEAL, "China launches Shenzhou-24",
         "First foreign astronaut aboard Tiangong; liftoff at 08:18."),
        ("MIDDLE EAST", AMBER, "Two tankers hit mines in Hormuz",
         "Iran says the ships caught fire on an unauthorised route."),
        ("MIDDLE EAST", AMBER, "Houthis claim Riyadh tower strike",
         "Second hit on the capital's tallest tower in a week; 11 injured."),
        ("ASIA", GREEN, "Seoul subway strike called off",
         "Last-minute wage deal at 2:40 a.m. keeps Lines 1\u20138 running normally."),
        ("LATIN AMERICA", RED, "Cartagena supermarket siege ends",
         "Forces move in as hostages are freed after a day-long standoff."),
    ]

    y = 240
    block_h, gap = 132, 10
    for tag, color, headline, detail in stories:
        d.rounded_rectangle([48, y, 976, y + block_h], radius=14,
                            fill=CARD, outline=CARD_EDGE, width=2)
        d.rectangle([48, y + 14, 58, y + block_h - 14], fill=color)
        d.text((76, y + 14), tag, font=font(BOLD, 23), fill=color)
        d.text((76, y + 44), headline, font=font(BOLD, 37), fill=WHITE)
        d.text((76, y + 94), detail, font=font(REG, 26), fill=MUTED)
        y += block_h + gap

    d.text((48, 962),
           "Sources: Xinhua \u00b7 CNA \u00b7 IRNA \u00b7 Arab News \u00b7 SCMP \u00b7 Yonhap \u00b7 Al Jazeera \u00b7 Ynet",
           font=font(REG, 21), fill=MUTED)

    img.save(OUT, format="PNG", optimize=True)
    print("wrote", OUT, os.path.getsize(OUT), "bytes")


if __name__ == "__main__":
    main()
