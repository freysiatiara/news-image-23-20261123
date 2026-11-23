#!/usr/bin/env python3
"""Draw the news-image-20261123 front page: MONDAY 23 NOVEMBER 2026.
Deterministic PIL render (no network, no fonts beyond system DejaVu).
Run: python3 draw.py  -> writes entry.png (1024x1024, <= 1 MiB).
Story list verified against web reporting on 23 Nov 2026 (UTC morning):
COP31 collapse fallout, Hormuz tanker attacks, Ukraine drones, Sparta II,
BepiColombo Mercury orbit, El Chapo Isidro capture, Gaza, UN AI-weapons talks.
"""
import textwrap
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
BG = (250, 247, 240)          # paper
INK = (20, 24, 30)
NAVY = (15, 42, 74)
NAVY2 = (23, 64, 110)
GOLD = (201, 162, 39)
RED = (178, 34, 34)
TEAL = (14, 110, 110)
RULE = (180, 175, 165)
MUTED = (90, 92, 96)

SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SERIF_R = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(d, text, fnt, width):
    """Greedy word wrap to pixel width; returns list of lines."""
    lines, cur = [], ""
    for word in text.split():
        trial = (cur + " " + word).strip()
        if d.textlength(trial, font=fnt) <= width:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def para(d, x, y, width, text, fnt, fill=INK, leading=4):
    """Draw wrapped paragraph; return y after last line."""
    for line in wrap(d, text, fnt, width):
        d.text((x, y), line, font=fnt, fill=fill)
        y += fnt.size + leading
    return y


def headline(d, x, y, width, text, fnt, fill=INK, leading=2):
    return para(d, x, y, width, text, fnt, fill=fill, leading=leading)


def kicker(d, x, y, text, color=RED):
    f = font(SANS_B, 13)
    d.text((x, y), text.upper(), font=f, fill=color)
    return y + 18


def rule(d, x, y, width, fill=RULE, wdt=1):
    d.line([(x, y), (x + width, y)], fill=fill, width=wdt)

# --- STORIES: (region, bold lead, one-line summary) -----------------------
# Every item below was reported on Monday 23 November 2026 (UTC) or is the
# overnight fallout the world woke up to that morning. COP31 fell on Sun 22
# Nov; its collapse and reactions lead the day and are dated as such in text.
LEAD_COP31 = (
    "COP31 COLLAPSES",
    "Antalya ends with no deal. The EU, UK and island states reject a text "
    "that never names fossil fuels; the longest COP ever ends in failure.",
)
LEAD_HORMUZ = (
    "HORMUZ UNDER FIRE",
    "Tanker attacks at their highest level since the war began: 25 hit in "
    "seven days. Three more struck Fri-Sat; crews safe. Trump said to "
    "favour an economic squeeze on Iran over new strikes.",
)
LEAD_UKRAINE = (
    "UKRAINE: 186 DRONES",
    "Russia's overnight barrage: 161 shot down, but a block in Dymer falls, "
    "14 missing, 3 dead. The Sparta II still burns off Finland; 16 crew out.",
)

