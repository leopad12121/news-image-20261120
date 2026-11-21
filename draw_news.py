#!/usr/bin/env python3
"""Draw the front page for 20 November 2026 (news-image-20261120, round 2).

A 1024x1024 newspaper front page rendered entirely with Python + PIL.
Deterministic: fixed text, fixed colours, fixed geometry. No network,
no timestamps, no randomness -- running it twice yields a byte-identical
entry.png.
"""

from PIL import Image, ImageDraw, ImageFont

# ---------------------------------------------------------------- canvas
PAGE = 1024
MARGIN = 48
CONTENT = PAGE - 2 * MARGIN          # 928
GUTTER = 28
COLUMN = (CONTENT - GUTTER) // 2     # 450

PAPER = (247, 243, 234)
INK = (17, 17, 17)
GREY = (90, 86, 78)
RED = (160, 30, 30)
RULE = (60, 58, 52)

FONTS = "/usr/share/fonts/truetype/dejavu/"


def load(name, size):
    return ImageFont.truetype(FONTS + name, size)


SERIF = "DejaVuSerif.ttf"
SERIF_BOLD = "DejaVuSerif-Bold.ttf"
SANS = "DejaVuSans.ttf"
SANS_BOLD = "DejaVuSans-Bold.ttf"

# ---------------------------------------------------------------- content
MASTHEAD = "THE WORLD IN ONE DAY"
DATELINE = "FRIDAY, 20 NOVEMBER 2026  -  THE DAY'S WORLD NEWS IN A SINGLE IMAGE"

LEAD = {
    "kicker": "LEAD STORY - KYIV AND POLAND",
    "headline": "Russia's biggest strike of the war hits Kyiv - and lands in Poland",
    "body": (
        "Russia fired more than 400 drones and over 110 missiles at Ukraine "
        "overnight, killing at least eight people. Three bridges across the "
        "Dnipro in Kyiv were hit, and two missiles and a drone also fell in "
        "Poland, scrambling Polish and NATO jets."
    ),
}

MIDDLE_LEFT = {
    "kicker": "INDIA - CYCLONE AKVAN",
    "headline": "Cyclone Akvan hits India's east coast",
    "body": (
        "Cyclone Akvan made landfall near Gopalpur on Friday morning with "
        "winds of 70-80 km/h. About 372,000 people were evacuated to "
        "shelters, and no casualties or major damage were reported."
    ),
}

MIDDLE_RIGHT = {
    "kicker": "WASHINGTON - IRAN",
    "headline": "Trump: no rush on new Iran strikes",
    "body": (
        "President Trump said there is no rush to decide on new strikes on "
        "Iran, pushing any decision into 2027, after earlier suggesting "
        "Tehran would be more open to a deal after the US midterms."
    ),
}

BOTTOM_LEFT = {
    "kicker": "ANTALYA, TURKIYE - CLIMATE",
    "headline": "COP31 talks run into overtime",
    "body": (
        "Nearly 200 nations deadlocked at the UN climate talks in Antalya "
        "over a draft deal that drops any mention of fossil fuels. "
        "Negotiators were sent into the weekend with no deal in sight."
    ),
}

BOTTOM_RIGHT = {
    "kicker": "SPACE - VOYAGER 1",
    "headline": "Voyager 1 calls home from a light-day away",
    "body": (
        "NASA's Voyager 1 phoned home from about one light-day away - the "
        "farthest human-made object, still talking after nearly half a "
        "century."
    ),
}

ALSO_ITEMS = [
    "White House fires its cyber chief after tech chaos.",
    "Six killed as a gas blast collapses a housing block in Georgia.",
    "Trump bought up to $265,000 of Nvidia stock in September, a disclosure shows.",
    "US signs a new military pact with Venezuela.",
]

FOOTER = "Drawn entirely with Python and PIL - no photographs, no network.  -  20 November 2026"


# ---------------------------------------------------------------- helpers
def wrap_text(draw, text, font, max_width):
    """Greedy word wrap; returns a list of lines that fit max_width."""
    lines = []
    current = ""
    for word in text.split():
        trial = word if not current else current + " " + word
        if draw.textlength(trial, font=font) <= max_width:
            current = trial
        else:
            if current:
                lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines


