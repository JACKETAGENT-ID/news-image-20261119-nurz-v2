#!/usr/bin/env python3
"""Compose the globe-edition entry.png for news-image-20261119 (nurz v2).

Builds a 1024x1024 PNG: deep-navy background, a big masthead naming the
day, a generated globe at the centre, and five story callouts radiating
around it. Run:  python3 compose.py   (writes entry.png next to this file)
"""
import os
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
GLOBE = os.path.join(
    HERE, "assets",
    "media-generation-globe-hero-0-6b6b858d-266b-4c1a-a441-10e069e7044b.png")
OUT = os.path.join(HERE, "entry.png")

W, H = 1024, 1024
NAVY = (8, 18, 43)
GOLD = (212, 175, 105)
GOLD_BRIGHT = (232, 196, 130)
WHITE = (245, 247, 250)
MIST = (196, 208, 224)

FONT_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
FONT_REG = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, width):
    """Greedy word wrap to the given pixel width."""
    words = text.split()
    lines, cur = [], ""
    for word in words:
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=fnt) <= width:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


STORIES = [
    # (number, place, field, headline, summary, fact, box)
    (1, "SHENZHEN", "SUMMIT",
     "Three leaders, one table",
     "Trump, Xi and Putin hold a first three-way summit in Shenzhen.",
     "Ukraine tops the agenda.",
     (22, 185, 284, 450)),
    (2, "THE HAGUE", "JUSTICE",
     "World court rules today",
     "The ICJ delivers its verdict on the Rohingya genocide case.",
     "First state genocide verdict ever.",
     (740, 185, 1002, 450)),
    (3, "THE GULF", "CONFLICT",
     "Gulf strikes escalate",
     "Iran hits Gulf states after a US strike on Qeshm island.",
     "Tanker hit in the Strait of Hormuz.",
     (22, 525, 284, 790)),
    (4, "NEW YORK", "MARKETS",
     "A record market debut",
     "Anthropic starts trading as ANT after a record $81.3bn IPO.",
     "Priced at $83 a share; about $1.5tn value.",
     (740, 525, 1002, 790)),
    (5, "ANTALYA", "CLIMATE",
     "Climate talks race on",
     "Ministers push through the night to unblock a COP31 deal.",
     "Final text due tonight.",
     (332, 720, 692, 905)),
]


