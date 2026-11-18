#!/usr/bin/env python3
"""Draw the 18 November 2026 world-news poster and save it as entry.png.

A newspaper front page: masthead and date on top, one lead story about
the US-Iran escalation in the Gulf, then five shorter stories below it.
Every pictogram is drawn here from plain shapes - no photos, no copied art.
Flat colours only, so the PNG stays small and the text stays readable
even when the picture is shown at about 300 pixels wide.
"""

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
OUT = "entry.png"

PAPER = (253, 251, 245)
INK = (17, 17, 17)
RED = (185, 28, 28)
BLUE = (29, 78, 216)
TEAL = (13, 116, 128)
GOLD = (180, 130, 29)
GREEN = (21, 128, 61)
GREY = (90, 90, 90)
LIGHT = (238, 234, 224)

SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_w):
    """Split text into lines that fit inside max_w pixels."""
    lines, cur = [], ""
    for word in text.split(" "):
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def para(draw, x, y, text, fnt, max_w, fill, spacing=6):
    """Draw wrapped text, return the y just below the last line."""
    for line in wrap(draw, text, fnt, max_w):
        draw.text((x, y), line, font=fnt, fill=fill)
        y += fnt.size + spacing
    return y


def waves(draw, x, y, w, h, colour):
    """Three stacked wave strokes inside a box starting at (x, y)."""
    for i in range(3):
        yy = y + 8 + i * 14
        pts = []
        for px in range(x, x + w + 1, 8):
            import math
            pts.append((px, yy + 5 * math.sin((px - x) / w * 6.28)))
        draw.line(pts, fill=colour, width=4)


def pic_gulf(draw, x, y, s):
    """Lead pictogram: a ship on waves under a jet, in a framed box."""
    draw.rectangle([x, y, x + s, y + s], outline=INK, width=3, fill=(219, 234, 254))
    # jet: a delta shape pointing right, with a tail fin on top
    draw.polygon([(x + s * 0.18, y + s * 0.30), (x + s * 0.82, y + s * 0.22),
                  (x + s * 0.86, y + s * 0.30), (x + s * 0.82, y + s * 0.34),
                  (x + s * 0.30, y + s * 0.40)], fill=INK)
    draw.polygon([(x + s * 0.40, y + s * 0.28), (x + s * 0.48, y + s * 0.12),
                  (x + s * 0.56, y + s * 0.28)], fill=INK)
    # ship hull and cabin
    draw.polygon([(x + s * 0.18, y + s * 0.62), (x + s * 0.82, y + s * 0.62),
                  (x + s * 0.72, y + s * 0.78), (x + s * 0.28, y + s * 0.78)],
                 fill=RED)
    draw.rectangle([x + s * 0.42, y + s * 0.46, x + s * 0.58, y + s * 0.62],
                   fill=INK)
    draw.line([x + s * 0.50, y + s * 0.34, x + s * 0.50, y + s * 0.46],
              fill=INK, width=4)
    waves(draw, x + 10, y + s - 44, s - 20, 20, BLUE)


def pic_bridge(draw, x, y, s):
    """Broken bridge: two deck pieces with a gap, held by two towers."""
    draw.rectangle([x, y, x + s, y + s], outline=INK, width=3, fill=(254, 226, 226))
    mid = x + s // 2
    draw.line([x + 8, y + s * 0.62, mid - 14, y + s * 0.62], fill=INK, width=8)
    draw.line([mid + 14, y + s * 0.62, x + s - 8, y + s * 0.62], fill=INK, width=8)
    for tx in (x + s * 0.22, x + s * 0.74):
        draw.line([tx, y + s * 0.18, tx, y + s * 0.62], fill=INK, width=7)
        draw.line([tx - 16, y + s * 0.18, tx + 16, y + s * 0.18], fill=INK, width=7)
    draw.line([mid - 14, y + s * 0.62, mid + 6, y + s * 0.90], fill=RED, width=6)
    draw.line([mid + 14, y + s * 0.62, mid - 6, y + s * 0.90], fill=RED, width=6)
    draw.line([x + 8, y + s * 0.90, x + s - 8, y + s * 0.90], fill=BLUE, width=5)


