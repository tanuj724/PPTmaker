"""
PPTmaker - Builder Agent
Topic: World War II — The Last World War
Theme: Sovereign Archive (Olive / Antique Gold / Allied Blue / Axis Crimson / Cream)
Slide Budget: 11 slides
Design: 11 distinct layout archetypes, zero consecutive duplicates, full speaker notes.
"""

import os
import sys

from pptx import Presentation
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import MSO_ANCHOR, MSO_AUTO_SIZE, PP_ALIGN
from pptx.util import Inches, Pt

# ==============================================================================
# THEME CONSTANTS — SOVEREIGN ARCHIVE
# ==============================================================================
PRIMARY_DARK = RGBColor(0x1F, 0x3D, 0x2B)       # #1F3D2B Deep field olive
SECONDARY_DARK = RGBColor(0x2C, 0x44, 0x36)     # #2C4436 Slate olive (image backing)
ALLIES_BLUE = RGBColor(0x3E, 0x6B, 0x8C)        # #3E6B8C Battle map blue (Allies)
AXIS_CRIMSON = RGBColor(0x9A, 0x33, 0x24)       # #9A3324 Deep iron crimson (Axis)
ACCENT_METAL = RGBColor(0xC9, 0xA2, 0x27)       # #C9A227 Antique medal gold
ACCENT_LIGHT = RGBColor(0xE9, 0xD0, 0x84)       # #E9D084 Pale medal gold
CANVAS = RGBColor(0xF9, 0xF4, 0xEB)             # #F9F4EB Archival cream
SURFACE_ALT = RGBColor(0xF0, 0xE9, 0xD8)        # #F0E9D8 Tinted surface
TEXT_INK = RGBColor(0x21, 0x26, 0x28)           # #212628 Charcoal ink
TEXT_MUTED = RGBColor(0x6F, 0x77, 0x75)         # #6F7775 Slate muted
RULE_COLOR = RGBColor(0xE0, 0xD8, 0xC4)         # #E0D8C4 Cream-grey hairline
ON_DARK_TEXT = RGBColor(0xD6, 0xDC, 0xBF)       # #D6DCBF Soft lichen on olive
WHITE_RGB = RGBColor(0xFF, 0xFF, 0xFF)

TITLE_FONT = "Georgia"
BODY_FONT = "Arial"

SLIDE_W = 13.333
SLIDE_H = 7.500
TOTAL = 11

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ASSETS_DIR = os.path.join(BASE_DIR, "assets_ww2")
OUTPUT_PPTX = os.path.join(BASE_DIR, "World_War_2_Presentation.pptx")


def asset(name):
    return os.path.join(ASSETS_DIR, name + ".jpg")


# ==============================================================================
# DEFENSIVE GEOMETRY & PRIMITIVES
# ==============================================================================
SAFE_W = 13.333
SAFE_H = 7.500


def clamp_box(l, t, w, h):
    l = max(0.0, min(l, SAFE_W - 0.01))
    t = max(0.0, min(t, SAFE_H - 0.01))
    w = max(0.05, min(w, SAFE_W - l))
    h = max(0.05, min(h, SAFE_H - t))
    return l, t, w, h


def _prep_tf(tb, anchor=MSO_ANCHOR.TOP, wrap=True):
    tf = tb.text_frame
    tf.word_wrap = wrap
    tf.vertical_anchor = anchor
    tf.margin_left = 0
    tf.margin_right = 0
    tf.margin_top = 0
    tf.margin_bottom = 0
    try:
        tf.auto_size = MSO_AUTO_SIZE.NONE
    except Exception:
        pass
    return tf


def set_bg(slide, color):
    slide.background.fill.solid()
    slide.background.fill.fore_color.rgb = color


def add_rect(slide, l, t, w, h, fill=None, line_color=None, line_w=0.75,
             shape_type=MSO_SHAPE.RECTANGLE, adj=None, no_fill=False):
    l, t, w, h = clamp_box(l, t, w, h)
    sp = slide.shapes.add_shape(shape_type, Inches(l), Inches(t), Inches(w), Inches(h))
    if no_fill or fill is None:
        sp.fill.background()
    else:
        sp.fill.solid()
        sp.fill.fore_color.rgb = fill
    if line_color is None:
        sp.line.fill.background()
    else:
        sp.line.color.rgb = line_color
        sp.line.width = Pt(line_w)
    if adj is not None:
        try:
            sp.adjustments[0] = adj
        except Exception:
            pass
    sp.shadow.inherit = False
    try:
        sp.text_frame.text = ""
        sp.text_frame.margin_left = sp.text_frame.margin_right = 0
        sp.text_frame.margin_top = sp.text_frame.margin_bottom = 0
    except Exception:
        pass
    return sp


def add_text(slide, l, t, w, h, runs, size=16.5, bold=False, color=None,
             font=BODY_FONT, align=PP_ALIGN.LEFT, anchor=MSO_ANCHOR.TOP,
             italic=False, spacing=1.0, space_after=0.0):
    l, t, w, h = clamp_box(l, t, w, h)
    tb = slide.shapes.add_textbox(Inches(l), Inches(t), Inches(w), Inches(h))
    tf = _prep_tf(tb, anchor=anchor, wrap=True)
    if isinstance(runs, str):
        runs = [{"text": runs}]
    p = tf.paragraphs[0]
    p.alignment = align
    p.line_spacing = spacing
    p.space_after = Pt(space_after)
    for r in runs:
        run = p.add_run()
        run.text = r["text"]
        run.font.name = r.get("font", font)
        run.font.size = Pt(r.get("size", size))
        run.font.bold = r.get("bold", bold)
        run.font.italic = r.get("italic", italic)
        clr = r.get("color", color)
        if clr is not None:
            run.font.color.rgb = clr
    return tb


def add_bullets(slide, l, t, w, h, items, size=16.5, font=BODY_FONT,
                ink=None, marker_color=None, spacing=1.12, space_after=9.5,
                marker="\u25AA  "):
    l, t, w, h = clamp_box(l, t, w, h)
    tb = slide.shapes.add_textbox(Inches(l), Inches(t), Inches(w), Inches(h))
    tf = _prep_tf(tb, anchor=MSO_ANCHOR.TOP, wrap=True)
    if ink is None:
        ink = TEXT_INK
    if marker_color is None:
        marker_color = ACCENT_METAL

    for i, item in enumerate(items):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.alignment = PP_ALIGN.LEFT
        p.line_spacing = spacing
        p.space_after = Pt(space_after)

        m = p.add_run()
        m.text = marker
        m.font.name = font
        m.font.size = Pt(size)
        m.font.bold = True
        m.font.color.rgb = marker_color

        if isinstance(item, (list, tuple)):
            lead, payload = item[0], item[1]
            r1 = p.add_run()
            r1.text = lead + " "
            r1.font.name = font
            r1.font.size = Pt(size)
            r1.font.bold = True
            r1.font.color.rgb = ink

            r2 = p.add_run()
            r2.text = payload
            r2.font.name = font
            r2.font.size = Pt(size)
            r2.font.bold = False
            r2.font.color.rgb = ink
        else:
            r = p.add_run()
            r.text = str(item)
            r.font.name = font
            r.font.size = Pt(size)
            r.font.color.rgb = ink
    return tb