def draw_lines(draw, x, y, lines, font, fill, leading):
    """Draw lines top-down; returns the y just below the last line."""
    for line in lines:
        draw.text((x, y), line, font=font, fill=fill)
        y += leading
    return y


def draw_rule(draw, y, x0=MARGIN, x1=PAGE - MARGIN, thickness=2):
    draw.rectangle([x0, y, x1, y + thickness - 1], fill=RULE)
    return y + thickness


def centred_x(draw, text, font):
    return (PAGE - draw.textlength(text, font=font)) / 2


def draw_story(draw, x, y, story, width):
    """One column story: red kicker, bold headline, serif body.

    Returns the y just below the body text.
    """
    kicker_font = load(SANS_BOLD, 17)
    head_font = load(SERIF_BOLD, 28)
    body_font = load(SERIF, 18)

    draw.text((x, y), story["kicker"], font=kicker_font, fill=RED)
    y += 26

    head_lines = wrap_text(draw, story["headline"], head_font, width)
    y = draw_lines(draw, x, y, head_lines, head_font, INK, 35)
    y += 6

    body_lines = wrap_text(draw, story["body"], body_font, width)
    y = draw_lines(draw, x, y, body_lines, body_font, INK, 24)
    return y


# ---------------------------------------------------------------- page
def build():
    image = Image.new("RGB", (PAGE, PAGE), PAPER)
    draw = ImageDraw.Draw(image)

    y = 26

    # Masthead
    mast_font = load(SERIF_BOLD, 60)
    draw.text((centred_x(draw, MASTHEAD, mast_font), y), MASTHEAD,
              font=mast_font, fill=INK)
    y += 70
    y = draw_rule(draw, y)
    y += 8

    # Dateline
    date_font = load(SANS_BOLD, 18)
    draw.text((centred_x(draw, DATELINE, date_font), y), DATELINE,
              font=date_font, fill=GREY)
    y += 26
    y = draw_rule(draw, y)
    y += 12

    # Lead story, full width
    lead_kicker = load(SANS_BOLD, 17)
    draw.text((MARGIN, y), LEAD["kicker"], font=lead_kicker, fill=RED)
    y += 24

    lead_head = load(SERIF_BOLD, 44)
    head_lines = wrap_text(draw, LEAD["headline"], lead_head, CONTENT)
    y = draw_lines(draw, MARGIN, y, head_lines, lead_head, INK, 52)
    y += 6

    lead_body = load(SERIF, 20)
    body_lines = wrap_text(draw, LEAD["body"], lead_body, CONTENT)
    y = draw_lines(draw, MARGIN, y, body_lines, lead_body, INK, 27)
    y += 10
    y = draw_rule(draw, y)
    y += 12

    # Middle row: two columns
    left_end = draw_story(draw, MARGIN, y, MIDDLE_LEFT, COLUMN)
    right_end = draw_story(draw, MARGIN + COLUMN + GUTTER, y,
                           MIDDLE_RIGHT, COLUMN)
    y = max(left_end, right_end) + 10
    y = draw_rule(draw, y)
    y += 12

    # Bottom row: two columns
    left_end = draw_story(draw, MARGIN, y, BOTTOM_LEFT, COLUMN)
    right_end = draw_story(draw, MARGIN + COLUMN + GUTTER, y,
                           BOTTOM_RIGHT, COLUMN)
    y = max(left_end, right_end) + 10
    y = draw_rule(draw, y)
    y += 12

    # "Also in the news" strip
    strip_kicker = load(SANS_BOLD, 17)
    draw.text((MARGIN, y), "ALSO IN THE NEWS", font=strip_kicker, fill=RED)
    y += 24

    item_font = load(SERIF, 17)
    for item in ALSO_ITEMS:
        draw.text((MARGIN, y), "- " + item, font=item_font, fill=INK)
        y += 21

    # Footer
    draw_rule(draw, PAGE - 34)
    foot_font = load(SANS, 15)
    draw.text((centred_x(draw, FOOTER, foot_font), PAGE - 26), FOOTER,
              font=foot_font, fill=GREY)

    image.save("entry.png", format="PNG")
    print("wrote entry.png (1024x1024)")


if __name__ == "__main__":
    build()