def pic_summit(draw, x, y, s):
    """Three leaders at one table: three coloured circles, one table."""
    draw.rectangle([x, y, x + s, y + s], outline=INK, width=3, fill=(220, 252, 231))
    for i, col in enumerate((RED, BLUE, GOLD)):
        cx = x + s * (0.25 + i * 0.25)
        cy = y + s * 0.38
        draw.ellipse([cx - 20, cy - 20, cx + 20, cy + 20], fill=col)
        draw.rectangle([cx - 19, cy + 20, cx + 19, y + s * 0.66], fill=col)
    draw.rectangle([x + 8, y + s * 0.66, x + s - 8, y + s * 0.78], fill=INK)
    draw.rectangle([x + s * 0.30, y + s * 0.78, x + s * 0.36, y + s - 10], fill=INK)
    draw.rectangle([x + s * 0.64, y + s * 0.78, x + s * 0.70, y + s - 10], fill=INK)


def pic_vote(draw, x, y, s):
    """Ballot box with a star above it."""
    draw.rectangle([x, y, x + s, y + s], outline=INK, width=3, fill=(219, 234, 254))
    cx, cy, r = x + s // 2, y + s * 0.30, 26
    star = []
    import math
    for i in range(10):
        ang = -math.pi / 2 + i * math.pi / 5
        rr = r if i % 2 == 0 else r * 0.45
        star.append((cx + rr * math.cos(ang), cy + rr * math.sin(ang)))
    draw.polygon(star, fill=GOLD)
    draw.rectangle([x + s * 0.20, y + s * 0.56, x + s * 0.80, y + s * 0.88],
                   fill=INK)
    draw.rectangle([x + s * 0.38, y + s * 0.48, x + s * 0.62, y + s * 0.58],
                   fill=PAPER)
    draw.line([x + s * 0.30, y + s * 0.72, x + s * 0.46, y + s * 0.84,
               x + s * 0.72, y + s * 0.62], fill=PAPER, width=6)


