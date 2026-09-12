"""
PPTmaker - Builder Agent (Premium Creative Edition)
Topic: Messi vs Ronaldo — The Definitive GOAT Debate
Design: Anti-monotony creative system with 12 distinct layout blueprints.
"""
import os

from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE

# ---------------------------------------------------------------------------
# THEME
# ---------------------------------------------------------------------------
NAVY = RGBColor(0x0E, 0x16, 0x26)
SLATE_DARK = RGBColor(0x15, 0x22, 0x38)
CYAN = RGBColor(0x00, 0xA8, 0xE8)
CRIMSON = RGBColor(0xE6, 0x39, 0x46)
GOLD = RGBColor(0xD4, 0xAF, 0x37)
GOLD_LIGHT = RGBColor(0xF3, 0xE5, 0xAB)
CANVAS = RGBColor(0xF7, 0xF9, 0xFC)
INK = RGBColor(0x1A, 0x20, 0x2C)
MUTED = RGBColor(0x64, 0x74, 0x8B)
RULE = RGBColor(0xD8, 0xE0, 0xEA)
WHITE_RGB = RGBColor(0xFF, 0xFF, 0xFF)

TITLE_FONT = "Georgia"
BODY_FONT = "Arial"

SLIDE_W = 13.333
SLIDE_H = 7.500
TOTAL = 11
ASSETS = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets_messi_ronaldo")


def asset(name):
    return os.path.join(ASSETS, name + ".jpg")


def set_bg(slide, color):
    slide.background.fill.solid()
    slide.background.fill.fore_color.rgb = color


def add_rect(slide, l, t, w, h, fill, line_color=None, line_w=None,
             shape_type=MSO_SHAPE.RECTANGLE, adj=None, no_fill=False):
    sp = slide.shapes.add_shape(shape_type, Inches(l), Inches(t), Inches(w), Inches(h))
    if no_fill:
        sp.fill.background()
    else:
        sp.fill.solid()
        sp.fill.fore_color.rgb = fill
    if line_color is None:
        sp.line.fill.background()
    else:
        sp.line.color.rgb = line_color
        sp.line.width = Pt(line_w if line_w else 0.75)
    if adj is not None:
        try:
            sp.adjustments[0] = adj
        except Exception:
            pass
    sp.shadow.inherit = False
    return sp


def add_text(slide, l, t, w, h, runs, size=18, bold=False, color=INK, font=BODY_FONT,
             align=PP_ALIGN.LEFT, anchor=MSO_ANCHOR.TOP, italic=False, spacing=1.0,
             space_after=0.0):
    tb = slide.shapes.add_textbox(Inches(l), Inches(t), Inches(w), Inches(h))
    tf = tb.text_frame
    tf.word_wrap = True
    tf.vertical_anchor = anchor
    tf.margin_left = 0
    tf.margin_right = 0
    tf.margin_top = 0
    tf.margin_bottom = 0
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
        run.font.color.rgb = r.get("color", color)
    return tb


def add_bullets(slide, l, t, w, h, items, size=16.5, spacing=1.12, space_after=9.5):
    tb = slide.shapes.add_textbox(Inches(l), Inches(t), Inches(w), Inches(h))
    tf = tb.text_frame
    tf.word_wrap = True
    tf.vertical_anchor = MSO_ANCHOR.TOP
    tf.margin_left = 0
    tf.margin_right = 0
    tf.margin_top = 0
    tf.margin_bottom = 0
    for i, item in enumerate(items):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.alignment = PP_ALIGN.LEFT
        p.line_spacing = spacing
        p.space_after = Pt(space_after)
        m = p.add_run()
        m.text = "\u25AA  "
        m.font.name = BODY_FONT
        m.font.size = Pt(size)
        m.font.bold = True
        m.font.color.rgb = GOLD
        if isinstance(item, (list, tuple)):
            lead, rest = item
            r1 = p.add_run()
            r1.text = lead + " "
            r1.font.name = BODY_FONT
            r1.font.size = Pt(size)
            r1.font.bold = True
            r1.font.color.rgb = INK
            r2 = p.add_run()
            r2.text = rest
            r2.font.name = BODY_FONT
            r2.font.size = Pt(size)
            r2.font.color.rgb = INK
        else:
            r = p.add_run()
            r.text = item
            r.font.name = BODY_FONT
            r.font.size = Pt(size)
            r.font.color.rgb = INK
    return tb


def add_stat(slide, l, t, w, h, stat, sub=None):
    add_rect(slide, l, t, w, h, NAVY, shape_type=MSO_SHAPE.ROUNDED_RECTANGLE, adj=0.05)
    add_rect(slide, l, t, 0.055, h, CYAN)
    add_rect(slide, l + 0.055, t, 0.055, h, CRIMSON)
    add_text(slide, l + 0.28, t + 0.15, w - 0.58, 0.74, stat,
             size=14.0, bold=True, color=GOLD_LIGHT, font=TITLE_FONT, spacing=1.05)
    if sub:
        add_rect(slide, l + 0.28, t + 0.94, w - 0.58, 0.014, GOLD)
        add_text(slide, l + 0.28, t + 1.00, w - 0.58, 0.34, sub,
                 size=9.5, color=RGBColor(0xD0, 0xDA, 0xE5))
    add_rect(slide, l + w - 0.50, t + 0.20, 0.28, 0.28, GOLD, shape_type=MSO_SHAPE.STAR_5_POINT)


def add_picture_frame(slide, img_path, l, t, w, h, gap=0.08):
    add_rect(slide, l, t, w, h, SLATE_DARK)
    pic = slide.shapes.add_picture(img_path, Inches(l + gap), Inches(t + gap),
                                   Inches(w - 2 * gap), Inches(h - 2 * gap))
    add_rect(slide, l, t, w, h, None, line_color=GOLD, line_w=1.2, no_fill=True)
    return pic