def add_picture_framed(slide, img_path, l, t, w, h, backing=SECONDARY_DARK,
                       border_color=ACCENT_METAL, border_w=1.2, inset=0.08):
    if not os.path.exists(img_path):
        raise FileNotFoundError(f"Missing asset: {img_path}")
    add_rect(slide, l, t, w, h, backing)
    slide.shapes.add_picture(
        img_path,
        Inches(l + inset), Inches(t + inset),
        Inches(w - 2 * inset), Inches(h - 2 * inset)
    )
    add_rect(slide, l, t, w, h, None, line_color=border_color, line_w=border_w, no_fill=True)


def add_notes(slide, transition, elaboration, bridge):
    text = (
        f"TRANSITION — {transition}\n\n"
        f"ELABORATION — {elaboration}\n\n"
        f"BRIDGE — {bridge}"
    )
    slide.notes_slide.notes_text_frame.text = text


def blank_slide(prs):
    return prs.slides.add_slide(prs.slide_layouts[6])


# ==============================================================================
# CHROME RENDERER (Shared Header + Footer across all content slides)
# ==============================================================================
def render_chrome(slide, num, title, kicker=None):
    # Left vertical stripe
    add_rect(slide, 0.00, 0.00, 0.18, SLIDE_H, PRIMARY_DARK)

    # Header zone
    if kicker:
        add_text(slide, 0.55, 0.42, 9.50, 0.32, kicker.upper(),
                 size=11, bold=True, color=ACCENT_METAL, font=BODY_FONT)
        add_text(slide, 0.55, 0.78, 10.50, 0.70, title,
                 size=28, bold=True, color=PRIMARY_DARK, font=TITLE_FONT)
        rule_y = 1.77
    else:
        add_text(slide, 0.55, 0.52, 11.00, 0.80, title,
                 size=30, bold=True, color=PRIMARY_DARK, font=TITLE_FONT)
        rule_y = 1.62

    # Accent rules
    add_rect(slide, 0.60, rule_y, 2.20, 0.055, ACCENT_METAL)
    add_rect(slide, 0.60, rule_y + 0.09, 12.10, 0.014, RULE_COLOR)

    # Slide number badge (oval)
    add_rect(slide, 12.30, 0.50, 0.58, 0.58, ACCENT_METAL, shape_type=MSO_SHAPE.OVAL)
    add_rect(slide, 12.30, 0.50, 0.58, 0.58, None, line_color=PRIMARY_DARK, line_w=1.0,
             shape_type=MSO_SHAPE.OVAL, no_fill=True)
    add_text(slide, 12.30, 0.50, 0.58, 0.58, f"{num:02d}", size=13, bold=True,
             color=PRIMARY_DARK, align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)

    # Footer
    footer_str = "WORLD WAR II \u00b7 1939\u20131945 \u00b7 THE LAST WORLD WAR"
    add_text(slide, 0.60, 7.12, 7.50, 0.25, footer_str,
             size=8.5, bold=True, color=TEXT_MUTED)
    add_text(slide, 11.55, 7.08, 1.45, 0.30, f"{num:02d} / {TOTAL:02d}",
             size=11, color=TEXT_MUTED, align=PP_ALIGN.RIGHT)


# ==============================================================================
# SLIDE BUILDERS (11 Distinct Layouts)
# ==============================================================================

# ── SLIDE 01: HERO COVER ──────────────────────────────────────────────────────
def slide_01(prs):
    sl = blank_slide(prs)
    img = asset("hero_cover")
    if os.path.exists(img):
        sl.shapes.add_picture(img, Inches(0), Inches(0), Inches(SLIDE_W), Inches(SLIDE_H))
    else:
        set_bg(sl, PRIMARY_DARK)

    # Inset gold border
    add_rect(sl, 0.30, 0.30, 12.733, 6.90, None, line_color=ACCENT_METAL, line_w=1.5, no_fill=True)

    # Central star emblem
    add_rect(sl, 6.233, 2.30, 0.866, 0.866, ACCENT_METAL, shape_type=MSO_SHAPE.STAR_5_POINT)

    # Title & Subtitles
    add_text(sl, 1.20, 3.20, 10.933, 1.10, "THE LAST WORLD WAR",
             size=56, bold=True, color=ACCENT_LIGHT, font=TITLE_FONT,
             align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)

    add_text(sl, 1.20, 4.38, 10.933, 0.55, "Six Years That Remade the Century",
             size=23, italic=True, color=CANVAS, font=TITLE_FONT,
             align=PP_ALIGN.CENTER)

    # Divider
    add_rect(sl, 5.166, 5.20, 3.00, 0.045, ACCENT_METAL)

    # Taglines
    add_text(sl, 1.20, 5.45, 10.933, 0.50,
             "SIX YEARS  \u00b7  SIXTY MILLION LIVES  \u00b7  ONE NEW WORLD ORDER",
             size=16, bold=True, color=ACCENT_LIGHT, align=PP_ALIGN.CENTER)

    add_text(sl, 1.20, 6.25, 10.933, 0.40,
             "At least 60 million dead, a majority of them civilians \u2014 and a peace agreement that still governs the planet",
             size=12.5, color=CANVAS, align=PP_ALIGN.CENTER)

    add_text(sl, 1.20, 6.95, 10.933, 0.30,
             "Photograph: US Marines raise the flag on Iwo Jima, Feb 1945 (Joe Rosenthal, US Gov / public domain)",
             size=10, color=ACCENT_LIGHT, align=PP_ALIGN.CENTER)

    add_notes(sl,
        transition="Open with the frame and the claim — this is one of the only photographs almost everyone can name, and it was taken on a volcanic island 7,000 miles from Berlin. That spread is the point.",
        elaboration="Every conflict before this one had been, at most, regional. World War II was fought on the ground in Europe, Africa, and Asia, across every ocean, and from the Arctic to the Solomon Islands. The real number underneath all the dates is the death count: the current consensus estimate is sixty to seventy-five million, and for the first time in any war most of them were civilians. That is roughly three percent of every person alive in 1940 — ended in six years.",
        bridge="So before we talk about armies and battles, let's sit with the scale of the event itself — because every slide after this is measured against it."
    )
    return sl