def main():
    img = Image.new("RGB", (W, H), NAVY)
    draw = ImageDraw.Draw(img, "RGBA")

    # --- starfield speckle for depth (fixed seed pattern, deterministic) ---
    import random
    rng = random.Random(20261119)
    for _ in range(260):
        x = rng.randint(0, W - 1)
        y = rng.randint(0, H - 1)
        r = rng.randint(1, 2)
        a = rng.randint(40, 130)
        draw.ellipse([x - r, y - r, x + r, y + r], fill=(255, 255, 255, a))

    # --- masthead ---
    f_kicker = font(FONT_BOLD, 25)
    f_date = font(FONT_BOLD, 66)
    kicker = "T H U R S D A Y   ·   T H E   W O R L D   I N   O N E   I M A G E"
    tw = draw.textlength(kicker, font=f_kicker)
    draw.text(((W - tw) / 2, 30), kicker, font=f_kicker, fill=GOLD_BRIGHT)
    date = "19 NOVEMBER 2026"
    tw = draw.textlength(date, font=f_date)
    draw.text(((W - tw) / 2, 62), date, font=f_date, fill=WHITE)
    draw.line([(W / 2 - 180, 148), (W / 2 + 180, 148)], fill=GOLD, width=3)
    draw.ellipse([W / 2 - 5, 143, W / 2 + 5, 153], fill=GOLD)

    # --- globe (circular crop, gold ring) ---
    globe = Image.open(GLOBE).convert("RGB")
    side = min(globe.size)
    globe = globe.crop(((globe.width - side) // 2, (globe.height - side) // 2,
                        (globe.width + side) // 2, (globe.height + side) // 2))
    R = 215
    CX, CY = 512, 478
    globe = globe.resize((2 * R, 2 * R), Image.LANCZOS)
    mask = Image.new("L", (2 * R, 2 * R), 0)
    md = ImageDraw.Draw(mask)
    md.ellipse([0, 0, 2 * R - 1, 2 * R - 1], fill=255)
    img.paste(globe, (CX - R, CY - R), mask)
    draw.ellipse([CX - R - 3, CY - R - 3, CX + R + 3, CY + R + 3],
                 outline=GOLD, width=3)

    # --- callout panels ---
    f_tag = font(FONT_BOLD, 14)
    f_head = font(FONT_BOLD, 26)
    f_body = font(FONT_REG, 19)
    f_fact = font(FONT_BOLD, 18)

    for num, place, field, head, summ, fact, (x0, y0, x1, y1) in STORIES:
        # connector: box edge nearest globe centre -> globe rim
        bcx, bcy = (x0 + x1) / 2, (y0 + y1) / 2
        dx, dy = CX - bcx, CY - bcy
        dist = (dx * dx + dy * dy) ** 0.5
        ux, uy = dx / dist, dy / dist
        # start at box edge along the direction
        sx = bcx + ux * ((x1 - x0) / 2 + 4)
        sy = bcy + uy * ((y1 - y0) / 2 + 4)
        ex = CX - ux * (R + 4)
        ey = CY - uy * (R + 4)
        draw.line([(sx, sy), (ex, ey)], fill=GOLD, width=2)
        draw.ellipse([ex - 5, ey - 5, ex + 5, ey + 5], fill=GOLD)

        # panel
        overlay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        od = ImageDraw.Draw(overlay)
        od.rounded_rectangle([x0, y0, x1, y1], radius=14,
                             fill=(13, 32, 66, 228), outline=GOLD, width=2)
        img.paste(Image.alpha_composite(img.convert("RGBA"), overlay)
                  .convert("RGB"), (0, 0))
        draw = ImageDraw.Draw(img, "RGBA")

        pad = 16
        tx = x0 + pad
        ty = y0 + 14
        inner = (x1 - x0) - 2 * pad
        # number badge, top-left, tag on one line beside it
        bx, by = x0 + 30, y0 + 28
        draw.ellipse([bx - 14, by - 14, bx + 14, by + 14], fill=GOLD)
        f_num = font(FONT_BOLD, 20)
        nw = draw.textlength(str(num), font=f_num)
        nh = draw.textbbox((0, 0), str(num), font=f_num)
        draw.text((bx - nw / 2, by - (nh[3] - nh[1]) / 2 - 2), str(num),
                  font=f_num, fill=NAVY)
        draw.text((tx + 34, ty), place + "  ·  " + field, font=f_tag,
                  fill=GOLD_BRIGHT)
        ty += 30
        for line in wrap(draw, head, f_head, inner):
            draw.text((tx, ty), line, font=f_head, fill=WHITE)
            ty += 33
        ty += 4
        for line in wrap(draw, summ, f_body, inner):
            draw.text((tx, ty), line, font=f_body, fill=MIST)
            ty += 26
        ty += 6
        draw.line([(tx, ty), (tx + 42, ty)], fill=GOLD, width=2)
        ty += 8
        for line in wrap(draw, fact, f_fact, inner):
            draw.text((tx, ty), line, font=f_fact, fill=GOLD_BRIGHT)
            ty += 24

    # --- footer ---
    f_foot = font(FONT_REG, 18)
    foot = "All five stories happened or were first reported on 19 November 2026"
    tw = draw.textlength(foot, font=f_foot)
    draw.text(((W - tw) / 2, 968), foot, font=f_foot, fill=MIST)

    img.save(OUT, "PNG", optimize=True)
    print("wrote", OUT, os.path.getsize(OUT), "bytes")


if __name__ == "__main__":
    main()
