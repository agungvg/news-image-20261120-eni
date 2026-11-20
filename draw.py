#!/usr/bin/env python3
"""THE WORLD — front page for Friday 20 November 2026.

Deterministic: fixed fonts, no randomness, no timestamps, no network.
Two runs write byte-identical PNGs. Output: 1024x1024 PNG, under 1 MiB.

Stories verified from 20 November 2026 reporting (BBC, Reuters, WSJ,
Investor's Business Daily, Kyiv Independent, India Meteorological Dept):
Kyiv bridge barrage, Cyclone Akvan landfall, Anthropic's record IPO,
the AI sell-off, COP31's final day, the Trump-Xi-Putin declaration,
the ICJ's Myanmar genocide ruling, UK-EU youth mobility, and more.
"""
import os
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
MARGIN = 26
PAPER = (250, 247, 240)
INK = (24, 24, 24)
GRAY = (96, 92, 84)
RED = (150, 28, 28)
BLUE = (28, 58, 110)
RULE = (178, 170, 156)
PANEL = (238, 232, 219)

SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SERIF_I = "/usr/share/fonts/truetype/noto/NotoSerif-Italic.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_w):
    lines, cur = [], ""
    for w in text.split():
        trial = (cur + " " + w).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def center(draw, y, text, fnt, fill=INK):
    x = (W - draw.textlength(text, font=fnt)) / 2
    draw.text((x, y), text, font=fnt, fill=fill)
    return y + fnt.size


def hline(draw, x0, x1, y, width=1, fill=RULE):
    draw.line([(x0, y), (x1, y)], fill=fill, width=width)


# ------------------------------------------------------------------ content
LEAD = {
    "kicker": "KYIV UNDER FIRE",
    "headline": "RUSSIAN MISSILES HIT THREE KYIV BRIDGES",
    "subhead": (
        "An overnight ballistic barrage splits the capital across the "
        "Dnipro — three dead, fifteen hurt — a day after Putin vowed "
        "a painful reply to the Kerch Bridge strikes."
    ),
    "body": (
        "KYIV — Russian ballistic missiles struck three bridges over "
        "the Dnipro in the early hours of Friday, Mayor Vitali "
        "Klitschko said, cutting traffic between the capital's two "
        "banks and knocking out power, heat and water in several "
        "districts. The Podilskyi and Darnytskyi crossings were hit "
        "and the Southern Bridge struck again. Three water-utility "
        "workers were killed and about fifteen people injured."
    ),
}

SECOND = [
    ("CYCLONE AKVAN LANDFALL",
     "Akvan crosses India's east coast near Gopalpur",
     "300,000+ evacuated in Odisha and Andhra Pradesh; winds of "
     "70–80 km/h, gusts to 90 — the third cyclone in a month."),
    ("ANTHROPIC'S $81BN DEBUT",
     "ANT jumps 17% as the record IPO fails to stop the rout",
     "The largest IPO ever values Anthropic at $1.3tn — yet the "
     "Nasdaq falls 2.25% and Asia's chip stocks plunge on Friday."),
]

REGIONS_LEFT = [
    ("NORTH AMERICA", [
        "Trump posthumously pardons baseball legend Pete Rose",
        "Senate rejects Iran war-powers resolution, 51–48",
        "US sanctions Comancheros and Italy's 'Ndrangheta",
        "California probes Nvidia over AI chips sold to China",
        "House panel: 880,000 AI chips approved for China",
    ]),
    ("EUROPE", [
        "UK and EU agree youth mobility scheme at summit",
        "Europe ready for talks with Russia on ending the war",
        "Poland prepares $50bn nuclear deal with US firms",
        "Czech leaders visit Israel to inspect missile systems",
        "Genoa airport halts flights after mystery drones",
    ]),
    ("MIDDLE EAST", [
        "Houthi strike damages Riyadh's 80-storey PIF tower",
        "Israel runs one-day Gaza operation past ceasefire line",
        "Saudi air defences destroy two Houthi drones",
        "Tanker catches fire after mine strike near Hormuz",
        "Israeli strike hits Hezbollah site in east Lebanon",
    ]),
    ("DIPLOMACY & LAW", [
        "Trump, Xi and Putin release 'peace declaration'",
        "UN court: Myanmar committed genocide on Rohingya",
        "COP31 final day deadlocked as draft drops fossil cuts",
        "UK pledges 1,000+ drones for Ukraine in £260m package",
        "European allies meet in Berlin over Ukraine peace role",
    ]),
]