# ── SLIDE 02: DUAL STAT SHOWCASE ──────────────────────────────────────────────
def slide_02(prs):
    sl = blank_slide(prs)
    set_bg(sl, CANVAS)
    render_chrome(sl, 2, "The Deadliest Conflict in History", kicker="THE SCALE")

    # Left stat panel: 6 YEARS
    add_rect(sl, 0.60, 2.05, 5.85, 3.20, PRIMARY_DARK, adj=0.04)
    add_rect(sl, 0.60, 2.05, 0.11, 3.20, ACCENT_METAL)
    add_text(sl, 0.85, 2.50, 5.35, 1.10, "6", size=64, bold=True,
             color=ACCENT_LIGHT, font=TITLE_FONT, align=PP_ALIGN.CENTER)
    add_text(sl, 0.85, 3.70, 5.35, 0.40, "YEARS OF WAR", size=14, bold=True,
             color=ACCENT_METAL, align=PP_ALIGN.CENTER)
    add_text(sl, 0.85, 4.15, 5.35, 0.40, "September 1939 \u2013 September 1945",
             size=10.5, color=ON_DARK_TEXT, align=PP_ALIGN.CENTER)

    # Right stat panel: 60M+ DEAD
    add_rect(sl, 6.88, 2.05, 5.85, 3.20, PRIMARY_DARK, adj=0.04)
    add_rect(sl, 6.88, 2.05, 0.11, 3.20, ACCENT_METAL)
    add_text(sl, 7.13, 2.50, 5.35, 1.10, "60M+", size=64, bold=True,
             color=ACCENT_LIGHT, font=TITLE_FONT, align=PP_ALIGN.CENTER)
    add_text(sl, 7.13, 3.70, 5.35, 0.40, "DEAD WORLDWIDE", size=14, bold=True,
             color=ACCENT_METAL, align=PP_ALIGN.CENTER)
    add_text(sl, 7.13, 4.15, 5.35, 0.40, "estimates run to 75M; over half civilians",
             size=10.5, color=ON_DARK_TEXT, align=PP_ALIGN.CENTER)

    # Bottom insight bar
    add_rect(sl, 0.60, 5.55, 12.133, 1.25, SURFACE_ALT, line_color=RULE_COLOR, line_w=1.0)
    add_rect(sl, 0.60, 5.55, 0.11, 1.25, PRIMARY_DARK)
    add_text(sl, 0.85, 5.80, 11.60, 0.80,
             "No event in recorded history killed a larger share of humanity \u2014 roughly one person in thirty, worldwide.",
             size=14, bold=True, color=PRIMARY_DARK, align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)

    add_notes(sl,
        transition="You've seen the photograph; now the two numbers that should genuinely change how you think about this war.",
        elaboration="Six years sounds short — shorter than the career of a professional footballer. But measure the density. In barely two thousand days the war killed sixty to seventy-five million people. For scale: every soldier, sailor, airman and civilian — the war took about one in thirty of the whole human species as it stood in 1940. The physical damage matched the human: Berlin, Warsaw, London, Rotterdam, Tokyo, Manila, and hundreds of others were reduced to rubble fields that took two decades to clear.",
        bridge="A war this destructive does not begin at full size — it escalates from smaller crises. Let's trace the road in."
    )
    return sl


# ── SLIDE 03: HORIZONTAL TIMELINE RIBBON ──────────────────────────────────────
def slide_03(prs):
    sl = blank_slide(prs)
    set_bg(sl, CANVAS)
    render_chrome(sl, 3, "It Did Not Start Global", kicker="ORIGINS")

    # Central axis
    add_rect(sl, 0.60, 4.28, 12.133, 0.06, ACCENT_METAL)

    # 4 Nodes: (x, y, period, title, body, is_above)
    nodes = [
        (0.60, 2.05, "1931", "Manchuria", "Japan invades; the League of Nations protests and does nothing. The first alarm.", True),
        (3.69, 4.55, "1937", "Full Invasion", "Japan's war on China begins in earnest; millions die before 1939.", False),
        (6.78, 2.05, "1939", "Poland, 1 Sept", "Germany invades; Britain and France declare war two days later.", True),
        (9.87, 4.55, "1941", "Global by Default", "Barbarossa in June; Pearl Harbor in December. Now a world war.", False),
    ]

    for x, y, period, n_title, body, is_above in nodes:
        card_fill = WHITE_RGB if is_above else SURFACE_ALT
        border_col = ALLIES_BLUE if is_above else AXIS_CRIMSON

        # Card container
        add_rect(sl, x, y, 2.85, 1.96, card_fill, line_color=border_col, line_w=1.2)
        # Top accent stripe
        add_rect(sl, x, y, 2.85, 0.10, border_col)

        # Content inside card
        add_text(sl, x + 0.18, y + 0.20, 2.50, 0.34, n_title,
                 size=11.5, bold=True, color=PRIMARY_DARK, font=TITLE_FONT)
        add_text(sl, x + 0.18, y + 0.62, 2.50, 1.15, body,
                 size=9.5, color=TEXT_INK, spacing=1.05)

        # Date badge on axis
        badge_y = 4.10 if is_above else 4.40
        add_rect(sl, x + 0.08, badge_y, 1.10, 0.26, PRIMARY_DARK, adj=0.15)
        add_text(sl, x + 0.08, badge_y, 1.10, 0.26, period,
                 size=9, bold=True, color=ACCENT_LIGHT,
                 align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)

    add_notes(sl,
        transition="Every coalition war has a fuse that runs back further than the official start date. This one was really lit in Asia eight years before Europe's war began.",
        elaboration="In 1931 Japan took Manchuria and the League of Nations sent a report it could not enforce. In 1937 Japan's full invasion of China turned into a conflict that would eventually kill somewhere between fifteen and twenty million Chinese — many people do not realise the war in Asia was already staggering by 1939. In Europe, Germany remilitarised the Rhineland, annexed Austria, took Czechoslovakia, and still Britain and France adjusted their strategy rather than fight. Then came the Molotov-Ribbentrop pact of 1939, which let Hitler invade Poland without a second front.",
        bridge="The point of the timeline is not the dates — it's that each failure to stop small aggression made the next one bigger. That escalation produced the two coalitions we'll look at now."
    )
    return sl


