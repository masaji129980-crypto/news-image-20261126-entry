#!/usr/bin/env python3
"""Draw the front page of THE WORLD for Thursday 26 November 2026.

Original newspaper-style image, drawn entirely in code with Pillow.
Stories are the day's most consequential world news, gathered from
multiple news sources on 26 November 2026 (see README.md).
Layout is flowing: each block returns its bottom y, so nothing overlaps.
Output: entry.png, 1024x1024, well under the 1 MiB limit.
"""
import math
import os
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (248, 243, 232)
INK = (26, 26, 26)
RED = (164, 30, 34)
BLUE = (31, 58, 95)
GREY = (110, 105, 95)
PANEL = (222, 232, 240)

FONT_DIR = "/usr/share/fonts/truetype/dejavu"
SERIF = os.path.join(FONT_DIR, "DejaVuSerif-Bold.ttf")
SERIF_REG = os.path.join(FONT_DIR, "DejaVuSerif.ttf")
SANS = os.path.join(FONT_DIR, "DejaVuSans.ttf")
SANS_B = os.path.join(FONT_DIR, "DejaVuSans-Bold.ttf")


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_w):
    """Greedy word wrap returning a list of lines."""
    lines, cur = [], ""
    for word in text.split():
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


def para(draw, x, y, text, fnt, max_w, leading, fill=INK):
    """Draw wrapped paragraph, return y after last line."""
    for line in wrap(draw, text, fnt, max_w):
        draw.text((x, y), line, font=fnt, fill=fill)
        y += leading
    return y


def rule(draw, x0, y, x1, width=2, fill=INK):
    draw.line([(x0, y), (x1, y)], fill=fill, width=width)


def draw_globe(draw, cx, cy, r):
    """Simple line globe: circle, meridians, parallels, trade arrows."""
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], outline=BLUE, width=4,
                 fill=(235, 240, 246))
    for k in (0.45, 0.8):
        draw.ellipse([cx - r * k, cy - r, cx + r * k, cy + r],
                     outline=BLUE, width=2)
    for dy in (-r * 0.45, 0, r * 0.45):
        xw = (r * r - dy * dy) ** 0.5
        draw.line([(cx - xw, cy + dy), (cx + xw, cy + dy)], fill=BLUE, width=2)
    for ang, col in ((205, RED), (335, RED)):
        a = math.radians(ang)
        x0 = cx + int((r + 24) * math.cos(a))
        y0 = cy + int((r + 24) * math.sin(a))
        x1 = cx + int((r + 48) * math.cos(a))
        y1 = cy + int((r + 48) * math.sin(a))
        draw.line([(x0, y0), (x1, y1)], fill=col, width=4)
        draw.polygon([(x1, y1), (x1 - 12, y1 - 2), (x1 - 2, y1 - 12)],
                     fill=col)


def draw_flame(draw, x, y, s, col=RED):
    """Stylised flame icon, s = height in px."""
    pts = [(x, y + s), (x + s * 0.22, y + s * 0.55),
           (x + s * 0.12, y + s * 0.42), (x + s * 0.38, y + s * 0.12),
           (x + s * 0.5, y + s * 0.38), (x + s * 0.62, y),
           (x + s * 0.72, y + s * 0.45), (x + s * 0.88, y + s * 0.55),
           (x + s, y + s)]
    draw.polygon(pts, fill=col)
    draw.polygon([(x + s * 0.35, y + s), (x + s * 0.5, y + s * 0.55),
                  (x + s * 0.65, y + s)], fill=(232, 140, 40))


def draw_satellite(draw, x, y, s):
    """Stylised satellite icon."""
    draw.rectangle([x + s * 0.35, y + s * 0.3, x + s * 0.65, y + s * 0.62],
                   fill=BLUE, outline=INK, width=2)
    draw.rectangle([x, y + s * 0.35, x + s * 0.32, y + s * 0.58],
                   fill=(120, 160, 200), outline=INK, width=2)
    draw.rectangle([x + s * 0.68, y + s * 0.35, x + s, y + s * 0.58],
                   fill=(120, 160, 200), outline=INK, width=2)
    draw.line([(x + s * 0.5, y + s * 0.62), (x + s * 0.5, y + s * 0.85)],
              fill=INK, width=3)
    draw.arc([x + s * 0.3, y + s * 0.7, x + s * 0.7, y + s], 0, 180,
             fill=INK, width=3)


