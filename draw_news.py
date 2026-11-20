#!/usr/bin/env python3
"""Draw a 1024x1024 newspaper front page summing up 20 November 2026.

Deterministic: fixed text, fixed colours, fixed geometry. No network,
no timestamps, no randomness. Running it twice produces a byte-identical
entry.png.
"""

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (247, 243, 234)
INK = (17, 17, 17)
GREY = (90, 86, 78)
RED = (160, 30, 30)
RULE = (60, 58, 52)

SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, width):
    """Greedy word wrap to a pixel width; returns a list of lines."""
    lines, cur = [], ""
    for word in text.split(" "):
        trial = word if not cur else cur + " " + word
        if draw.textlength(trial, font=fnt) <= width:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def para(draw, x, y, text, fnt, width, leading, fill=INK):
    for line in wrap(draw, text, fnt, width):
        draw.text((x, y), line, font=fnt, fill=fill)
        y += leading
    return y


def kicker(draw, x, y, text):
    fnt = font(SANS_B, 17)
    draw.text((x, y), text.upper(), font=fnt, fill=RED)
    return y + 22


def hrule(draw, x0, x1, y, width=2, fill=RULE):
    draw.line([(x0, y), (x1, y)], fill=fill, width=width)


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    mx = 48  # side margin

    # ---- Masthead ----
    y = 30
    title = "THE WORLD IN ONE DAY"
    tf = font(SERIF_B, 60)
    tw = d.textlength(title, font=tf)
    d.text(((W - tw) / 2, y), title, font=tf, fill=INK)
    y += 72
    hrule(d, mx, W - mx, y, width=3)
    y += 10
    dateline = "FRIDAY, 20 NOVEMBER 2026  -  THE DAY'S WORLD NEWS IN A SINGLE IMAGE"
    df = font(SANS_B, 18)
    dw = d.textlength(dateline, font=df)
    d.text(((W - dw) / 2, y), dateline, font=df, fill=GREY)
    y += 30
    hrule(d, mx, W - mx, y, width=3)
    y += 18

    # ---- Lead story: Trump, Xi, Putin ----
    y = kicker(d, mx, y, "Lead story - Shenzhen, China")
    y = para(
        d, mx, y,
        "Trump, Xi and Putin sign 'peace declaration'",
        font(SERIF_B, 44), W - 2 * mx, 52,
    )
    y += 4
    y = para(
        d, mx, y,
        "The leaders of the United States, China and Russia met for the first "
        "time ever as a trio on the sidelines of the APEC summit in Shenzhen, "
        "declaring that \"a nuclear war cannot be won and must never be "
        "fought\". Their declaration pledges dialogue on nuclear risks and "
        "UN reform - but says nothing about the wars in Ukraine or Iran.",
        font(SERIF, 20), W - 2 * mx, 27,
    )
    y += 12
    hrule(d, mx, W - mx, y, width=2)
    y += 14

    # ---- Middle row: two stories side by side ----
    col_w = (W - 2 * mx - 28) // 2
    left_x = mx
    right_x = mx + col_w + 28
    row_y = y

    yy = kicker(d, left_x, row_y, "The Hague - World court")
    yy = para(
        d, left_x, yy,
        "Top UN court: Myanmar committed genocide",
        font(SERIF_B, 28), col_w, 34,
    )
    yy += 4
    yy = para(
        d, left_x, yy,
        "The International Court of Justice rules that Myanmar committed "
        "genocide against the Rohingya in its 2017 military operations.",
        font(SERIF, 18), col_w, 24,
    )

    yy2 = kicker(d, right_x, row_y, "Riyadh - Saudi Arabia")
    yy2 = para(
        d, right_x, yy2,
        "Houthi strike damages Riyadh's tallest tower",
        font(SERIF_B, 28), col_w, 34,
    )
    yy2 += 4
    yy2 = para(
        d, right_x, yy2,
        "A missile strike damages the skyscraper housing Saudi Arabia's "
        "sovereign wealth fund, the latest blow in the group's campaign.",
        font(SERIF, 18), col_w, 24,
    )

    y = max(yy, yy2) + 12
    hrule(d, mx, W - mx, y, width=2)
    y += 14

    # ---- Bottom row: two stories side by side ----
    row_y = y
    yy = kicker(d, left_x, row_y, "India - Cyclone Akvan")
    yy = para(
        d, left_x, yy,
        "Cyclone Akvan makes landfall on India's east coast",
        font(SERIF_B, 28), col_w, 34,
    )
    yy += 4
    yy = para(
        d, left_x, yy,
        "More than 120,000 people are evacuated in Odisha and Andhra "
        "Pradesh as the severe storm comes ashore, with trains cancelled.",
        font(SERIF, 18), col_w, 24,
    )

    yy2 = kicker(d, right_x, row_y, "Wall Street - Markets")
    yy2 = para(
        d, right_x, yy2,
        "Anthropic debuts at a $2 trillion valuation",
        font(SERIF_B, 28), col_w, 34,
    )
    yy2 += 4
    yy2 = para(
        d, right_x, yy2,
        "The AI lab's Nasdaq debut tops SpaceX's record listing, even as "
        "its shares give back an early spike and Wall Street falls.",
        font(SERIF, 18), col_w, 24,
    )

    y = max(yy, yy2) + 12
    hrule(d, mx, W - mx, y, width=2)
    y += 14

    # ---- Also in the news strip ----
    y = kicker(d, mx, y, "Also in the news")
    also = [
        "Ukraine hits the Crimea Bridge again; Putin rules out any sea or energy truce.",
        "Israel launches a ground operation in Hamas-controlled central Gaza.",
        "Three oil tankers catch fire after hitting mines east of the Strait of Hormuz.",
        "NASA's Voyager 1 phones home from a full light-day away - the farthest ever.",
    ]
    for item in also:
        d.text((mx + 18, y), "-", font=font(SANS_B, 17), fill=RED)
        y = para(d, mx + 40, y, item, font(SERIF, 17), W - 2 * mx - 40, 22)

    # ---- Footer ----
    y = H - 34
    hrule(d, mx, W - mx, y, width=2)
    y += 8
    foot = "Drawn entirely with Python and PIL - no photographs, no network.  -  20 November 2026"
    ff = font(SANS, 15)
    fw = d.textlength(foot, font=ff)
    d.text(((W - fw) / 2, y), foot, font=ff, fill=GREY)

    img.save("entry.png", format="PNG")
    print("wrote entry.png (1024x1024)")


if __name__ == "__main__":
    main()