# ── SLIDE 04: VERSUS DUEL SPLIT ───────────────────────────────────────────────
def slide_04(prs):
    sl = blank_slide(prs)
    set_bg(sl, CANVAS)
    render_chrome(sl, 4, "Two Coalitions, One War", kicker="THE COALITIONS")

    # Central VS badge
    add_rect(sl, 6.166, 3.65, 1.00, 0.55, ACCENT_METAL, adj=0.20)
    add_text(sl, 6.166, 3.65, 1.00, 0.55, "VS", size=18, bold=True,
             color=PRIMARY_DARK, font=TITLE_FONT, align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)

    cols = [
        {
            "x": 0.60, "w": 5.55, "banner": "THE ALLIES", "accent": ALLIES_BLUE,
            "img": asset("versus_allies"),
            "big": "50+", "label": "NATIONS", "sub": "the Grand Alliance by 1945",
            "bullets": [
                ["Core four:", "Britain, the USSR, the US, and China"],
                ["Instinct:", "fought for unconditional surrender after 1943"],
                ["Weight:", "over 100M mobilized across the alliance"]
            ]
        },
        {
            "x": 7.18, "w": 5.55, "banner": "THE AXIS", "accent": AXIS_CRIMSON,
            "img": asset("versus_axis"),
            "big": "3", "label": "FOUNDERS", "sub": "Berlin-Rome-Tokyo Pact, 1940",
            "bullets": [
                ["Core pact:", "the Tripartite Pact, signed September 1940"],
                ["Reach:", "peak 1942, from the Atlantic to the Pacific"],
                ["Fatal move:", "declared war on the US after Pearl Harbor"]
            ]
        }
    ]

    for c in cols:
        x, w, accent = c["x"], c["w"], c["accent"]
        # Outer container
        add_rect(sl, x, 2.00, w, 4.90, WHITE_RGB, line_color=accent, line_w=1.2)
        # Top banner
        add_rect(sl, x, 2.00, w, 0.44, accent)
        add_text(sl, x, 2.00, w, 0.44, c["banner"], size=11, bold=True,
                 color=WHITE_RGB, align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)

        # Portrait picture
        if os.path.exists(c["img"]):
            add_picture_framed(sl, c["img"], x + 0.16, 2.56, 2.00, 1.85,
                               backing=SECONDARY_DARK, border_color=accent, border_w=1.0)
        else:
            add_rect(sl, x + 0.16, 2.56, 2.00, 1.85, SECONDARY_DARK)

        # Stat panel
        add_rect(sl, x + 2.30, 2.56, 3.08, 1.85, PRIMARY_DARK, adj=0.05)
        add_rect(sl, x + 2.30, 2.56, 0.10, 1.85, accent)
        add_text(sl, x + 2.45, 2.70, 2.80, 0.38, c["big"], size=18, bold=True,
                 color=ACCENT_LIGHT, font=TITLE_FONT, align=PP_ALIGN.CENTER)
        add_rect(sl, x + 2.55, 3.14, 2.60, 0.014, ACCENT_METAL)
        add_text(sl, x + 2.45, 3.22, 2.80, 0.45, c["sub"], size=9.5,
                 color=ON_DARK_TEXT, align=PP_ALIGN.CENTER, spacing=1.05)
        add_text(sl, x + 2.45, 3.85, 2.80, 0.35, c["label"], size=9.5, bold=True,
                 color=ACCENT_METAL, align=PP_ALIGN.CENTER)

        # Bullets
        add_bullets(sl, x + 0.18, 4.62, w - 0.36, 2.10, c["bullets"],
                    size=12.5, spacing=1.08, space_after=7, marker_color=accent)

    add_notes(sl,
        transition="The timelines explain how the war grew; the coalitions explain how it was won and nearly lost.",
        elaboration="The Axis was an alliance of convenience, not of ideology — Japan and Germany had even been geopolitically hostile through the 1930s. Its three founders never agreed a shared strategy: Germany worked for a European empire, Japan for an Asian one, Italy for a Mediterranean revival. The Allies were just as strange in their own way — communist Russia, capitalist America, imperial Britain and republican China were enemies of each other's systems, united only by a common foe. Their stated goal from Casablanca in 1943 was unconditional surrender, which meant the Axis would not be allowed to negotiate its way out.",
        bridge="Inside those coalitions, the war was fought as 'total war' — every factory, lab, and citizen mobilised. That machinery is the next thing to understand."
    )
    return sl


# ── SLIDE 05: THREE PILLAR CARDS ──────────────────────────────────────────────
def slide_05(prs):
    sl = blank_slide(prs)
    set_bg(sl, CANVAS)
    render_chrome(sl, 5, "The Whole Society Mobilized", kicker="TOTAL WAR")

    pillars = [
        {
            "x": 0.60, "num": "01", "title": "Factories at War",
            "stat": "~296,000 aircraft built in the US alone",
            "bullets": [
                ["Shipbuilding:", "2,700+ Liberty ships in four years"],
                ["Tanks:", "88,000+ produced by American plants"],
                ["Soviet shift:", "1,500 factories moved beyond Urals"]
            ]
        },
        {
            "x": 4.76, "num": "02", "title": "Six Years on Rations",
            "stat": "British rationing lasted until 1954",
            "bullets": [
                ["Labour:", "women powered every war economy"],
                ["Food:", "farms fed armies before their towns"],
                ["Moral code:", "austerity was patriotism in uniform"]
            ]
        },
        {
            "x": 8.92, "num": "03", "title": "The Laboratory Weapon",
            "stat": "radar, penicillin, jets, atomic bomb",
            "bullets": [
                ["Radar:", "decided Britain's sky in 1940"],
                ["Medicine:", "penicillin saved tens of thousands"],
                ["The bomb:", "tested at Trinity, July 1945"]
            ]
        }
    ]

    for p in pillars:
        x = p["x"]
        # Container
        add_rect(sl, x, 2.05, 3.80, 4.80, WHITE_RGB, line_color=ACCENT_METAL, line_w=1.2)
        # Top accent bar
        add_rect(sl, x, 2.05, 3.80, 0.10, PRIMARY_DARK)

        # Number oval
        add_rect(sl, x + 0.18, 2.25, 0.50, 0.50, PRIMARY_DARK, shape_type=MSO_SHAPE.OVAL)
        add_text(sl, x + 0.18, 2.25, 0.50, 0.50, p["num"], size=12, bold=True,
                 color=ACCENT_LIGHT, align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)

        # Title
        add_text(sl, x + 0.80, 2.25, 2.85, 0.52, p["title"], size=14.5, bold=True,
                 color=PRIMARY_DARK, font=TITLE_FONT, anchor=MSO_ANCHOR.MIDDLE)

        # Stat band
        add_rect(sl, x + 0.18, 2.82, 3.44, 0.68, PRIMARY_DARK, adj=0.04)
        add_rect(sl, x + 0.18, 2.82, 0.10, 0.68, ACCENT_METAL)
        add_text(sl, x + 0.34, 2.85, 3.20, 0.62, p["stat"], size=11, bold=True,
                 color=ACCENT_LIGHT, align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)

        # Bullets
        add_bullets(sl, x + 0.22, 3.70, 3.36, 2.95, p["bullets"],
                    size=12, spacing=1.08, space_after=6)

    add_notes(sl,
        transition="Total war means the distinction between soldier and civilian disappears — and that is visible in how every belligerent rebuilt itself overnight.",
        elaboration="Consider just one country. American shipyards took roughly four years and a hundred days each to produce over twenty-seven hundred Liberty ships; Ford's plant at Willow Run turned out a B-24 bomber every hour at peak. On the other side, when German panzers pushed toward Moscow in 1941, the Soviets dismantled about fifteen hundred factories and relocated them east of the Ural mountains, some producing within a hundred days of arriving. And notice the label says home front, not home — in Britain, food, clothing and fuel were rationed from 1940 until 1954, nearly a decade after the war ended.",
        bridge="These economies did not just supply battles — they decided which side could afford to keep losing and absorb the cost. Let's name the real ledger."
    )
    return sl