REGIONS_RIGHT = [
    ("ASIA-PACIFIC", [
        "Taiwan stocks plunge 2,200 points in a day",
        "Nikkei slides 4.7% as SoftBank falls 15.6%",
        "Japan core inflation hits 2.2%, a 2026 high",
        "Samsung names Won-Joon Choi to head mobile unit",
        "China issues Mount Fuji warning to its climbers",
    ]),
    ("MARKETS & TECH", [
        "Dow falls below 50,000 as sell-off deepens",
        "S&P 500 drops 2.02%; Nasdaq down 2.25%",
        "AMD sinks 8% after short-seller export report",
        "GTA 6 sales top $2.3bn, industry estimate says",
        "Google adds Mac control to its Gemini assistant",
    ]),
    ("SPORT & CULTURE", [
        "Chelsea edge PSG 1–0 on Buurman's 87th-minute goal",
        "Wattimena beats Littler 10–8 at Grand Slam of Darts",
        "Unseeded Sykes stuns Humphries 10–9 in thriller",
        "Russell fastest in wet Las Vegas GP practice",
        "Texans trample Colts to keep playoff hopes alive",
    ]),
]

NUMBERS = [
    ("3", "bridges over the Dnipro hit in Kyiv"),
    ("300,000+", "people evacuated ahead of Cyclone Akvan"),
    ("$81.3bn", "raised in Anthropic's record IPO"),
    ("+17%", "ANT's first-day gain; Nasdaq −2.25%"),
    ("−4.7%", "Nikkei and Kospi fall on Friday"),
]