def add_header(slide, num, title, kicker=None):
    add_rect(slide, 0, 0, 0.09, SLIDE_H, CYAN)
    add_rect(slide, 0.09, 0, 0.09, SLIDE_H, CRIMSON)
    y = 0.42
    if kicker:
        add_text(slide, 0.55, y, 9.0, 0.32, kicker.upper(), size=11, bold=True, color=GOLD)
        add_text(slide, 0.55, y + 0.36, 10.5, 0.70, title, size=28, bold=True,
                 color=NAVY, font=TITLE_FONT)
        rule_y = y + 1.35
    else:
        add_text(slide, 0.55, y + 0.10, 11.0, 0.80, title, size=30, bold=True,
                 color=NAVY, font=TITLE_FONT)
        rule_y = y + 1.20
    add_rect(slide, 0.60, rule_y, 2.20, 0.055, GOLD)
    add_rect(slide, 0.60, rule_y + 0.09, 12.10, 0.014, RULE)
    add_rect(slide, 12.30, 0.50, 0.58, 0.58, GOLD, shape_type=MSO_SHAPE.OVAL)
    add_rect(slide, 12.30, 0.50, 0.58, 0.58, None, line_color=NAVY, line_w=1.0,
             shape_type=MSO_SHAPE.OVAL, no_fill=True)
    add_text(slide, 12.30, 0.50, 0.58, 0.58, f"{num:02d}", size=13, bold=True,
             color=NAVY, align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
    return rule_y


def add_footer(slide, num):
    add_text(slide, 0.60, 7.12, 7.50, 0.25,
             "MESSI VS RONALDO  \u2022  THE DEFINITIVE GOAT DEBATE",
             size=8.5, bold=True, color=MUTED)
    add_text(slide, 11.55, 7.08, 1.45, 0.30, f"{num:02d} / {TOTAL:02d}",
             size=11, color=MUTED, align=PP_ALIGN.RIGHT)


def add_dual_badge(slide, x, y, w=1.40, h=0.12):
    half = w / 2.0
    add_rect(slide, x, y, half, h, CYAN)
    add_rect(slide, x + half, y, half, h, CRIMSON)


def add_notes(slide, text):
    slide.notes_slide.notes_text_frame.text = text


def blank(prs):
    return prs.slides.add_slide(prs.slide_layouts[6])


def new_deck():
    prs = Presentation()
    prs.slide_width = Inches(SLIDE_W)
    prs.slide_height = Inches(SLIDE_H)
    prs.core_properties.title = "Messi vs Ronaldo: The Definitive GOAT Debate"
    prs.core_properties.author = "PPTmaker"
    prs.core_properties.subject = "Empirical analysis of football's greatest rivalry"
    return prs


IMG_X, IMG_W, IMG_H = 8.15, 4.40, 3.10
STAT_X, STAT_W = 8.15, 4.40


def content_side(slide, img, l=IMG_X, iw=IMG_W, ih=IMG_H):
    add_picture_frame(slide, asset(img), l, 1.95, iw, ih)
    label = img.upper().replace("_", " ")
    add_text(slide, l, 1.74, iw, 0.24, label, size=9, bold=True, color=GOLD)

# ---------------------------------------------------------------------------
# SLIDE 1 : TITLE — hero_cover
# ---------------------------------------------------------------------------
def slide_title(prs):
    s = blank(prs)
    s.shapes.add_picture(asset("title"), 0, 0, Inches(SLIDE_W), Inches(SLIDE_H))
    add_rect(s, 0.30, 0.30, SLIDE_W - 0.60, SLIDE_H - 0.60, None, line_color=GOLD, line_w=1.5, no_fill=True)
    add_dual_badge(s, 0.55, 0.50, w=1.40, h=0.12)
    add_rect(s, SLIDE_W / 2 - 0.43, 2.30, 0.86, 0.86, GOLD, shape_type=MSO_SHAPE.STAR_5_POINT)
    add_rect(s, SLIDE_W / 2 - 0.21, 2.52, 0.43, 0.43, SLATE_DARK, shape_type=MSO_SHAPE.STAR_5_POINT)
    add_text(s, 1.20, 3.20, SLIDE_W - 2.40, 1.10, "MESSI VS RONALDO",
             size=56, bold=True, color=GOLD_LIGHT, font=TITLE_FONT,
             align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
    add_text(s, 1.20, 4.38, SLIDE_W - 2.40, 0.55,
             "The Definitive Analysis of Football's Greatest Rivalry",
             size=23, italic=True, color=CANVAS, font=TITLE_FONT, align=PP_ALIGN.CENTER)
    add_rect(s, SLIDE_W / 2 - 1.50, 5.20, 3.00, 0.045, GOLD)
    add_text(s, 1.20, 5.45, SLIDE_W - 2.40, 0.50,
             "TWO TITANS   \u2022   TWO DECADES   \u2022   ONE UNREPEATABLE ERA",
             size=16, bold=True, color=GOLD_LIGHT, align=PP_ALIGN.CENTER)
    add_text(s, 1.20, 6.25, SLIDE_W - 2.40, 0.40,
             "TACTICAL GENIUS   \u2022   ATHLETIC PERFECTION   \u2022   HISTORIC SILVERWARE",
             size=12.5, color=CANVAS, align=PP_ALIGN.CENTER)
    add_text(s, 1.20, 6.95, SLIDE_W - 2.40, 0.30,
             "Prepared with PPTmaker Creative Multi-Agent System",
             size=10, color=RGBColor(0xA5, 0xB4, 0xC8), align=PP_ALIGN.CENTER)
    add_notes(s, "Transition / Hook: Welcome everyone. For nearly two decades, the global sporting landscape has been defined by an unprecedented rivalry between two icons: Lionel Messi and Cristiano Ronaldo. "
                 "Elaboration: Today, we look past subjective fan tribalism to conduct an empirical, data-driven analysis of their tactical DNA, club triumphs, individual hardware, direct El Clásico battles, international legacies, and late-career expansions. From Rosario to Madeira, their parallel journeys pushed the limits of human athletic excellence. "
                 "Bridge: Let us begin by examining the overall statistical landscape of their combined twenty-year supremacy.")


# ---------------------------------------------------------------------------
# SLIDE 2 : OVERVIEW — asymmetric_editorial_split
# ---------------------------------------------------------------------------
def slide_overview(prs):
    s = blank(prs)
    set_bg(s, CANVAS)
    add_header(s, 2, "An Unprecedented Era of Supremacy", kicker="Overview")
    add_bullets(s, 0.60, 2.10, 7.00, 4.50, [
        ("Two decades of dominance:", "shared 13 Ballon d'Or awards across 15 consecutive seasons"),
        ("Statistical absurdity:", "combined for over 1,750 official senior goals and 70 major trophies"),
        ("Direct confrontation:", "clashed in 36 head-to-head matches for club and country at peak fitness"),
        ("Global sporting revolution:", "drove football viewership, sponsorship valuations, and digital reach to record highs"),
        ("Symbiotic greatness:", "each titan admitted the other's relentless output pushed them to higher peaks"),
    ], size=16.5)
    content_side(s, "overview")
    add_stat(s, STAT_X, 5.25, STAT_W, 1.45, "13 Ballon d'Ors \u2022 1,750+ Goals",
             sub="36 head-to-head clashes \u2022 70 major senior trophies")
    add_footer(s, 2)
    add_notes(s, "Transition: To understand the magnitude of this rivalry, we must first appreciate the staggering numbers they generated together. "
                 "Elaboration: Never before in professional sports have two generational talents competed in the same domestic league, during their physical primes, representing the fiercest club rivals on earth\u2014Barcelona and Real Madrid. Between 2008 and 2023, they captured 13 out of 15 Ballon d'Or trophies. "
                 "Bridge: To appreciate how they got here, let us trace their contrasting origins.")


# ---------------------------------------------------------------------------
# SLIDE 3 : ORIGINS & RISE — horizontal_timeline_ribbon (4 nodes)
# ---------------------------------------------------------------------------
def slide_timeline(prs):
    s = blank(prs)
    set_bg(s, CANVAS)
    add_header(s, 3, "From Rosario to Madeira: Humble Origins", kicker="Genesis & Breakthrough")
    # Timeline axis line
    add_rect(s, 0.60, 4.28, 12.133, 0.06, GOLD)
    nodes = [
        ("2003\u20132004", "THE BREAKTHROUGH", "Messi debuts for Barca in 2004;\nRonaldo signs with Man United in 2003"),
        ("2008", "FIRST BALLON D'ORS", "Ronaldo captures his first UCL & Ballon d'Or;\nMessi lifts Olympic Gold in Beijing"),
        ("2009", "THE WAR BEGINS", "Ronaldo's world-record \u20ac94M\nmove to Real Madrid starts\n9 years of direct El Cl\xe1sico warfare"),
        ("2012\u20132018", "THE PEAK ERA", "Combined seven consecutive\nBallon d'Ors; the greatest\nindividual duel in sport history"),
    ]
    # Bottom card positions (alternating top and bottom)
    # Top nodes: bottom edge touches timeline
    # Bottom nodes: top edge below timeline
    # X positions evenly spaced
    xs = [0.60, 3.69, 6.78, 9.87]
    tops_first = [2.05, 4.55, 2.05, 4.55]  # alternating above/below axis
    
    for i, (date, title, body) in enumerate(nodes):
        is_top = (i % 2 == 0)
        y_top = 2.05 if is_top else 4.55
        fill = WHITE_RGB if (i % 2 == 0) else RGBColor(0xEE, 0xF2, 0xF7)
        border = CYAN if i < 2 else CRIMSON

        add_rect(s, xs[i], y_top, 2.85, 1.96, fill, line_color=border, line_w=1.2)
        # Top accent bar
        add_rect(s, xs[i], y_top, 2.85, 0.10, border)

        # Date badge anchored on timeline
        badge_top = 4.10 if is_top else 4.40
        add_rect(s, xs[i] + 0.08, badge_top, 1.10, 0.26, NAVY, shape_type=MSO_SHAPE.ROUNDED_RECTANGLE, adj=0.15)
        add_text(s, xs[i] + 0.08, badge_top, 1.10, 0.26, date, size=9, bold=True, color=GOLD_LIGHT,
                 align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)

        if is_top:
            # Content in top card
            add_text(s, xs[i] + 0.18, y_top + 0.20, 2.50, 0.34, title, size=11.5, bold=True, color=NAVY)
            add_text(s, xs[i] + 0.18, y_top + 0.65, 2.50, 0.85, body, size=9.5, color=INK, spacing=1.05)
        else:
            # Content in bottom card
            add_text(s, xs[i] + 0.18, y_top + 0.34, 2.50, 0.34, title, size=11.5, bold=True, color=NAVY)
            add_text(s, xs[i] + 0.18, y_top + 0.78, 2.50, 0.85, body, size=9.5, color=INK, spacing=1.05)

    add_footer(s, 3)
    add_notes(s, "Transition: Their origins could not have been more different, yet their trajectories led to a shared destiny on Europe's biggest stages. "
                 "Elaboration: Messi overcame growth hormone deficiency in Rosario through Barcelona's legendary La Masia academy, while Ronaldo conquered adversity in Madeira before dazzling at Sporting CP and Manchester United. By 2009, Ronaldo's move to Madrid created the greatest direct duel the sport has ever seen, with both players entering an extended peak that defined world football. "
                 "Bridge: Those divergent backgrounds sculpted two radically different tactical identities.")


# ---------------------------------------------------------------------------
# SLIDE 4 : TACTICAL DNA — versus_duel_split (50/50 side-by-side)
# ---------------------------------------------------------------------------
def slide_versus(prs):
    s = blank(prs)
    set_bg(s, CANVAS)
    add_header(s, 4, "Tactical DNA: Two Paths to Greatness", kicker="Playstyles")
    
    # Central VS badge
    add_rect(s, 6.166, 3.65, 1.00, 0.55, GOLD, shape_type=MSO_SHAPE.ROUNDED_RECTANGLE, adj=0.20)
    add_text(s, 6.166, 3.65, 1.00, 0.55, "VS", size=18, bold=True, color=NAVY,
             align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)

    # Left Column — MESSI
    lx, lw = 0.60, 5.55
    add_rect(s, lx, 2.00, lw, 4.90, WHITE_RGB, line_color=CYAN, line_w=1.2)
    add_rect(s, lx, 2.00, lw, 0.44, CYAN, adj=0.02)
    add_text(s, lx, 2.00, lw, 0.44, "LIONEL MESSI — THE PLAYMAKER", size=11, bold=True, color=WHITE_RGB,
             align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
    add_picture_frame(s, asset("messi_action"), lx + 0.16, 2.56, 2.00, 1.85)
    # Messi stat badge
    add_rect(s, lx + 2.36, 2.56, 2.98, 1.85, NAVY, shape_type=MSO_SHAPE.ROUNDED_RECTANGLE, adj=0.05)
    add_rect(s, lx + 2.36, 2.56, 0.10, 1.85, CYAN)
    add_text(s, lx + 2.55, 2.72, 2.64, 0.36, "375+ ASSISTS", size=16, bold=True, color=CYAN,
             align=PP_ALIGN.CENTER)
    add_rect(s, lx + 2.55, 3.14, 2.64, 0.014, GOLD)
    add_text(s, lx + 2.55, 3.20, 2.64, 0.50, "All-time official\ncareer assists record", size=10, color=GOLD_LIGHT,
             align=PP_ALIGN.CENTER)
    add_text(s, lx + 2.55, 3.80, 2.64, 0.38, "THE ORCHESTRATOR", size=9.5, bold=True, color=CYAN,
             align=PP_ALIGN.CENTER)
    # Messi bullets
    add_bullets(s, lx + 0.18, 4.62, lw - 0.36, 2.10, [
        ("Spatial vision:", "generational playmaking & dribbling"),
        ("Low gravity magic:", "microscopic control in tight spaces"),
        ("Late career pivot:", "deep midfield conductor"),
    ], size=12.5, spacing=1.08, space_after=7)

    # Right Column — RONALDO
    rx = 6.78
    add_rect(s, rx, 2.00, lw, 4.90, WHITE_RGB, line_color=CRIMSON, line_w=1.2)
    add_rect(s, rx, 2.00, lw, 0.44, CRIMSON, adj=0.02)
    add_text(s, rx, 2.00, lw, 0.44, "CRISTIANO RONALDO — THE FINISHER", size=11, bold=True, color=WHITE_RGB,
             align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
    add_picture_frame(s, asset("ronaldo_action"), rx + 0.16, 2.56, 2.00, 1.85)
    add_rect(s, rx + 2.36, 2.56, 2.98, 1.85, NAVY, shape_type=MSO_SHAPE.ROUNDED_RECTANGLE, adj=0.05)
    add_rect(s, rx + 2.36, 2.56, 0.10, 1.85, CRIMSON)
    add_text(s, rx + 2.55, 2.72, 2.64, 0.36, "130+ HEADERS", size=16, bold=True, color=CRIMSON,
             align=PP_ALIGN.CENTER)
    add_rect(s, rx + 2.55, 3.14, 2.64, 0.014, GOLD)
    add_text(s, rx + 2.55, 3.20, 2.64, 0.50, "Elite aerial leap \u2022\n780mm vertical \u2022 clinical poacher", size=10, color=GOLD_LIGHT,
             align=PP_ALIGN.CENTER)
    add_text(s, rx + 2.55, 3.80, 2.64, 0.38, "THE GOAL MACHINE", size=9.5, bold=True, color=CRIMSON,
             align=PP_ALIGN.CENTER)
    add_bullets(s, rx + 0.18, 4.62, lw - 0.36, 2.10, [
        ("Physical dominance:", "explosive acceleration & power"),
        ("Aerial supremacy:", "67 knockout UCL goals; unmatched leap"),
        ("Late career pivot:", "pure number 9 predator"),
    ], size=12.5, spacing=1.08, space_after=7)

    add_footer(s, 4)
    add_notes(s, "Transition: Their contrasting DNA is what made their battles so spellbinding to watch side-by-side. "
                 "Elaboration: Lionel Messi embodies spatial genius\u2014gliding past midfields with micro-touches, dictating rhythm, and recording the most assists in history. Cristiano Ronaldo embodies athletic perfection\u2014skying above defenders with towering headers and explosive striking. Both adapted brilliantly: Messi dropped deep as a conductor, Ronaldo transformed into the box's deadliest finisher. "
                 "Bridge: Those distinct superpowers fueled historic club supremacy across Europe.")


# ---------------------------------------------------------------------------
# SLIDE 5 : CLUB RECORDS — stat_grid_quad (2x2)
# ---------------------------------------------------------------------------
def slide_stats(prs):
    s = blank(prs)
    set_bg(s, CANVAS)
    add_header(s, 5, "Historic Club Supremacy in Numbers", kicker="Records & Milestones")
    
    stats = [
        ("140", "Most Goals\nUCL All-Time Leader", "Ronaldo — supreme longevity\nacross three elite leagues"),
        ("91", "Calendar Year Goals\nUntouchable 2012", "Messi — shattered Gerd Müller's\n40-year record in style"),
        ("4 / 5", "Champions Leagues\nCombined: Nine Titles", "Ronaldo 5 \u2022 Messi 4 \u2022\n3-peat 2016\u20132018 for Real Madrid"),
        ("10", "La Liga Titles\nBarcelona's Golden Era", "Messi — the face of Guardiola's\n2009 sextuple & 2015 treble"),
    ]
    
    # Positions for 2x2 grid
    grid = [(0.60, 2.00), (6.88, 2.00), (0.60, 4.55), (6.88, 4.55)]
    for (x, y), (big, title, desc) in zip(grid, stats):
        border = GOLD
        add_rect(s, x, y, 5.85, 2.25, WHITE_RGB, line_color=border, line_w=1.0,
                 shape_type=MSO_SHAPE.ROUNDED_RECTANGLE, adj=0.04)
        add_rect(s, x, y, 5.85, 0.10, NAVY, adj=0.02)
        add_text(s, x + 0.28, y + 0.22, 1.55, 0.70, big, size=38, bold=True, color=NAVY,
                 font=TITLE_FONT)
        add_text(s, x + 2.10, y + 0.22, 3.50, 0.65, title, size=14.5, bold=True, color=NAVY)
        # Description
        add_text(s, x + 2.10, y + 1.10, 3.50, 0.70, desc, size=11, color=MUTED, spacing=1.06)
        add_rect(s, x + 5.20, y + 1.72, 0.32, 0.32, GOLD, shape_type=MSO_SHAPE.STAR_5_POINT)

    add_footer(s, 5)
    add_notes(s, "Transition: No individual rivalry has ever been so thoroughly quantified — let us place their milestones side by side. "
                 "Elaboration: Ronaldo holds the UCL scoring record with 140 goals and an unbroken three-peat with Madrid. Messi holds the single calendar-year world record of 91 goals in 2012, eclipsing Gerd Müller. Together, they own nine European Crowns, sixteen La Liga titles, and four league championships in England alone. "
                 "Bridge: Those club numbers are matched by a breathtaking monopoly on individual honors.")


# ---------------------------------------------------------------------------
# SLIDE 6 : INDIVIDUAL HONORS — three_pillar_cards
# ---------------------------------------------------------------------------
def slide_pillars(prs):
    s = blank(prs)
    set_bg(s, CANVAS)
    add_header(s, 6, "Three Pillars of Individual Greatness", kicker="Accolades & Legacy")
    
    pillars = [
        ("01", "BALLON D'OR\nMONOPOLY", "8 for Messi\n5 for Ronaldo", [
            "Messi: 8-time winner, only player with 4 consecutive",
            "Ronaldo: 5, spanning United, Madrid & Portugal",
            "13 of 15 consecutive Ballon d'Ors shared",
        ]),
        ("02", "EUROPEAN\nGOLDEN SHOES", "6 for Messi\n4 for Ronaldo", [
            "Messi: all-time Golden Shoe record holder",
            "Ronaldo: 4 Shoes, unique cross-league feat (England + Spain)",
            "Unmatched scoring consistency for 16 seasons",
        ]),
        ("03", "ALL-TIME\nSCORING", "900+ Career Goals\n1,200+ Appearances", [
            "Ronaldo: first to 900 official career goals in history",
            "Messi: 850+ goals with 375+ assists",
            "Both in FIFPro World 11 for 16 consecutive seasons",
        ]),
    ]
    
    xs = [0.60, 4.76, 8.92]
    colors = [CYAN, GOLD, CRIMSON]
    for i, (num, title, stat, bullets) in enumerate(pillars):
        x = xs[i]
        accent = colors[i]
        add_rect(s, x, 2.05, 3.80, 4.80, WHITE_RGB, line_color=accent, line_w=1.4)
        add_rect(s, x, 2.05, 3.80, 0.10, accent)
        add_rect(s, x + 0.18, 2.25, 0.50, 0.50, NAVY, shape_type=MSO_SHAPE.OVAL)
        add_text(s, x + 0.18, 2.25, 0.50, 0.50, num, size=12, bold=True, color=GOLD_LIGHT,
                 align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
        add_text(s, x + 0.83, 2.25, 2.78, 0.52, title, size=14.5, bold=True, color=NAVY, font=TITLE_FONT)
        # Stat band
        add_rect(s, x + 0.18, 2.82, 3.44, 0.68, NAVY, shape_type=MSO_SHAPE.ROUNDED_RECTANGLE, adj=0.04)
        add_rect(s, x + 0.18, 2.82, 0.10, 0.68, accent)
        add_text(s, x + 0.34, 2.85, 3.28, 0.62, stat, size=11, bold=True, color=GOLD_LIGHT,
                 align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
        # Bullets
        bullet_y = 3.70
        add_bullets(s, x + 0.22, bullet_y, 3.36, 2.75,
                    [(a.split(":")[0] + ":" if ":" in a else a.split("\u2014")[0] + "\u2014",
                      a.split(":", 1)[1].strip() if ":" in a else a.split("\u2014", 1)[1].strip())
                     if (":" in a or "\u2014" in a) else a for a in bullets],
                    size=12, spacing=1.08, space_after=6)

    add_footer(s, 6)
    add_notes(s, "Transition: Let us dissect the hardware that confirms their sustained supremacy. "
                 "Elaboration: Messi's 8 Ballon d'Ors and 6 Golden Shoes reflect his unparalleled consistency, while Ronaldo's 5 and 4 — spanning England, Spain, and Italy — highlight unparalleled cross-league dominance. The third pillar: sheer productivity. Ronaldo became the first player to cross 900 official career goals, while Messi combines scoring with 375+ assists. "
                 "Bridge: Nowhere did those superpowers collide more directly than on El Clásico soil.")


# ---------------------------------------------------------------------------
# SLIDE 7 : EL CLÁSICO — spotlight_quote_manifesto
# ---------------------------------------------------------------------------
def slide_spotlight(prs):
    s = blank(prs)
    set_bg(s, CANVAS)
    add_header(s, 7, "The Theater of El Clásico: 2009–2018", kicker="Direct Confrontation")
    
    # Left picture panel
    add_picture_frame(s, asset("clasico"), 0.60, 2.00, 4.80, 4.85)
    
    # Giant quote icon
    add_text(s, 5.70, 2.00, 0.70, 0.55, "\u201C", size=52, bold=True, color=GOLD, font=TITLE_FONT)
    
    # Quote text
    add_text(s, 5.70, 2.60, 7.13, 1.30,
             "For nine years we elevated\nfootball above everything.",
             size=22, italic=True, color=NAVY, font=TITLE_FONT, spacing=1.08)
    
    # Citation band
    add_rect(s, 5.70, 3.95, 7.13, 0.52, NAVY, shape_type=MSO_SHAPE.ROUNDED_RECTANGLE, adj=0.06)
    add_text(s, 5.70, 3.95, 7.13, 0.52, "— Cristiano on the Messi rivalry  \u2022  La Liga, 2017",
             size=11, italic=True, color=GOLD_LIGHT, align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)

    # 2 key bullets below citation
    add_bullets(s, 5.70, 4.65, 7.13, 2.10, [
        ("30 direct El Clásicos:", "each derby drew 400M+ global viewers \u2014 the most-watched recurring fixture"),
        ("Signature moments:", "Ronaldo's \u201cCalma\u201d in 2012 vs Messi's shirt-hold climax in 2017 at the Bernabéu"),
        ("Evenly matched scoring:", "Messi 20, Ronaldo 18 \u2014 guarding the positional play vs the lethal counter"),
    ], size=12.5, spacing=1.08, space_after=6.5)

    add_footer(s, 7)
    add_notes(s, "Transition: The absolute apex of the rivalry was La Liga's El Clásico between 2009 and 2018. "
                 "Elaboration: Thirty official Clásico showdowns became global cultural events watched by 400 million. Messi scored 20 times in head-to-head derby meetings, Ronaldo 18. Each authored immortal imagery: Ronaldo silencing the Camp Nou with the 'Calma' gesture in 2012, and Messi holding his shirt aloft to Madrid's crowd in 2017. The duel mirrored a tactical contest \u2014 Guardiola's possession against Mourinho & Zidane's lethal transitions. "
                 "Bridge: But for years, skeptics pressed the same question about both: the national stage.")


# ---------------------------------------------------------------------------
# SLIDE 8 : HEAD-TO-HEAD LEDGER — matrix_data_table
# ---------------------------------------------------------------------------
def slide_matrix(prs):
    s = blank(prs)
    set_bg(s, CANVAS)
    add_header(s, 8, "The Empirical Ledger — Face to Face", kicker="Comparative Matrix")
    
    # Table container
    # Use pptx native table for crisp grid
    left, top, tw, th = Inches(0.60), Inches(2.05), Inches(8.20), Inches(4.75)
    rows_data = [
        ("Ballon d'Or Wins", "8", "5"),
        ("UCL Titles", "4", "5"),
        ("UCL Goals (All-Time)", "129", "140"),
        ("Direct Duel Goals (36 meets)", "22", "21"),
        ("International Trophies", "Copa 21/24, WC 2022, Finalissima", "Euro 2016, Nations Lg 2019"),
        ("Overall Career Goals", "850+", "900+"),
    ]
    
    table_shape = s.shapes.add_table(len(rows_data) + 1, 3, left, top, tw, th)
    table = table_shape.table
    try:
        table.columns[0].width = Inches(3.35)
        table.columns[1].width = Inches(2.42)
        table.columns[2].width = Inches(2.42)
    except Exception:
        pass

    headers = ["Metric / Honor", "LIONEL MESSI", "CRISTIANO RONALDO"]
    for col_idx, h in enumerate(headers):
        cell = table.cell(0, col_idx)
        cell.fill.solid()
        cell.fill.fore_color.rgb = NAVY
        cell.vertical_anchor = MSO_ANCHOR.MIDDLE
        cell.margin_top = Pt(0)
        cell.margin_bottom = Pt(0)
        p = cell.text_frame.paragraphs[0]
        p.text = h
        p.alignment = PP_ALIGN.CENTER
        p.font.bold = True
        p.font.color.rgb = GOLD_LIGHT if col_idx > 0 else GOLD
        p.font.size = Pt(11) if col_idx > 0 else Pt(12)

    for row_idx, (metric, v_messi, v_ronaldo) in enumerate(rows_data, start=1):
        vals = [metric, v_messi, v_ronaldo]
        is_alt = (row_idx % 2 == 0)
        for col_idx, val in enumerate(vals):
            cell = table.cell(row_idx, col_idx)
            cell.fill.solid()
            cell.fill.fore_color.rgb = RGBColor(0xEE, 0xF2, 0xF7) if is_alt else WHITE_RGB
            cell.vertical_anchor = MSO_ANCHOR.MIDDLE
            cell.margin_left = Pt(6)
            cell.margin_right = Pt(6)
            p = cell.text_frame.paragraphs[0]
            p.text = val
            p.alignment = PP_ALIGN.CENTER if col_idx > 0 else PP_ALIGN.LEFT
            p.font.bold = (col_idx > 0)
            p.font.color.rgb = INK
            p.font.size = Pt(10.5) if len(val) > 20 else Pt(12)

    # Right highlight callout
    add_rect(s, 9.10, 2.05, 3.633, 4.75, NAVY, shape_type=MSO_SHAPE.ROUNDED_RECTANGLE, adj=0.03)
    add_rect(s, 9.10, 2.05, 0.11, 4.75, GOLD)
    add_text(s, 9.30, 2.25, 3.23, 0.30, "THE NUMBERS SPEAK", size=10.5, bold=True, color=GOLD,
             align=PP_ALIGN.CENTER)
    add_rect(s, 9.40, 2.60, 3.03, 0.014, RULE)
    add_text(s, 9.30, 2.78, 3.23, 0.60, "900+  vs  850+ Goals", size=15, bold=True, color=CYAN,
             align=PP_ALIGN.CENTER)
    add_rect(s, 9.40, 3.45, 3.03, 0.014, RULE)
    
    # Entity tallies insight box
    add_rect(s, 9.30, 3.60, 3.23, 1.25, SLATE_DARK, shape_type=MSO_SHAPE.ROUNDED_RECTANGLE, adj=0.04)
    add_text(s, 9.30, 3.70, 3.23, 1.10,
             "Near-parity across every\nmajor statistical category,\nseparated only by narrative\nand philosophy.",
             size=10.5, color=RGBColor(0xD0, 0xDA, 0xE5), align=PP_ALIGN.CENTER, spacing=1.06)
    add_text(s, 10.30, 5.70, 1.00, 0.50, "NO\nLOSER", size=12, bold=True, color=GOLD,
             align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)

    add_footer(s, 8)
    add_notes(s, "Transition: A glance at the ledger reveals remarkable near-parity across every major honor. "
                 "Elaboration: Messi's 8 Ballon d'Ors and 2022 World Cup contrast Ronaldo's 5 Ballon d'Ors and his status as the UCL's all-time top scorer (140 goals) and first to 900 career goals. In head-to-head scoring, the margin is nearly identical: 22 direct goals for Messi vs 21 for Ronaldo. Statistically, only philosophy separates them. "
                 "Bridge: The final verdict came when both captains led their homelands to long-awaited glory.")


# ---------------------------------------------------------------------------
# SLIDE 9 : LONGEVITY — asymmetric_editorial_split
# ---------------------------------------------------------------------------
def slide_longevity(prs):
    s = blank(prs)
    set_bg(s, CANVAS)
    add_header(s, 9, "Redefining Longevity & Global Frontiers", kicker="The Final Chapter")
    add_bullets(s, 0.60, 2.10, 7.00, 4.50, [
        ("Unprecedented longevity:", "competing at elite levels past 37 with 1,200+ professional appearances each"),
        ("Ronaldo's Saudi frontier:", "joined Al-Nassr (2023), igniting a migration of global stars to the Middle East"),
        ("Messi's American frontier:", "signed with Inter Miami (2023), delivering Leagues Cup & MLS commercial boom"),
        ("Still the talismans:", "both remain active captains and focal points for Portugal and Argentina"),
        ("The scientific edge:", "strict nutrition, cryotherapy, and sleep protocols sustained 20 years without decline"),
    ], size=16.0)
    content_side(s, "longevity")
    add_stat(s, STAT_X, 5.25, STAT_W, 1.45, "Dominating Beyond Age 37",
             sub="Al-Nassr \u2022 Inter Miami \u2022 Captains at the World Cup")
    add_footer(s, 9)
    add_notes(s, "Transition: While most forwards retire by their mid-thirties, these two rewrote the limits of athletic aging. "
                 "Elaboration: In 2023, Ronaldo moved to Al-Nassr and Messi to Inter Miami, each transforming their new league commercially and culturally — triggering attendance records, sponsor windfalls, and Apple TV subscription surges. Their meticulous recovery regimes, stretching, and ice protocols proved that disciplined lifestyle work could extend peak performance beyond traditional boundaries. "
                 "Bridge: How should history weigh their final cultural legacy and verdict?")


# ---------------------------------------------------------------------------
# SLIDE 10 : THE VERDICT — key_takeaways_mosaic
# ---------------------------------------------------------------------------
def slide_verdict(prs):
    s = blank(prs)
    set_bg(s, CANVAS)
    add_header(s, 10, "The Verdict: Two Philosophies, One Era", kicker="Takeaways")
    
    # Left takeaway card
    add_rect(s, 0.60, 2.00, 5.85, 2.80, WHITE_RGB, line_color=CYAN, line_w=1.2,
             shape_type=MSO_SHAPE.ROUNDED_RECTANGLE, adj=0.04)
    add_rect(s, 0.60, 2.00, 5.85, 0.10, CYAN)
    add_rect(s, 0.78, 2.22, 0.50, 0.50, NAVY, shape_type=MSO_SHAPE.OVAL)
    add_text(s, 0.78, 2.22, 0.50, 0.50, "1", size=14, bold=True, color=GOLD_LIGHT,
             align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
    add_text(s, 1.43, 2.22, 4.60, 0.50, "THE NATURAL GENIUS", size=14, bold=True, color=CYAN)
    add_text(s, 0.78, 2.86, 5.45, 1.75,
             "If greatness is defined by spatial vision,\neffortless dribbling, selfless playmaking,\nand orchestral control \u2014 the answer tilts\nto Lionel Messi.",
             size=11.5, color=INK, spacing=1.08)

    # Right takeaway card
    add_rect(s, 6.88, 2.00, 5.85, 2.80, WHITE_RGB, line_color=CRIMSON, line_w=1.2,
             shape_type=MSO_SHAPE.ROUNDED_RECTANGLE, adj=0.04)
    add_rect(s, 6.88, 2.00, 5.85, 0.10, CRIMSON)
    add_rect(s, 7.06, 2.22, 0.50, 0.50, NAVY, shape_type=MSO_SHAPE.OVAL)
    add_text(s, 7.06, 2.22, 0.50, 0.50, "2", size=14, bold=True, color=GOLD_LIGHT,
             align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
    add_text(s, 7.71, 2.22, 4.60, 0.50, "THE ATHLETIC SPECIMEN", size=14, bold=True, color=CRIMSON)
    add_text(s, 7.06, 2.86, 5.45, 1.75,
             "If greatness is defined by athletic mastery,\naerial supremacy, lethal multi-league\nfinishing, and relentless willpower \u2014\nthe answer tilts to Cristiano Ronaldo.",
             size=11.5, color=INK, spacing=1.08)

    # Bottom synthesis banner
    add_rect(s, 0.60, 5.05, 12.133, 1.75, NAVY, shape_type=MSO_SHAPE.ROUNDED_RECTANGLE, adj=0.03)
    # Decorative gold line
    add_rect(s, 1.20, 5.28, 10.933, 0.04, GOLD)
    add_text(s, 0.60, 5.42, 12.133, 0.40, "THE ERA NO ONE WILL FORGET", size=13, bold=True, color=GOLD,
             align=PP_ALIGN.CENTER)
    add_text(s, 1.20, 5.82, 10.933, 0.50, "1.5 Billion Social Followers \u2022 20 Years \u2022 No True Loser",
             size=11.5, bold=True, color=GOLD_LIGHT, align=PP_ALIGN.CENTER)
    add_text(s, 1.20, 6.28, 10.933, 0.40, "A duopoly that built the global modern game \u2014 and inspired a generation of wingers, false nines, and strikers.",
             size=9.5, color=RGBColor(0xC7, 0xD2, 0xE1), align=PP_ALIGN.CENTER)

    add_footer(s, 10)
    add_notes(s, "Transition: We now arrive at the verdict that reflects a philosophical choice, not a scoring deficit. "
                 "Elaboration: If you value innate artistry, natural genius, and symphonic control, your choice is Messi. If you value supreme physical conditioning, skyward vertical leaps, and lethal adaptability across three leagues, your choice is Ronaldo. Together they form a duopoly that sold jerseys to a combined 1.5 billion followers, reshaped sponsor economics, and made football the world's most scalable sport. "
                 "Bridge: The debate may echo forever, but for our generation, the true victory belongs to the sport itself.")


# ---------------------------------------------------------------------------
# SLIDE 11 : CLOSING — hero_closing_climax
# ---------------------------------------------------------------------------
def slide_closing(prs):
    s = blank(prs)
    s.shapes.add_picture(asset("closing"), 0, 0, Inches(SLIDE_W), Inches(SLIDE_H))
    add_rect(s, 0.30, 0.30, SLIDE_W - 0.60, SLIDE_H - 0.60, None, line_color=GOLD, line_w=1.5, no_fill=True)
    add_dual_badge(s, 0.55, 0.50, w=1.40, h=0.12)
    add_rect(s, SLIDE_W / 2 - 0.43, 2.30, 0.86, 0.86, GOLD, shape_type=MSO_SHAPE.STAR_5_POINT)
    add_rect(s, SLIDE_W / 2 - 0.21, 2.52, 0.43, 0.43, SLATE_DARK, shape_type=MSO_SHAPE.STAR_5_POINT)
    add_text(s, 1.20, 3.20, SLIDE_W - 2.40, 1.10, "THE GOLDEN ERA",
             size=56, bold=True, color=GOLD_LIGHT, font=TITLE_FONT,
             align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
    add_rect(s, SLIDE_W / 2 - 1.50, 4.35, 3.00, 0.045, GOLD)
    add_text(s, 1.20, 4.55, SLIDE_W - 2.40, 0.55, "\u201cTwo Legends. One Unforgettable Era.\u201d",
             size=24, italic=True, color=CANVAS, font=TITLE_FONT, align=PP_ALIGN.CENTER)
    add_text(s, 1.20, 5.35, SLIDE_W - 2.40, 0.50, "The debate may continue, but football already won.",
             size=18, bold=True, color=GOLD_LIGHT, align=PP_ALIGN.CENTER)
    add_text(s, 1.20, 6.95, SLIDE_W - 2.40, 0.30,
             "Prepared with PPTmaker Creative Multi-Agent System",
             size=10, color=RGBColor(0xA5, 0xB4, 0xC8), align=PP_ALIGN.CENTER)
    add_notes(s, "Transition: In closing, whichever titan you lean towards, the larger truth is undeniable. "
                 "Elaboration: We were blessed to witness twenty uninterrupted years of fierce, respectful rivalry played at heights never reached before. Their battles elevated football to global theater and inspired the next generation of playmakers, wingers, and athletes. "
                 "Bridge: Thank you for your attention. I now open the floor to questions and discussion.")


def verify_deck(filepath: str, expected_slides: int = TOTAL):
    prs = Presentation(filepath)
    assert len(prs.slides) == expected_slides, f"Slide count mismatch: {len(prs.slides)} != {expected_slides}"
    assert abs(prs.slide_width - Inches(SLIDE_W)) < 3000, "Width is not 13.333 inches (16:9)"
    assert abs(prs.slide_height - Inches(SLIDE_H)) < 3000, "Height is not 7.500 inches (16:9)"
    for i, slide in enumerate(prs.slides, 1):
        assert slide.has_notes_slide, f"Slide {i} missing speaker notes"
        notes = slide.notes_slide.notes_text_frame.text.strip()
        assert len(notes) > 50, f"Slide {i} speaker notes too brief: '{notes}'"
    print(f"Deck verification passed successfully: {filepath} ({len(prs.slides)} slides, 100% compliant)")
    return True


def main():
    builders = [
        slide_title,        # 01 hero_cover
        slide_overview,     # 02 asymmetric_editorial_split
        slide_timeline,     # 03 horizontal_timeline_ribbon
        slide_versus,       # 04 versus_duel_split
        slide_stats,        # 05 stat_grid_quad
        slide_pillars,      # 06 three_pillar_cards
        slide_spotlight,    # 07 spotlight_quote_manifesto
        slide_matrix,       # 08 matrix_data_table
        slide_longevity,    # 09 asymmetric_editorial_split
        slide_verdict,      # 10 key_takeaways_mosaic
        slide_closing,      # 11 hero_closing_climax
    ]
    # Verify asset integrity check
    for img_name in ["title", "overview", "longevity", "closing"]:
        assert os.path.exists(asset(img_name)), f"Missing required asset: {img_name}.jpg"
    for img_name in ["messi_action", "ronaldo_action", "clasico"]:
        assert os.path.exists(asset(img_name)), f"Missing duel asset: {img_name}.jpg"

    prs = new_deck()
    for fn in builders:
        fn(prs)
    out = "Messi_vs_Ronaldo_Presentation.pptx"
    prs.save(out)
    print(f"Saved PowerPoint presentation: {out}")
    verify_deck(out, expected_slides=TOTAL)


if __name__ == "__main__":
    main()