# ── SLIDE 06: STAT GRID QUAD ──────────────────────────────────────────────────
def slide_06(prs):
    sl = blank_slide(prs)
    set_bg(sl, CANVAS)
    render_chrome(sl, 6, "Numbers the Mind Rejects", kicker="THE LEDGER")

    cards = [
        {"x": 0.60, "y": 2.00, "big": "60\u201375M", "label": "DEAD IN TOTAL,\nTHE ESTIMATE",
         "desc": "Over half were civilians \u2014 the first time in recorded warfare"},
        {"x": 6.88, "y": 2.00, "big": "100M", "label": "SOLDIERS\nMOBILIZED",
         "desc": "About 4% of the entire human population in 1940 served in uniform"},
        {"x": 0.60, "y": 4.55, "big": "~3%", "label": "OF HUMANITY\nKILLED",
         "desc": "Roughly one person in thirty on Earth in 1940 died in the war"},
        {"x": 6.88, "y": 4.55, "big": "50+", "label": "STATES FORMALLY\nAT WAR",
         "desc": "Virtually every region from the Arctic to the Pacific was touched"},
    ]

    for c in cards:
        x, y = c["x"], c["y"]
        # Card container
        add_rect(sl, x, y, 5.85, 2.25, WHITE_RGB, line_color=ACCENT_METAL, line_w=1.0, adj=0.04)
        # Top bar
        add_rect(sl, x, y, 5.85, 0.10, PRIMARY_DARK)

        # Big number
        add_text(sl, x + 0.28, y + 0.22, 1.80, 0.70, c["big"], size=36, bold=True,
                 color=PRIMARY_DARK, font=TITLE_FONT)

        # Label
        add_text(sl, x + 2.15, y + 0.22, 3.40, 0.65, c["label"], size=13.5, bold=True,
                 color=PRIMARY_DARK)

        # Descriptor
        add_text(sl, x + 2.15, y + 1.10, 3.40, 0.70, c["desc"], size=11,
                 color=TEXT_MUTED, spacing=1.06)

        # Star ornament
        add_rect(sl, x + 5.25, y + 1.72, 0.32, 0.32, ACCENT_METAL, shape_type=MSO_SHAPE.STAR_5_POINT)

    add_notes(sl,
        transition="The alliances and the factories give the shape; these four numbers give the weight.",
        elaboration="Take the top row seriously, because our brains are built to underweight large numbers. Sixty to seventy-five million people — and more than half of them were civilians. A hundred million soldiers were mobilized, which in a world of 2.3 billion people meant one in roughly twenty of everyone alive was under arms. When you read that about three percent of the entire species died inside that one conflict, set it against the First World War, where the comparable figure was closer to one percent. And it was genuinely global — over fifty independent states were formally at war.",
        bridge="Every one of those numbers is a person, and the next slide stops counting altogether — it just lets someone speak."
    )
    return sl


# ── SLIDE 07: SPOTLIGHT QUOTE MANIFESTO ────────────────────────────────────────
def slide_07(prs):
    sl = blank_slide(prs)
    set_bg(sl, CANVAS)
    render_chrome(sl, 7, "So Much Owed to So Few", kicker="BATTLE OF BRITAIN \u00b7 1940")

    # Framed picture on left
    img = asset("spotlight")
    if os.path.exists(img):
        add_picture_framed(sl, img, 0.60, 2.00, 4.80, 4.85,
                           backing=SECONDARY_DARK, border_color=ACCENT_METAL, border_w=1.2)
    else:
        add_rect(sl, 0.60, 2.00, 4.80, 4.85, SECONDARY_DARK)

    # Big quote glyph
    add_text(sl, 5.70, 2.00, 0.70, 0.55, "\u201C", size=52, bold=True,
             color=ACCENT_METAL, font=TITLE_FONT)

    # Quote text
    quote_str = "Never in the field of human conflict was so much owed by so many to so few."
    add_text(sl, 5.70, 2.50, 7.13, 1.25, quote_str, size=21, italic=True,
             color=PRIMARY_DARK, font=TITLE_FONT, spacing=1.08)

    # Citation band
    add_rect(sl, 5.70, 3.85, 7.13, 0.52, PRIMARY_DARK, adj=0.06)
    add_text(sl, 5.70, 3.85, 7.13, 0.52,
             "\u2014 Winston Churchill, House of Commons, 20 August 1940",
             size=11, italic=True, color=ACCENT_LIGHT,
             align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)

    # Takeaways
    takeaways = [
        ["The few:", "roughly 3,000 RAF pilots, average age about 20"],
        ["The odds:", "outnumbered by German bombers and fighters that summer"],
        ["The stakes:", "the planned invasion of Britain was postponed indefinitely"]
    ]
    add_bullets(sl, 5.70, 4.60, 7.13, 2.20, takeaways,
                size=12.5, spacing=1.08, space_after=6.5)

    add_notes(sl,
        transition="We have been on the scale of millions. It matters to come down to the scale of a few thousand people making a decision on a Tuesday.",
        elaboration="Churchill was praising the Royal Air Force pilots of the summer of 1940 — roughly three thousand of them, many still in their early twenties, flying fighters like the Spitfire and Hurricane against a German air force of several thousand aircraft that was trying to break Britain before any invasion could land. They were chronically short of pilots, and the average pilot who survived was promoted twice in a month because the ranks kept emptying. The invasion barges Hitler had gathered were stood down once the air force gave him no chance.",
        bridge="Churchill called it the Few — but the heaviest price of the war was not paid by them. It was paid by the civilians of two continents, which is what the ledger next shows."
    )
    return sl