def draw_cross(draw, x, y, s):
    """Simple memorial cross icon."""
    draw.rectangle([x + s * 0.42, y, x + s * 0.58, y + s], fill=GREY)
    draw.rectangle([x, y + s * 0.18, x + s, y + s * 0.42], fill=GREY)
    draw.ellipse([x + s * 0.42, y - s * 0.12, x + s * 0.58, y + s * 0.04],
                 fill=RED)


def draw_badge(draw, x, y, s):
    """Police shield icon."""
    pts = [(x, y), (x + s, y), (x + s, y + s * 0.55),
           (x + s * 0.5, y + s), (x, y + s * 0.55)]
    draw.polygon(pts, fill=BLUE, outline=INK)
    draw.text((x + s * 0.5, y + s * 0.42), "*", font=font(SANS_B, int(s * 0.55)),
              fill=(255, 255, 255), anchor="mm")


def draw_oil(draw, x, y, s):
    """Oil derrick icon."""
    draw.polygon([(x + s * 0.1, y + s), (x + s * 0.35, y),
                  (x + s * 0.65, y), (x + s * 0.9, y + s)], outline=INK,
                 width=4)
    draw.line([(x + s * 0.42, y + s * 0.25), (x + s * 0.58, y + s * 0.25)],
              fill=INK, width=4)
    draw.line([(x + s * 0.2, y + s * 0.6), (x + s * 0.8, y + s * 0.6)],
              fill=INK, width=4)
    draw.ellipse([x + s * 0.42, y + s * 0.7, x + s * 0.58, y + s * 0.86],
                 fill=INK)