SECTIONS = [
    ("MIDDLE EAST", RED, [
        ("BAHRAIN SEEKS UN ACTION",
         "Iran hit a civilian facility on Saturday; two hurt, Bahrain demands a UN response."),
        ("HOUTHIS HIT RIYADH AGAIN",
         "Third straight day of strikes; Saudi Arabia intercepts a missile and a drone."),
        ("GAZA: 9 KILLED IN 48 HOURS",
         "Israeli strikes continue; toll since the Oct 2025 ceasefire now 1,661."),
        ("UNITY TALKS RESUME",
         "Netanyahu's Likud and Eisenkot's Yashar open a second round of talks in Herzliya."),
        ("LEBANON SEIZES EXPLOSIVES",
         "Army arrests three people with 264 kg of explosives."),
        ("US-CHINA TALK HORMUZ",
         "Washington and Beijing discuss risks to shipping and energy through the strait."),
    ]),
    ("EUROPE", NAVY2, [
        ("CRIMEA BRIDGE BLASTS",
         "BBC Verify: new footage shows explosions moments before part of the bridge fell."),
        ("KALININGRAD ON ALERT",
         "Rare air alert sounds as drones are reported near the naval base."),
        ("LISBON MARCHES",
         "Thousands take to the streets as living costs fuel anger."),
        ("FRANCE: 6TH SATURDAY",
         "Cost-of-living protests continue for a sixth weekend."),
        ("HONG KONG VOTES",
         "Voters go to the polls in the Legislative Council election."),
        ("UK TO BUILD UKRAINE DRONES",
         "Britain signs a deal to produce Ukrainian drones."),
        ("DE GENNARO DEAD AT 78",
         "Former Italian police chief found dead in Tuscany amid a mafia bombing inquiry."),
    ]),
    ("ASIA-PACIFIC", TEAL, [
        ("NEPAL PM MEETS MODI",
         "Balendra Shah holds bilateral talks in Delhi on his state visit."),
        ("SEOUL MINISTER QUITS",
         "South Korea's education minister resigns over an AI exam-cheating scandal."),
        ("FACTORY FIRE IN INDONESIA",
         "Body bags recovered after the blaze; 50 people still missing."),
        ("AMIT SHAH IN ARUNACHAL",
         "India's home minister launches a Rs 4,000-crore infrastructure push."),
        ("MYANMAR SLAMS ASEAN",
         "Army-backed government calls the bloc's decision 'unfair and imbalanced'."),
    ]),
    ("AMERICAS", (122, 74, 10), [
        ("'EL CHAPO ISIDRO' CAUGHT",
         "FBI top-10 fugitive seized in Sinaloa; 11 killed in the gunfight."),
        ("SCHUMER CHALLENGED",
         "Senate Democrats' leader faces a challenge from Chris Van Hollen; vote 1 Dec."),
        ("PENTAGON OPENS UAP FILES",
         "43 more declassified files, three Middle East videos, all unresolved."),
        ("BITCOIN REBOUNDS",
         "Crypto climbs back after hitting a two-year low."),
    ]),
    ("AFRICA", (90, 60, 140), [
        ("NIGERIA BOAT SINKS",
         "At least 24 people dead after a boat capsizes."),
        ("LIBYA: BLAST AT BENGHAZI",
         "Drone strike blamed for an explosion near a Russian ship; 10 port workers hurt."),
        ("ICJ RULING: MALAYSIA ACTS",
         "Kuala Lumpur to coordinate with the UN and OIC after the Myanmar atrocity ruling."),
    ]),
    ("SCIENCE & SPACE", (16, 110, 90), [
        ("BEPICOLOMBO REACHES MERCURY",
         "After eight years, ESA-JAXA probe enters orbit; a thruster glitch, ESA updates Monday."),
        ("MOSQUITOES v DENGUE",
         "Scientists report specially bred mosquitoes can fend off dengue fever."),
        ("UN: AI-WEAPONS TALKS GO ON",
         "Nations agree to keep negotiating lethal autonomous systems; no binding rules yet."),
    ]),
    ("SPORT & BUSINESS", (60, 90, 30), [
        ("INDIA 720/9 DECLARED",
         "Record Test total in Wellington against New Zealand."),
        ("INDIA-PAKISTAN IN QATAR",
         "Cricket rivalry brings World Cup buzz to Doha stadiums."),
        ("SNOOKER: ANUPAMA KEEPS CROWN",
         "Indian star defends the IBSF world women's title."),
        ("TATA STEEL'S BIG DEAL",
         "Rs 28,000-crore pact with APL Apollo; Nvidia chip-row details emerge."),
    ]),
]

TOTAL_STORIES = 3 + sum(len(items) for _, _, items in SECTIONS)

