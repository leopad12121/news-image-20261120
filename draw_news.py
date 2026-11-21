#!/usr/bin/env python3
"""Draw the 20 November 2026 front page for the news-image-20261120 bounty.

A 1024x1024 newspaper front page: masthead, one lead story, four more
stories in two rows of two columns, and an "also in the news" strip.
Everything is fixed text, fixed colours and fixed geometry, so running
this script twice writes a byte-identical entry.png. No network, no
clock, no randomness. Standard library plus Pillow only.
"""

from PIL import Image, ImageDraw, ImageFont

PAGE_W, PAGE_H = 1024, 1024
PAPER = (247, 243, 234)   # warm off-white newsprint
INK = (17, 17, 17)
GREY = (90, 86, 78)
RED = (160, 30, 30)
RULE = (60, 58, 52)

SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
SERIF_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
MARGIN = 48


def load(path, size):
    return ImageFont.truetype(path, size)


def wrap_lines(draw, text, fnt, max_width):
    """Greedy word wrap; returns the lines that fit max_width pixels."""
    lines = []
    current = ""
    for word in text.split(" "):
        trial = word if not current else current + " " + word
        if draw.textlength(trial, font=fnt) <= max_width:
            current = trial
        else:
            if current:
                lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines


def draw_para(draw, x, y, text, fnt, width, leading, fill=INK):
    for line in wrap_lines(draw, text, fnt, width):
        draw.text((x, y), line, font=fnt, fill=fill)
        y += leading
    return y


def draw_kicker(draw, x, y, text):
    fnt = load(SANS_BOLD, 17)
    draw.text((x, y), text.upper(), font=fnt, fill=RED)
    return y + 22


def draw_rule(draw, x0, x1, y, width=2):
    draw.line([(x0, y), (x1, y)], fill=RULE, width=width)


def draw_story(draw, x, y, width, kicker_text, headline, headline_size, body, body_size):
    """One kicker + headline + body block; returns the y below it."""
    y = draw_kicker(draw, x, y, kicker_text)
    y = draw_para(draw, x, y, headline, load(SERIF_BOLD, headline_size),
                  width, headline_size + 8)
    y += 4
    y = draw_para(draw, x, y, body, load(SERIF, body_size),
                  width, body_size + 6)
    return y


def main():
    img = Image.new("RGB", (PAGE_W, PAGE_H), PAPER)
    d = ImageDraw.Draw(img)

    # Masthead
    y = 30
    title_font = load(SERIF_BOLD, 60)
    title = "THE WORLD IN ONE DAY"
    d.text(((PAGE_W - d.textlength(title, font=title_font)) / 2, y),
           title, font=title_font, fill=INK)
    y += 72
    draw_rule(d, MARGIN, PAGE_W - MARGIN, y, width=3)
    y += 10
    date_font = load(SANS_BOLD, 18)
    dateline = "FRIDAY, 20 NOVEMBER 2026  -  THE DAY'S WORLD NEWS IN A SINGLE IMAGE"
    d.text(((PAGE_W - d.textlength(dateline, font=date_font)) / 2, y),
           dateline, font=date_font, fill=GREY)
    y += 30
    draw_rule(d, MARGIN, PAGE_W - MARGIN, y, width=3)
    y += 18

    # Lead story, full width: the overnight strike on Ukraine
    y = draw_story(
        d, MARGIN, y, PAGE_W - 2 * MARGIN,
        "Lead story - Kyiv and Poland",
        "Russia's biggest strike of the war hits Kyiv - and lands in Poland",
        44,
        "Russia fired more than 400 drones and over 110 missiles at Ukraine "
        "overnight, killing at least eight people. Three bridges across the "
        "Dnipro in Kyiv were hit, and two missiles and a drone also fell in "
        "Poland, scrambling Polish and NATO jets.",
        20,
    )
    y += 12
    draw_rule(d, MARGIN, PAGE_W - MARGIN, y)
    y += 14

    # Two-column rows
    col_w = (PAGE_W - 2 * MARGIN - 28) // 2
    left_x = MARGIN
    right_x = MARGIN + col_w + 28

    # Middle row: the cyclone, then Trump on Iran
    row_y = y
    left_end = draw_story(
        d, left_x, row_y, col_w,
        "India - Cyclone Akvan",
        "Cyclone Akvan hits India's east coast",
        28,
        "Cyclone Akvan made landfall near Gopalpur on Friday morning with "
        "winds of 70-80 km/h. About 372,000 people were evacuated to "
        "shelters, and no casualties or major damage were reported.",
        18,
    )
    right_end = draw_story(
        d, right_x, row_y, col_w,
        "Washington - Iran",
        "Trump: no rush on new Iran strikes",
        28,
        "President Trump said there is no rush to decide on new strikes on "
        "Iran, pushing any decision into 2027, after earlier suggesting "
        "Tehran would be more open to a deal after the US midterms.",
        18,
    )
    y = max(left_end, right_end) + 12
    draw_rule(d, MARGIN, PAGE_W - MARGIN, y)
    y += 14

    # Bottom row: the climate talks, then Voyager 1
    row_y = y
    left_end = draw_story(
        d, left_x, row_y, col_w,
        "Antalya, Turkiye - Climate",
        "COP31 talks run into overtime",
        28,
        "Nearly 200 nations deadlocked at the UN climate talks in Antalya "
        "over a draft deal that drops any mention of fossil fuels. "
        "Negotiators were sent into the weekend with no deal in sight.",
        18,
    )
    right_end = draw_story(
        d, right_x, row_y, col_w,
        "Space - Voyager 1",
        "Voyager 1 calls home from a light-day away",
        28,
        "NASA's Voyager 1 phoned home from about one light-day away - the "
        "farthest human-made object, still talking after nearly half a "
        "century.",
        18,
    )
    y = max(left_end, right_end) + 12
    draw_rule(d, MARGIN, PAGE_W - MARGIN, y)
    y += 14

    # Also in the news
    y = draw_kicker(d, MARGIN, y, "Also in the news")
    also = [
        "White House fires its cyber chief after tech chaos.",
        "Six killed as a gas blast collapses a housing block in Georgia.",
        "Trump bought up to $265,000 of Nvidia stock in September, a disclosure shows.",
        "US signs a new military pact with Venezuela.",
    ]
    for item in also:
        d.text((MARGIN + 18, y), "-", font=load(SANS_BOLD, 17), fill=RED)
        y = draw_para(d, MARGIN + 40, y, item, load(SERIF, 17),
                      PAGE_W - 2 * MARGIN - 40, 22)

    # Footer
    y = PAGE_H - 34
    draw_rule(d, MARGIN, PAGE_W - MARGIN, y)
    y += 8
    foot_font = load(SANS, 15)
    foot = "Drawn entirely with Python and PIL - no photographs, no network.  -  20 November 2026"
    d.text(((PAGE_W - d.textlength(foot, font=foot_font)) / 2, y),
           foot, font=foot_font, fill=GREY)

    img.save("entry.png", format="PNG")
    print("wrote entry.png (1024x1024)")


if __name__ == "__main__":
    main()