def draw_kyiv(draw, x0, y0, x1, y1):
    """Night over the Dnipro: dark sky, river, three bridges, smoke."""
    draw.rectangle([x0, y0, x1, y1], fill=(30, 38, 58))
    draw.rectangle([x0, y0, x1, y1], outline=RULE, width=1)
    # pale moon
    draw.ellipse([x1 - 52, y0 + 12, x1 - 22, y0 + 42], fill=(232, 226, 210))
    # far bank skyline
    base = y0 + int((y1 - y0) * 0.52)
    for fx, fw, fh in [(0.04, 0.07, 0.30), (0.16, 0.06, 0.42),
                       (0.30, 0.08, 0.26), (0.46, 0.06, 0.36),
                       (0.62, 0.07, 0.30), (0.78, 0.06, 0.40)]:
        span = x1 - x0
        tx0 = x0 + int(fx * span)
        tx1 = tx0 + int(fw * span)
        ty0 = base - int(fh * (base - y0))
        draw.rectangle([tx0, ty0, tx1, base], fill=(18, 24, 40))
        for wy in range(ty0 + 6, base - 4, 12):
            for wx in range(tx0 + 4, tx1 - 4, 11):
                if (wx * 3 + wy * 5) % 17 < 5:
                    draw.rectangle([wx, wy, wx + 2, wy + 3],
                                   fill=(240, 200, 110))
    # river
    draw.rectangle([x0, base, x1, y1], fill=(52, 78, 118))
    for ry in range(base + 6, y1 - 4, 10):
        draw.line([(x0 + 8, ry), (x1 - 8, ry)], fill=(84, 112, 150), width=1)
    # three bridges across the river
    for fx in (0.18, 0.48, 0.76):
        bx = x0 + int(fx * (x1 - x0))
        draw.line([(bx - 34, base + 8), (bx + 34, base + 8)],
                  fill=(220, 220, 220), width=3)
        draw.line([(bx, base - 26), (bx, base + 8)], fill=(220, 220, 220),
                  width=2)
        draw.line([(bx - 34, base + 8), (bx, base - 26)],
                  fill=(220, 220, 220), width=1)
        draw.line([(bx + 34, base + 8), (bx, base - 26)],
                  fill=(220, 220, 220), width=1)
    # smoke columns and fire glow over two bridges
    for fx, fy in [(0.18, base - 30), (0.76, base - 34)]:
        sx = x0 + int(fx * (x1 - x0))
        draw.ellipse([sx - 8, fy - 8, sx + 8, fy + 8], fill=(120, 120, 118))
        draw.ellipse([sx - 5, fy - 16, sx + 5, fy - 6], fill=(150, 150, 146))
        draw.ellipse([sx - 6, base + 2, sx + 6, base + 12],
                     fill=(226, 120, 40))
    cap = font(SANS, 10)
    draw.text((x0 + 6, y1 + 5),
              "Kyiv, Friday — three Dnipro crossings hit overnight.",
              font=cap, fill=GRAY)


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # ---- masthead
    y = 22
    y = center(d, y, "THE WORLD", font(SERIF_B, 62))
    y += 6
    hline(d, MARGIN, W - MARGIN, y, width=2, fill=INK)
    y += 5
    hline(d, MARGIN, W - MARGIN, y, width=1, fill=INK)
    y += 9
    y = center(d, y, "FRIDAY, 20 NOVEMBER 2026  •  33 STORIES  •  6 REGIONS",
               font(SANS_B, 14))
    y += 8
    hline(d, MARGIN, W - MARGIN, y, width=1, fill=RULE)

    # ---- lead story
    y += 11
    d.text((MARGIN, y), LEAD["kicker"], font=font(SANS_B, 15), fill=RED)
    y += 23
    head = font(SERIF_B, 33)
    for line in wrap(d, LEAD["headline"], head, W - 2 * MARGIN):
        d.text((MARGIN, y), line, font=head, fill=INK)
        y += 40
    y += 1
    sub = font(SERIF_I, 16)
    for line in wrap(d, LEAD["subhead"], sub, W - 2 * MARGIN):
        d.text((MARGIN, y), line, font=sub, fill=(60, 58, 52))
        y += 21
    y += 4
    body_top = y
    body_w = 540
    body = font(SERIF, 13)
    for line in wrap(d, LEAD["body"], body, body_w):
        d.text((MARGIN, y), line, font=body, fill=INK)
        y += 18
    ill_x = MARGIN + body_w + 22
    ill_w = W - MARGIN - ill_x
    draw_kyiv(d, ill_x, body_top, ill_x + ill_w, body_top + 116)
    y = max(y, body_top + 116 + 16)
    hline(d, MARGIN, W - MARGIN, y, width=1, fill=RULE)

    # ---- secondary strip: two boxes
    y += 10
    box_w = (W - 2 * MARGIN - 20) // 2
    box_h = 84
    for i, (kick, head_t, deck) in enumerate(SECOND):
        bx = MARGIN + i * (box_w + 20)
        d.rectangle([bx, y, bx + box_w, y + box_h], fill=PANEL, outline=RULE)
        d.text((bx + 12, y + 8), kick, font=font(SANS_B, 12), fill=BLUE)
        yy = y + 27
        hf = font(SANS_B, 14)
        for line in wrap(d, head_t, hf, box_w - 24):
            d.text((bx + 12, yy), line, font=hf, fill=INK)
            yy += 18
        df = font(SANS, 11)
        for line in wrap(d, deck, df, box_w - 24):
            d.text((bx + 12, yy), line, font=df, fill=(60, 58, 52))
            yy += 15
    y += box_h + 12
    hline(d, MARGIN, W - MARGIN, y, width=1, fill=RULE)

    # ---- region grid
    y += 11
    col_w = (W - 2 * MARGIN - 24) // 2
    left_x = MARGIN
    right_x = MARGIN + col_w + 24

    def region_block(x, top, name, stories):
        yy = top
        d.text((x, yy), name, font=font(SANS_B, 13), fill=RED)
        yy += 19
        hline(d, x, x + col_w, yy, width=1, fill=INK)
        yy += 7
        tf = font(SANS_B, 12)
        for title in stories:
            for line in wrap(d, title, tf, col_w):
                d.text((x, yy), line, font=tf, fill=INK)
                yy += 14
            yy += 2
        return yy

    ly = y
    for name, stories in REGIONS_LEFT:
        ly = region_block(left_x, ly, name, stories)
        ly += 7
    ry = y
    for name, stories in REGIONS_RIGHT:
        ry = region_block(right_x, ry, name, stories)
        ry += 7

    # day-in-numbers box under the right column
    by = ry + 2
    box_h = 104
    d.rectangle([right_x, by, right_x + col_w, by + box_h],
                fill=PANEL, outline=RULE)
    d.text((right_x + 12, by + 9), "THE DAY IN NUMBERS",
           font=font(SANS_B, 13), fill=RED)
    ny = by + 31
    nf = font(SANS_B, 12)
    vf = font(SANS, 12)
    for num, label in NUMBERS:
        d.text((right_x + 12, ny), num, font=nf, fill=INK)
        nw = d.textlength(num, font=nf)
        d.text((right_x + 12 + nw + 8, ny), label, font=vf, fill=INK)
        ny += 14

    # ---- footer
    fy = H - 30
    hline(d, MARGIN, W - MARGIN, fy, width=1, fill=RULE)
    center(d, fy + 8,
           "THE WORLD  •  Friday 20 November 2026  •  theworld.news",
           font(SANS, 12), fill=GRAY)

    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")
    img.save(out, "PNG", optimize=True)
    print("wrote", out, os.path.getsize(out), "bytes")


if __name__ == "__main__":
    main()