def pic_health(draw, x, y, s):
    """Medical cross in a circle, with small dots for cases."""
    draw.rectangle([x, y, x + s, y + s], outline=INK, width=3, fill=(254, 226, 226))
    cx, cy = x + s // 2, y + s * 0.42
    draw.ellipse([cx - 34, cy - 34, cx + 34, cy + 34], fill=RED)
    draw.rectangle([cx - 9, cy - 24, cx + 9, cy + 24], fill=PAPER)
    draw.rectangle([cx - 24, cy - 9, cx + 24, cy + 9], fill=PAPER)
    for dx in (-28, 0, 28):
        draw.ellipse([x + s // 2 + dx - 6, y + s * 0.80 - 6,
                      x + s // 2 + dx + 6, y + s * 0.80 + 6], fill=INK)


def pic_storm(draw, x, y, s):
    """Cyclone spiral: concentric arcs winding into the centre."""
    draw.rectangle([x, y, x + s, y + s], outline=INK, width=3, fill=(207, 250, 254))
    cx, cy = x + s // 2, y + s // 2
    k = s / 88
    for r, a0, a1 in ((40, 0, 300), (30, 90, 360), (20, 180, 420), (10, 270, 480)):
        rr = r * k
        draw.arc([cx - rr, cy - rr, cx + rr, cy + rr], a0, a1, fill=TEAL, width=7)
    draw.ellipse([cx - 5, cy - 5, cx + 5, cy + 5], fill=RED)


def story(draw, x, y, w, pic, headline, summary, hsize=25, ssize=18, ps=88):
    """One secondary story: pictogram on the left, headline and summary."""
    pic(draw, x, y, ps)
    tx = x + ps + 16
    tw = w - ps - 16
    yy = para(draw, tx, y + 2, headline, font(SANS_B, hsize), tw, INK, spacing=4)
    para(draw, tx, yy + 2, summary, font(SANS, ssize), tw, INK, spacing=3)


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # --- masthead ---
    d.line([36, 28, W - 36, 28], fill=INK, width=4)
    d.text((W // 2, 44), "THE WORLD TODAY", font=font(SERIF_B, 84),
           fill=INK, anchor="ma")
    d.line([36, 140, W - 36, 140], fill=INK, width=2)
    d.text((W // 2, 150), "ONE PAGE  •  WORLD NEWS  •  FREE TO READ",
           font=font(SANS, 20), fill=GREY, anchor="ma")

    # --- date banner, the most prominent line after the name ---
    d.rectangle([36, 184, W - 36, 238], fill=INK)
    d.text((W // 2, 196), "WEDNESDAY 18 NOVEMBER 2026", font=font(SANS_B, 34),
           fill=PAPER, anchor="ma")

    # --- lead story ---
    d.text((36, 258), "LEAD STORY", font=font(SANS_B, 22), fill=RED)
    lead_head = "U.S. JETS HIT QESHM MISSILE SITE"
    y = para(d, 36, 286, lead_head, font(SERIF_B, 40), 660, INK, spacing=4)
    lead_sum = ("U.S. jets struck a Revolutionary Guard missile launch site on "
                "Qeshm Island on Tuesday. Iran fired drones at a U.S. radar "
                "site in Bahrain, its third attack there in under a week. "
                "The U.S. said it sank five Iranian oil tankers in the Gulf "
                "of Oman; Iran said it attacked ten ships near the Strait of "
                "Hormuz, fired missiles at U.S. forces at the Al-Azraq base "
                "in Jordan, and announced a maritime restricted area from "
                "Chabahar into the Gulf of Oman and the Arabian Sea.")
    para(d, 36, y + 8, lead_sum, font(SANS, 20), 660, INK, spacing=4)
    pic_gulf(d, 736, 286, 216)

    d.line([36, 600, W - 36, 600], fill=INK, width=3)

    # --- five secondary stories ---
    col_w = (W - 72 - 28) // 2
    story(d, 36, 618, col_w, pic_bridge,
          "KERCH BRIDGE HIT FOR A SECOND DAY",
          "Part of its road span fell into the strait and the bridge shut "
          "down. Russia hit two major bridges of its own ahead of "
          "Thursday's summit.")
    story(d, 36 + col_w + 28, 618, col_w, pic_summit,
          "XI, PUTIN AND TRUMP TO MEET IN SHENZHEN",
          "The three leaders meet in Shenzhen this week. Trump arrived in "
          "Manila for Quad talks ahead of a visit to China.")
    story(d, 36, 763, col_w, pic_vote,
          "PELTOLA WINS ALASKA SENATE SEAT",
          "Democrat Mary Peltola won Alaska's Senate seat, giving the "
          "Democrats 56 seats in the Senate.")
    story(d, 36 + col_w + 28, 763, col_w, pic_health,
          "EBOLA CASES MORE THAN DOUBLE IN CONGO",
          "The outbreak in DR Congo has passed 11,000 cases and 5,400 "
          "deaths in three months, the UN said.")
    d.line([36, 902, W - 36, 902], fill=INK, width=2)
    story(d, 36, 916, W - 72, pic_storm,
          "CYCLONE XAVIER HITS THE NORTHERN COOK ISLANDS",
          "Cyclone Xavier, a Category 5 storm, hits the Northern Cook Islands.",
          hsize=26, ssize=20, ps=72)

    d.line([36, 996, W - 36, 996], fill=INK, width=4)
    img.save(OUT, optimize=True)
    print(f"saved {OUT}: {img.size[0]}x{img.size[1]}")


if __name__ == "__main__":
    main()