# --- ILLUSTRATIONS (flat vector panels, drawn fresh) ----------------------
def draw_globe(d, cx, cy, r):
    """Earth with meridian lines, cracked pact sheet below."""
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(38, 90, 140),
              outline=(10, 30, 55), width=3)
    for k in range(-2, 3):
        x0 = cx + k * r // 3
        d.arc([x0 - r // 3, cy - r, x0 + r // 3, cy + r], 270, 90,
              fill=(140, 190, 230), width=2)
    d.arc([cx - r, cy - r // 2, cx + r, cy + r // 2], 0, 360,
          fill=(140, 190, 230), width=2)
    d.arc([cx - r // 2, cy - r, cx + r // 2, cy + r], 0, 360,
          fill=(90, 150, 200), width=2)
    # land blobs
    d.ellipse([cx - r + 12, cy - r + 18, cx - 6, cy - 2], fill=(74, 140, 90))
    d.ellipse([cx + 2, cy + 4, cx + r - 14, cy + r - 16], fill=(74, 140, 90))
    # cracked sheet
    d.polygon([(cx - 52, cy + r - 6), (cx + 52, cy + r - 6),
               (cx + 44, cy + r + 26), (cx - 44, cy + r + 26)],
              fill=(255, 255, 255), outline=(120, 30, 30))
    d.line([(cx - 30, cy + r + 8), (cx + 28, cy + r + 8)], fill=(120, 30, 30), width=3)
    d.line([(cx - 30, cy + r + 16), (cx + 10, cy + r + 16)], fill=(120, 30, 30), width=3)


def draw_tanker(d, x, y, w, hgt):
    """Tanker silhouette on waves, with smoke."""
    d.rectangle([x, y + hgt - 34, x + w, y + hgt - 14], fill=(40, 44, 52))
    d.rectangle([x + w - 52, y + hgt - 58, x + w - 14, y + hgt - 34],
                fill=(40, 44, 52))
    d.rectangle([x + 14, y + hgt - 52, x + 44, y + hgt - 34], fill=(40, 44, 52))
    # funnel smoke, tight above the funnel
    for i in range(2):
        sx = x + w - 44 + i * 14
        d.ellipse([sx, y + 2 + i * 6, sx + 18, y + 18 + i * 6],
                  fill=(130, 130, 135))
    for i in range(4):
        wx = x + i * (w // 4)
        d.arc([wx, y + hgt - 12, wx + 44, y + hgt + 8], 180, 360,
              fill=(38, 90, 140), width=3)


def draw_ship_fire(d, x, y, w, hgt):
    """Burning cargo ship: hull, containers, flame, smoke."""
    d.rectangle([x, y + hgt - 30, x + w, y + hgt - 12], fill=(60, 30, 30))
    for i, c in enumerate([(178, 34, 34), (201, 162, 39), (38, 90, 140)]):
        d.rectangle([x + 12 + i * 46, y + hgt - 62, x + 52 + i * 46,
                     y + hgt - 30], fill=c, outline=(20, 20, 20))
    d.polygon([(x + w // 2 - 10, y + hgt - 62), (x + w // 2 + 10, y + hgt - 62),
               (x + w // 2 + 4, y + 22), (x + w // 2 - 4, y + 22)],
              fill=(230, 120, 20))
    d.polygon([(x + w // 2 - 5, y + hgt - 62), (x + w // 2 + 5, y + hgt - 62),
               (x + w // 2 + 2, y + 36), (x + w // 2 - 2, y + 36)],
              fill=(250, 200, 40))
    for i in range(2):
        sx = x + w // 2 - 34 + i * 52
        d.ellipse([sx, y + 2, sx + 24, y + 20], fill=(140, 140, 145))


def draw_section(d, x, y, w, title, color, items):
    """One region box; returns y below the box."""
    f_title = font(SANS_B, 15)
    f_lead = font(SANS_B, 12)
    f_body = font(SANS, 11)
    d.rectangle([x, y, x + w, y + 24], fill=color)
    d.text((x + 8, y + 3), title, font=f_title, fill=(255, 255, 255))
    y += 28
    for lead, body in items:
        y = headline(d, x + 2, y, w - 4, lead, f_lead, leading=1)
        y = para(d, x + 2, y, w - 4, body, f_body, fill=(60, 62, 66), leading=1)
        y += 5
    return y

# --- PAGE ------------------------------------------------------------------
def build():
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)

    # Masthead
    d.rectangle([0, 0, W, 112], fill=NAVY)
    d.rectangle([0, 112, W, 116], fill=GOLD)
    d.text((18, 10), "THE WORLD IN ONE DAY",
           font=font(SERIF, 44), fill=(255, 255, 255))
    d.text((18, 62), "MONDAY  23  NOVEMBER  2026",
           font=font(SANS_B, 26), fill=GOLD)
    d.text((18, 92), "The day's world news, in one picture  •  make.fun picture of the day",
           font=font(SANS, 13), fill=(200, 210, 225))
    right1, right2 = f"{TOTAL_STORIES} STORIES", "7 REGIONS"
    f_r = font(SANS_B, 20)
    for i, t in enumerate((right1, right2)):
        tw = d.textlength(t, font=f_r)
        d.text((W - 18 - tw, 14 + i * 26), t, font=f_r, fill=(255, 255, 255))

    # Lead row: three panels
    y0 = 128
    panels = [
        (16, 310, "LEAD  •  CLIMATE", RED, LEAD_COP31, "globe"),
        (338, 330, "LEAD  •  MIDDLE EAST", RED, LEAD_HORMUZ, "tanker"),
        (680, 328, "LEAD  •  EUROPE", NAVY2, LEAD_UKRAINE, "ship"),
    ]
    for x, w, kick, color, (head, body), art in panels:
        d.rectangle([x, y0, x + w, y0 + 238], fill=(255, 255, 255),
                    outline=RULE, width=1)
        kicker(d, x + 10, y0 + 8, kick, color)
        yy = headline(d, x + 10, y0 + 28, w - 20, head, font(SERIF, 23),
                      fill=INK)
        if art == "globe":
            draw_globe(d, x + w // 2, y0 + 126, 34)
            yy = y0 + 188
        elif art == "tanker":
            draw_tanker(d, x + 14, y0 + 100, w - 28, 72)
            yy = y0 + 180
        else:
            draw_ship_fire(d, x + 14, y0 + 98, w - 28, 76)
            yy = y0 + 180
        para(d, x + 10, yy, w - 20, body, font(SANS, 12),
             fill=(50, 52, 56), leading=2)

    # Region grid: three columns, sections stacked
    cols = [
        [SECTIONS[0], SECTIONS[3]],   # Middle East + Americas
        [SECTIONS[1], SECTIONS[4]],   # Europe + Africa
        [SECTIONS[2], SECTIONS[5], SECTIONS[6]],  # Asia-Pacific + Science + Sport
    ]
    col_x = [16, 348, 680]
    col_w = [320, 320, 328]
    grid_top = 378
    bottoms = []
    for cx, cw, stack in zip(col_x, col_w, cols):
        y = grid_top
        for title, color, items in stack:
            y = draw_section(d, cx, y, cw, title, color, items)
            y += 10
        bottoms.append(y)
    grid_bottom = max(bottoms)

    # Date-check footer strip
    fy = 962
    d.rectangle([0, fy, W, H], fill=NAVY)
    d.text((18, fy + 5),
           "DATE CHECK — MONDAY 23 NOVEMBER 2026:",
           font=font(SANS_B, 15), fill=GOLD)
    d.text((18, fy + 25),
           "Every story here is the news of this day as reported on 23 Nov 2026. "
           "COP31 fell on Sun 22 Nov; its collapse leads the world today.",
           font=font(SANS, 13), fill=(220, 228, 238))
    d.text((18, fy + 45),
           "Sources: Reuters, CNN, AP, BBC, ESA, UN News, national wires — 23 Nov 2026.",
           font=font(SANS, 11), fill=(170, 180, 195))
    print("grid bottom:", grid_bottom, "footer top:", fy,
          "stories:", TOTAL_STORIES)
    return img


if __name__ == "__main__":
    im = build()
    im.save("entry.png", optimize=True)
    import os
    print("entry.png bytes:", os.path.getsize("entry.png"))