# ── SLIDE 08: MATRIX DATA TABLE ───────────────────────────────────────────────
def slide_08(prs):
    sl = blank_slide(prs)
    set_bg(sl, CANVAS)
    render_chrome(sl, 8, "Counting the Uncountable", kicker="THE HUMAN COST")

    rows_data = [
        ("USSR", "~8.7M", "~18M"),
        ("China", "~3.5M", "~15M"),
        ("Germany", "~5.3M", "~1.5M"),
        ("Poland", "~0.2M", "~5.4M"),
        ("Japan", "~2.1M", "~0.9M"),
        ("USA", "~0.4M", "~11"),
    ]

    # Native table (7 rows, 3 cols)
    t_shape = sl.shapes.add_table(len(rows_data) + 1, 3, Inches(0.60), Inches(2.05), Inches(8.20), Inches(4.75))
    table = t_shape.table
    try:
        table.columns[0].width = Inches(3.35)
        table.columns[1].width = Inches(2.42)
        table.columns[2].width = Inches(2.42)
    except Exception:
        pass

    # Header row
    headers = ["NATION / THEATRE", "MILITARY DEATHS", "CIVILIAN DEATHS"]
    for col_idx, h_text in enumerate(headers):
        cell = table.cell(0, col_idx)
        cell.fill.solid()
        cell.fill.fore_color.rgb = PRIMARY_DARK
        cell.vertical_anchor = MSO_ANCHOR.MIDDLE
        cell.margin_left = cell.margin_right = Pt(6)
        p = cell.text_frame.paragraphs[0]
        p.alignment = PP_ALIGN.LEFT if col_idx == 0 else PP_ALIGN.CENTER
        p.text = h_text
        p.font.name = BODY_FONT
        p.font.size = Pt(11)
        p.font.bold = True
        p.font.color.rgb = ACCENT_LIGHT

    # Body rows
    for r_idx, row_vals in enumerate(rows_data, 1):
        bg = WHITE_RGB if r_idx % 2 == 1 else SURFACE_ALT
        for col_idx, val in enumerate(row_vals):
            cell = table.cell(r_idx, col_idx)
            cell.fill.solid()
            cell.fill.fore_color.rgb = bg
            cell.vertical_anchor = MSO_ANCHOR.MIDDLE
            cell.margin_left = cell.margin_right = Pt(6)
            p = cell.text_frame.paragraphs[0]
            p.alignment = PP_ALIGN.LEFT if col_idx == 0 else PP_ALIGN.CENTER
            p.text = val
            p.font.name = BODY_FONT
            p.font.size = Pt(12)
            p.font.bold = (col_idx > 0)
            p.font.color.rgb = TEXT_INK

    # Callout panel on right
    add_rect(sl, 9.10, 2.05, 3.633, 4.75, PRIMARY_DARK, adj=0.03)
    add_rect(sl, 9.10, 2.05, 0.11, 4.75, ACCENT_METAL)
    add_text(sl, 9.30, 2.25, 3.23, 0.30, "TOTAL CASUALTIES", size=10.5, bold=True,
             color=ACCENT_METAL, align=PP_ALIGN.CENTER)
    add_rect(sl, 9.40, 2.60, 3.03, 0.014, RULE_COLOR)
    add_text(sl, 9.30, 2.78, 3.23, 0.60, "60\u201375M", size=24, bold=True,
             color=ACCENT_LIGHT, font=TITLE_FONT, align=PP_ALIGN.CENTER)
    add_rect(sl, 9.40, 3.45, 3.03, 0.014, RULE_COLOR)

    # Sub-panel for insight
    add_rect(sl, 9.30, 3.65, 3.23, 2.20, SECONDARY_DARK, adj=0.04)
    add_text(sl, 9.45, 3.80, 2.93, 1.90,
             "Civilian deaths outnumbered military ones \u2014 for the first time in any war. Soviet and Chinese losses dwarfed the West's, and Poland lost ~17% of its total population.",
             size=10.5, color=ON_DARK_TEXT, align=PP_ALIGN.CENTER, spacing=1.06)

    add_text(sl, 9.30, 6.05, 3.23, 0.50, "MOSTLY CIVILIAN", size=12, bold=True,
             color=ACCENT_METAL, align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)

    add_notes(sl,
        transition="Here is the ledger the previous slide promised — and it corrects a common Western assumption about where the war was actually fought.",
        elaboration="Everything in this table is a rounded estimate, because counting the dead of a world war is an act of demography performed in ruins — figures for China alone range from fifteen to twenty-five million. But the shape is clear. The Soviet Union carried the heaviest single burden, roughly twenty-seven million dead. China lost maybe as many as twenty million. Notice the American column: four hundred thousand — tragic, but a rounding error against the Eastern Front. And the civilian column overturns the old arithmetic: more people died out of uniform than in it. Poland lost nearly a fifth of its population, including six million Jews murdered in the Holocaust.",
        bridge="This is the number-shaped reason the war's survivors built the postwar world the way they did. Which is exactly our last act."
    )
    return sl


# ── SLIDE 09: ASYMMETRIC EDITORIAL SPLIT ──────────────────────────────────────
def slide_09(prs):
    sl = blank_slide(prs)
    set_bg(sl, CANVAS)
    render_chrome(sl, 9, "The Tide Turned Twice", kicker="THE TURN")

    # Left Bullets
    bullets = [
        ["Midway, June 1942:", "four Japanese carriers sunk; the Pacific initiative over"],
        ["Stalingrad, Feb 1943:", "the 6th Army surrendered; Germany's first great defeat"],
        ["Kursk, July 1943:", "the largest tank battle halted the last eastern offensive"],
        ["D-Day, June 1944:", "156,000 troops landed on five beaches in one day"],
        ["Berlin, May 1945:", "Hitler dead, the Wehrmacht surrendered, Europe fell silent"]
    ]
    add_bullets(sl, 0.60, 2.10, 7.00, 4.50, bullets, size=14, spacing=1.10, space_after=9)

    # Right: Framed image + Stat card
    add_text(sl, 8.15, 1.74, 4.40, 0.24, "OMAHA BEACH \u00b7 6 JUNE 1944",
             size=9, bold=True, color=ACCENT_METAL)
    img = asset("asymmetric_turn")
    if os.path.exists(img):
        add_picture_framed(sl, img, 8.15, 1.95, 4.40, 3.10,
                           backing=SECONDARY_DARK, border_color=ACCENT_METAL, border_w=1.2)
    else:
        add_rect(sl, 8.15, 1.95, 4.40, 3.10, SECONDARY_DARK)

    # Stat card
    add_rect(sl, 8.15, 5.25, 4.40, 1.45, PRIMARY_DARK, adj=0.05)
    add_rect(sl, 8.15, 5.25, 0.11, 1.45, ACCENT_METAL)
    add_text(sl, 8.43, 5.40, 3.82, 0.50, "Putting It on the Axis", size=14, bold=True,
             color=ACCENT_LIGHT, font=TITLE_FONT)
    add_rect(sl, 8.43, 5.95, 3.82, 0.014, ACCENT_METAL)
    add_text(sl, 8.43, 6.05, 3.82, 0.55,
             "Midway \u00b7 Stalingrad \u00b7 Kursk \u00b7 D-Day \u2014 losses no coalition could replace",
             size=9.5, color=ON_DARK_TEXT, spacing=1.05)
    add_rect(sl, 12.05, 5.45, 0.28, 0.28, ACCENT_METAL, shape_type=MSO_SHAPE.STAR_5_POINT)

    add_notes(sl,
        transition="We have the cost and the coalitions. Now, where exactly did the war turn, and why does the answer sit in one disputed year?",
        elaboration="The turning points cluster in 1942-43 because the Axis overextended on its two widest fronts at once. In the Pacific, Midway in June 1942 cost Japan four fleet carriers in a single afternoon; with them went the ability to replace trained aircrews, and after that the Pacific was a slow, grinding retreat. On the Eastern Front, the German 6th Army was surrounded at Stalingrad and surrendered in February 1943 — the largest surrender in German military history. Kursk confirmed it four months later in the biggest tank battle ever fought. The Axis fact is now acts as a declining graph: once the Allies' factories and manpower began to outrun the Axis in 1943, no tactical genius could reverse it — only slow the timetable.",
        bridge="So the war was decided roughly four years in — and the last slide asked what was built from the wreckage, which is the peace we still live in."
    )
    return sl