def story_block(draw, x, y, w, kicker, headline, body, icon=None,
                head_size=24, body_size=15):
    """One story: kicker, headline, body; optional icon at top-left.
    Returns y after the last body line."""
    ix = x
    if icon is not None:
        icon(draw, x, y + 2, 36)
        ix = x + 46
    draw.text((ix, y), kicker, font=font(SANS_B, 13), fill=RED)
    y = para(draw, ix, y + 20, headline, font(SERIF, head_size),
             w - (ix - x), head_size + 5)
    y = para(draw, x, y + 4, body, font(SANS, body_size), w, body_size + 6)
    return y


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    M = 36  # margin

    # outer border
    d.rectangle([M - 8, M - 8, W - M + 8, H - M + 8], outline=INK, width=3)

    # ---- dateline bar ----
    d.text((M, 44), "No. 330", font=font(SANS, 14), fill=GREY)
    d.text((W // 2, 44), "THURSDAY, 26 NOVEMBER 2026",
           font=font(SANS_B, 17), fill=INK, anchor="mt")
    d.text((W - M, 44), "ONE DAY IN THE WORLD", font=font(SANS, 14),
           fill=GREY, anchor="rt")
    rule(d, M, 70, W - M, 2)

    # ---- masthead ----
    d.text((W // 2, 82), "THE WORLD", font=font(SERIF, 96), fill=INK,
           anchor="ma")
    rule(d, M, 190, W - M, 4)
    rule(d, M, 196, W - M, 1)
    d.text((W // 2, 206), "THE DAY'S NEWS FROM EVERY CORNER OF THE GLOBE",
           font=font(SANS_B, 14), fill=GREY, anchor="ma")

    # ---- lead story: tariffs ----
    ly = 238
    d.text((M, ly), "LEAD STORY  •  TRADE", font=font(SANS_B, 14), fill=RED)
    y = para(d, M, ly + 24, "TRUMP UNVEILS SWEEPING TARIFFS ON 14 ECONOMIES",
             font(SERIF, 40), 600, 46)
    y = para(d, M, y + 6,
             "Washington proposes duties of up to 35% on China, the EU and "
             "12 others from January 2027.",
             font(SERIF_REG, 19), 600, 25)
    y = para(d, M, y + 8,
             "The US Trade Representative ruled the 14 economies' "
             "overcapacity practices unreasonable. Asian markets fell as "
             "exporters braced for the levies.",
             font(SANS, 15), 600, 21)

    # lead illustration: globe + top rate
    px0, py0, px1, py1 = 668, 240, W - M, 428
    d.rectangle([px0, py0, px1, py1], fill=PANEL, outline=INK, width=2)
    draw_globe(d, (px0 + px1) // 2 - 68, (py0 + py1) // 2 - 8, 58)
    d.text((px1 - 14, py0 + 16), "UP TO", font=font(SANS_B, 16), fill=GREY,
           anchor="ra")
    d.text((px1 - 14, py0 + 38), "35%", font=font(SERIF, 52), fill=RED,
           anchor="ra")
    d.text((px1 - 14, py0 + 100), "NEW DUTIES", font=font(SANS_B, 15),
           fill=INK, anchor="ra")
    d.text(((px0 + px1) // 2, py1 - 12), "TRADE WAR, ROUND TWO",
           font=font(SANS_B, 13), fill=BLUE, anchor="mb")

    y = max(y, py1) + 16
    rule(d, M, y, W - M, 2)

    # ---- row A: energy + Cairo ----
    ay = y + 16
    col_w = (W - 2 * M - 28) // 2
    end_l = story_block(d, M, ay, col_w, "MIDDLE EAST  •  ENERGY",
                        "Houthis claim Saudi refinery attack; Brent tops $94",
                        "Yemen's Houthis said they hit the Ras Tanura refinery "
                        "and Riyadh's financial district. Brent jumped to "
                        "$94.61 a barrel.",
                        icon=draw_oil)
    end_r = story_block(d, M + col_w + 28, ay, col_w, "EGYPT  •  DISASTER",
                        "Cairo tanker fire kills at least 31 on ring road",
                        "A tanker crash set the highway around Cairo ablaze, "
                        "killing at least 31 in one of Egypt's worst road "
                        "disasters.",
                        icon=draw_flame)
    y = max(end_l, end_r) + 14
    rule(d, M, y, W - M, 1)

    # ---- row B: Ukraine war toll + Colombia ----
    by = y + 16
    end_l = story_block(d, M, by, col_w, "UKRAINE  •  WAR",
                        "Russia's own figures show nearly 500,000 war dead",
                        "Moscow's data put its military deaths in Ukraine near "
                        "half a million; Kyiv said it hit two Russian ships "
                        "off Libya.",
                        icon=draw_cross)
    end_r = story_block(d, M + col_w + 28, by, col_w, "COLOMBIA  •  RESCUE",
                        "Police free 20 hostages after 17-hour supermarket siege",
                        "Gunmen held 20 people in a supermarket for 17 hours. "
                        "Police stormed in and freed them all alive.",
                        icon=draw_badge)
    y = max(end_l, end_r) + 14
    rule(d, M, y, W - M, 1)

    # ---- row C: SpaceX, full width ----
    cy = y + 16
    draw_satellite(d, M, cy + 2, 40)
    d.text((M + 52, cy), "SPACE  •  TECHNOLOGY", font=font(SANS_B, 13),
           fill=RED)
    d.text((M + 52, cy + 20),
           "SpaceX cleared to launch one million AI data-centre satellites",
           font=font(SERIF, 24), fill=INK)
    d.text((M + 52, cy + 54),
           "US regulators approved a vast orbital fleet to beam computing power from space.",
           font=font(SANS, 15), fill=INK)
    y = cy + 84
    rule(d, M, y, W - M, 2)

    # ---- footer strip ----
    fy = y + 12
    d.text((M, fy), "ALSO TODAY:", font=font(SANS_B, 13), fill=RED)
    d.text((M + 108, fy),
           "Norway court voids oil licences  •  Macy's Thanksgiving parade "
           "postponed by storm  •  US Army detonates lead stockpile",
           font=font(SANS, 13), fill=GREY)
    print("footer ends at y =", fy + 18, "(page height", H, ")")

    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")
    img.save(out, "PNG", optimize=True)
    print("wrote", out, os.path.getsize(out), "bytes")


if __name__ == "__main__":
    main()