# ── SLIDE 10: KEY TAKEAWAYS MOSAIC ────────────────────────────────────────────
def slide_10(prs):
    sl = blank_slide(prs)
    set_bg(sl, CANVAS)
    render_chrome(sl, 10, "The Peace We Still Live In", kicker="THE AFTERMATH")

    # Card 1 (Left)
    add_rect(sl, 0.60, 2.00, 5.85, 2.80, WHITE_RGB, line_color=PRIMARY_DARK, line_w=1.2, adj=0.04)
    add_rect(sl, 0.60, 2.00, 5.85, 0.10, PRIMARY_DARK)
    add_rect(sl, 0.78, 2.22, 0.50, 0.50, PRIMARY_DARK, shape_type=MSO_SHAPE.OVAL)
    add_text(sl, 0.78, 2.22, 0.50, 0.50, "01", size=14, bold=True,
             color=ACCENT_LIGHT, align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
    add_text(sl, 1.43, 2.22, 4.80, 0.50, "A NEW ARCHITECTURE", size=14, bold=True,
             color=PRIMARY_DARK, font=TITLE_FONT)
    body1 = (
        "The UN Charter was signed in 1945 and the Nuremberg trials made crimes against humanity a legal, not moral, fact.\n\n"
        "The great powers promised to talk first and fight last."
    )
    add_text(sl, 0.78, 2.86, 5.45, 1.75, body1, size=11.5, color=TEXT_INK, spacing=1.08)

    # Card 2 (Right)
    add_rect(sl, 6.88, 2.00, 5.85, 2.80, WHITE_RGB, line_color=PRIMARY_DARK, line_w=1.2, adj=0.04)
    add_rect(sl, 6.88, 2.00, 5.85, 0.10, PRIMARY_DARK)
    add_rect(sl, 7.06, 2.22, 0.50, 0.50, PRIMARY_DARK, shape_type=MSO_SHAPE.OVAL)
    add_text(sl, 7.06, 2.22, 0.50, 0.50, "02", size=14, bold=True,
             color=ACCENT_LIGHT, align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
    add_text(sl, 7.71, 2.22, 4.80, 0.50, "EMPIRES ENDED", size=14, bold=True,
             color=PRIMARY_DARK, font=TITLE_FONT)
    body2 = (
        "The war bankrupted and discredited the colonial powers; within a generation most of Africa and Asia had independent states.\n\n"
        "A map already redrawn once was redrawn again in the Cold War."
    )
    add_text(sl, 7.06, 2.86, 5.45, 1.75, body2, size=11.5, color=TEXT_INK, spacing=1.08)

    # Bottom banner
    add_rect(sl, 0.60, 5.05, 12.133, 1.75, PRIMARY_DARK, adj=0.03)
    add_rect(sl, 1.20, 5.28, 10.933, 0.04, ACCENT_METAL)
    add_text(sl, 0.60, 5.42, 12.133, 0.40, "THE ECHO", size=13, bold=True,
             color=ACCENT_METAL, align=PP_ALIGN.CENTER)
    add_text(sl, 1.20, 5.82, 10.933, 0.50,
             "The nuclear age, the Cold War, and the United Nations were all born inside these six years.",
             size=11.5, bold=True, color=ACCENT_LIGHT, align=PP_ALIGN.CENTER)
    add_text(sl, 1.20, 6.28, 10.933, 0.40,
             "So far \u2014 at that scale \u2014 no war has repeated the last one.",
             size=9.5, color=ON_DARK_TEXT, align=PP_ALIGN.CENTER)

    add_notes(sl,
        transition="Wars end in treaties; this one ended in an architecture. Almost everything you'd list as 'modern world' descends from 1945.",
        elaboration="The UN replaced the failed League in 1945 with 51 members and the veto-holding Security Council. The Nuremberg trials of 1945-46 established that individuals, not just states, could be tried for crimes against humanity — a legal first. The war also ended empires: Britain and France emerged triumphant but bankrupt, and by the 1960s most of Africa and Asia were independent. But the honest complication belongs here too: the victory powers had no clean hands — Allied firebombing of Dresden and Tokyo, the atomic bombs, and Soviet brutality in the occupied East all mean 'the good war' is a partial label. And the peace inherited the war's tension.",
        bridge="That tension became the Cold War — fifty years of nuclear standoff that inherited the colossal weaponry of 1945. And yet."
    )
    return sl


# ── SLIDE 11: HERO CLOSING CLIMAX ─────────────────────────────────────────────
def slide_11(prs):
    sl = blank_slide(prs)
    img = asset("hero_closing")
    if os.path.exists(img):
        sl.shapes.add_picture(img, Inches(0), Inches(0), Inches(SLIDE_W), Inches(SLIDE_H))
    else:
        set_bg(sl, PRIMARY_DARK)

    # Inset gold border
    add_rect(sl, 0.30, 0.30, 12.733, 6.90, None, line_color=ACCENT_METAL, line_w=1.5, no_fill=True)

    # Central star emblem
    add_rect(sl, 6.233, 2.30, 0.866, 0.866, ACCENT_METAL, shape_type=MSO_SHAPE.STAR_5_POINT)

    # Title
    add_text(sl, 1.20, 3.20, 10.933, 1.10, "THE LAST WORLD WAR",
             size=56, bold=True, color=ACCENT_LIGHT, font=TITLE_FONT,
             align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)

    # Divider
    add_rect(sl, 5.166, 4.35, 3.00, 0.045, ACCENT_METAL)

    # Pull quote & closing line
    add_text(sl, 1.20, 4.55, 10.933, 0.60, "\u201CSo far, it holds.\u201D",
             size=24, italic=True, color=CANVAS, font=TITLE_FONT, align=PP_ALIGN.CENTER)

    add_text(sl, 1.20, 5.35, 10.933, 0.50,
             "The peace that followed is the world we still share.",
             size=18, bold=True, color=ACCENT_LIGHT, align=PP_ALIGN.CENTER)

    add_text(sl, 1.20, 6.95, 10.933, 0.30,
             "Photograph: Roosevelt, Churchill and Stalin at Yalta, February 1945 (US Gov / public domain)",
             size=10, color=ACCENT_LIGHT, align=PP_ALIGN.CENTER)

    add_notes(sl,
        transition="We opened with the photograph of Iwo Jima and the claim that this was the last world war. Close by honoring that claim exactly.",
        elaboration="It has been over eighty years since September 1939, and no conflict has come close to the scale of 1939-45 — no sixty million dead, no hundred million mobilized, no coalition of fifty states against a pact of three. That is not because humanity became kinder at war. It is because the survivors built institutions — the UN, the veto, the nuclear taboo — designed to make great-power war unaffordable, and because the bomb made any repeat of the six-year war unspeakable in a new way. The Yalta photograph is the hinge of it all: the Big Three dividing the map of what would become the Cold War.",
        bridge="The photograph behind me is not from the war's end as celebration, but from its negotiation. The last world war was built in six years — and it has taken every year since to build the peace. So far, it holds."
    )
    return sl


# ==============================================================================
# AUDIT HARNESS
# ==============================================================================
EMU_PER_INCH = 914400
SLIDE_W_EMU = int(13.333 * EMU_PER_INCH)
SLIDE_H_EMU = int(7.500 * EMU_PER_INCH)
TOL = 3000


def _boxes(slide):
    out = []
    for sh in slide.shapes:
        if sh.has_text_frame and sh.text_frame.text.strip():
            out.append((sh.left, sh.top, sh.width, sh.height, sh.text_frame.text[:32]))
    return out


def _overlap(a, b, slack=EMU_PER_INCH // 20):
    ax, ay, aw, ah, _ = a
    bx, by, bw, bh, _ = b
    if ax + aw <= bx + slack or bx + bw <= ax + slack:
        return False
    if ay + ah <= by + slack or by + bh <= ay + slack:
        return False
    return True


def audit_deck(path, expected_slides=11, min_distinct_layouts=6, layouts=None):
    prs = Presentation(path)
    fails = []

    if len(prs.slides) != expected_slides:
        fails.append(f"slide count {len(prs.slides)} != {expected_slides}")
    if abs(prs.slide_width - SLIDE_W_EMU) > TOL:
        fails.append(f"width {prs.slide_width} != {SLIDE_W_EMU}")
    if abs(prs.slide_height - SLIDE_H_EMU) > TOL:
        fails.append(f"height {prs.slide_height} != {SLIDE_H_EMU}")

    for i, slide in enumerate(prs.slides, 1):
        if not slide.has_notes_slide:
            fails.append(f"slide {i}: missing notes")
        else:
            n = slide.notes_slide.notes_text_frame.text.strip()
            if len(n) < 120:
                fails.append(f"slide {i}: notes too short ({len(n)} chars)")

        for sh in slide.shapes:
            if sh.left is None:
                continue
            if sh.left < -TOL or sh.top < -TOL:
                fails.append(f"slide {i}: shape at negative coords ({sh.left},{sh.top})")
            if sh.left + sh.width > SLIDE_W_EMU + TOL:
                fails.append(f"slide {i}: shape overflows right edge")
            if sh.top + sh.height > SLIDE_H_EMU + TOL:
                fails.append(f"slide {i}: shape overflows bottom edge")

        tbs = _boxes(slide)
        for a in range(len(tbs)):
            for b in range(a + 1, len(tbs)):
                if _overlap(tbs[a], tbs[b]):
                    fails.append(f"slide {i}: TEXT OVERLAP '{tbs[a][4]}' vs '{tbs[b][4]}'")

        for sh in slide.shapes:
            if not sh.has_text_frame:
                continue
            for p in sh.text_frame.paragraphs:
                for r in p.runs:
                    if r.font.size and r.font.size.pt < 8:
                        fails.append(f"slide {i}: font {r.font.size.pt}pt below 8pt floor")

    if layouts:
        distinct = len(set(layouts))
        if distinct < min_distinct_layouts:
            fails.append(f"only {distinct} distinct layouts (< {min_distinct_layouts})")
        for a, b in zip(layouts, layouts[1:]):
            if a == b:
                fails.append(f"consecutive duplicate layout: {a}")

    if fails:
        print("✗ AUDIT FAILED:")
        for f in fails:
            print(f"   - {f}")
        return False
    print(f"✓ AUDIT PASSED: {path}")
    print(f"   Slides: {len(prs.slides)}, Distinct layouts: {len(set(layouts or []))}, Collisions: 0")
    return True


# ==============================================================================
# MAIN
# ==============================================================================
LAYOUTS = [
    "hero_cover",
    "dual_stat_showcase",
    "horizontal_timeline_ribbon",
    "versus_duel_split",
    "three_pillar_cards",
    "stat_grid_quad",
    "spotlight_quote_manifesto",
    "matrix_data_table",
    "asymmetric_editorial_split",
    "key_takeaways_mosaic",
    "hero_closing_climax",
]


def main():
    print("=" * 70)
    print("PPTmaker Builder Agent — World War II Presentation")
    print("=" * 70)

    prs = Presentation()
    prs.slide_width = Inches(SLIDE_W)
    prs.slide_height = Inches(SLIDE_H)

    # Metadata
    prs.core_properties.title = "The Last World War: Six Years That Remade the Century"
    prs.core_properties.author = "PPTmaker Multi-Agent System"
    prs.core_properties.subject = "World War II Historical Analysis"
    prs.core_properties.keywords = "World War II, 1939-1945, Allies, Axis, Total War, United Nations, History"
    prs.core_properties.comments = (
        "Generated by PPTmaker autonomous multi-agent studio. "
        "Images courtesy of Wikimedia Commons / US National Archives / UK Ministry of Defence."
    )

    builders = [
        ("01 hero_cover", slide_01),
        ("02 dual_stat_showcase", slide_02),
        ("03 horizontal_timeline_ribbon", slide_03),
        ("04 versus_duel_split", slide_04),
        ("05 three_pillar_cards", slide_05),
        ("06 stat_grid_quad", slide_06),
        ("07 spotlight_quote_manifesto", slide_07),
        ("08 matrix_data_table", slide_08),
        ("09 asymmetric_editorial_split", slide_09),
        ("10 key_takeaways_mosaic", slide_10),
        ("11 hero_closing_climax", slide_11),
    ]

    for name, fn in builders:
        print(f"  Rendering slide {name}...")
        fn(prs)

    print(f"\nSaving presentation -> {OUTPUT_PPTX}")
    prs.save(OUTPUT_PPTX)

    print("\nRunning Audit Harness...")
    ok = audit_deck(OUTPUT_PPTX, expected_slides=11, min_distinct_layouts=6, layouts=LAYOUTS)
    if not ok:
        sys.exit(1)
    print("\nBuild completed successfully!")


if __name__ == "__main__":
    main()
