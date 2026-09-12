"""
PPTmaker - Builder Agent script  (premium edition, image-integrated)
Topic: The Indian Army - Guardians of the Nation
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
ARMY_GREEN = RGBColor(0x1F, 0x3D, 0x2B)
OLIVE = RGBColor(0x4A, 0x5D, 0x38)
CHARCOAL = RGBColor(0x23, 0x30, 0x3B)
GOLD = RGBColor(0xC9, 0xA2, 0x27)
GOLD_LIGHT = RGBColor(0xE9, 0xD0, 0x84)
CREAM = RGBColor(0xF9, 0xF4, 0xEB)
INK = RGBColor(0x21, 0x26, 0x28)
MUTED = RGBColor(0x6F, 0x77, 0x75)
CALL_BG = RGBColor(0xEA, 0xEF, 0xE1)
SAFFRON = RGBColor(0xFF, 0x99, 0x33)
FLAG_GREEN = RGBColor(0x13, 0x88, 0x08)
WHITE_RGB = RGBColor(0xFF, 0xFF, 0xFF)
RULE = RGBColor(0xDD, 0xD4, 0xC4)

TITLE_FONT = "Georgia"
BODY_FONT = "Arial"

SLIDE_W = 13.333
SLIDE_H = 7.5
TOTAL = 11
ASSETS = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets")


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


def add_bullets(slide, l, t, w, h, items, size=17, spacing=1.12, space_after=10):
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
    add_rect(slide, l, t, w, h, ARMY_GREEN, shape_type=MSO_SHAPE.ROUNDED_RECTANGLE, adj=0.05)
    add_rect(slide, l, t, 0.11, h, GOLD)
    add_text(slide, l + 0.32, t + 0.15, w - 0.66, 0.74, stat,
             size=14.5, bold=True, color=GOLD_LIGHT, font=TITLE_FONT, spacing=1.05)
    if sub:
        add_rect(slide, l + 0.32, t + 0.94, w - 0.66, 0.014, GOLD)
        add_text(slide, l + 0.32, t + 1.0, w - 0.66, 0.32, sub,
                 size=9.5, color=RGBColor(0xC7, 0xD2, 0xC9))
    star = add_rect(slide, l + w - 0.52, t + 0.22, 0.3, 0.3, GOLD,
                    shape_type=MSO_SHAPE.STAR_5_POINT)


def add_picture_frame(slide, img, l, t, w, h, gap=0.09):
    add_rect(slide, l, t, w, h, ARMY_GREEN)
    pic = slide.shapes.add_picture(img, Inches(l + gap), Inches(t + gap),
                                   Inches(w - 2 * gap), Inches(h - 2 * gap))
    add_rect(slide, l, t, w, h, None, line_color=GOLD, line_w=1.2, no_fill=True)
    return pic


def add_header(slide, num, title, kicker=None):
    add_rect(slide, 0, 0, 0.18, SLIDE_H, ARMY_GREEN)
    y = 0.42
    if kicker:
        add_text(slide, 0.55, y, 9.0, 0.32, kicker.upper(), size=11, bold=True, color=GOLD)
        add_text(slide, 0.55, y + 0.36, 10.5, 0.7, title, size=28, bold=True,
                 color=ARMY_GREEN, font=TITLE_FONT)
        rule_y = y + 1.35
    else:
        add_text(slide, 0.55, y + 0.1, 11.0, 0.8, title, size=30, bold=True,
                 color=ARMY_GREEN, font=TITLE_FONT)
        rule_y = y + 1.2
    add_rect(slide, 0.6, rule_y, 2.1, 0.055, GOLD)
    add_rect(slide, 0.6, rule_y + 0.09, 12.1, 0.014, RULE)
    add_rect(slide, 12.30, 0.5, 0.58, 0.58, GOLD, shape_type=MSO_SHAPE.OVAL)
    add_rect(slide, 12.30, 0.5, 0.58, 0.58, None, line_color=ARMY_GREEN, line_w=1.0,
             shape_type=MSO_SHAPE.OVAL, no_fill=True)
    add_text(slide, 12.30, 0.5, 0.58, 0.58, "{:02d}".format(num), size=13, bold=True,
             color=ARMY_GREEN, align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
    return rule_y


def add_footer(slide, num):
    add_text(slide, 0.6, 7.12, 6.0, 0.25, "THE INDIAN ARMY  \u2022  SERVICE BEFORE SELF",
             size=8, color=MUTED)
    add_text(slide, 11.55, 7.08, 1.45, 0.3, "{:02d} / {:02d}".format(num, TOTAL),
             size=11, color=MUTED, align=PP_ALIGN.RIGHT)


def add_tricolor(slide, x, y, w=1.15, band=0.1):
    add_rect(slide, x, y, w, band, SAFFRON)
    add_rect(slide, x, y + band, w, band, WHITE_RGB)
    add_rect(slide, x, y + 2 * band, w, band, FLAG_GREEN)


def add_notes(slide, text):
    slide.notes_slide.notes_text_frame.text = text


def blank(prs):
    return prs.slides.add_slide(prs.slide_layouts[6])


def new_deck():
    prs = Presentation()
    prs.slide_width = Inches(SLIDE_W)
    prs.slide_height = Inches(SLIDE_H)
    prs.core_properties.title = "The Indian Army - Guardians of the Nation"
    prs.core_properties.author = "PPTmaker"
    prs.core_properties.subject = "An overview of the Indian Army"
    return prs


IMG_X, IMG_W = 8.15, 4.4
IMG_H = 3.1
STAT_X, STAT_W = 8.15, 4.4


def content_side(slide, img, l=IMG_X, iw=IMG_W, ih=IMG_H):
    add_picture_frame(slide, asset(img), l, 1.95, iw, ih)
    label = img.upper()
    add_text(slide, l, 1.75, iw, 0.25, label, size=9, bold=True, color=GOLD)


# ---------------------------------------------------------------------------
# SLIDE 1 : TITLE
# ---------------------------------------------------------------------------
def slide_title(prs):
    s = blank(prs)
    s.shapes.add_picture(asset("title"), 0, 0, Inches(SLIDE_W), Inches(SLIDE_H))
    add_rect(s, 0.3, 0.3, SLIDE_W - 0.6, SLIDE_H - 0.6, None, line_color=GOLD, line_w=1.5, no_fill=True)
    add_tricolor(s, 0.55, 0.5, w=1.15, band=0.1)

    add_rect(s, SLIDE_W / 2 - 0.43, 2.42, 0.86, 0.86, GOLD, shape_type=MSO_SHAPE.STAR_5_POINT)
    add_rect(s, SLIDE_W / 2 - 0.21, 2.64, 0.43, 0.43, OLIVE, shape_type=MSO_SHAPE.STAR_5_POINT)

    add_text(s, 1.2, 3.3, SLIDE_W - 2.4, 1.1, "THE INDIAN ARMY",
             size=56, bold=True, color=GOLD_LIGHT, font=TITLE_FONT,
             align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
    add_text(s, 1.2, 4.45, SLIDE_W - 2.4, 0.55, "Guardians of the Nation",
             size=24, italic=True, color=CREAM, font=TITLE_FONT, align=PP_ALIGN.CENTER)

    add_rect(s, SLIDE_W / 2 - 1.35, 5.25, 2.7, 0.045, GOLD)
    add_text(s, 1.2, 5.5, SLIDE_W - 2.4, 0.55,
             "\u0938\u0947\u0935\u093e \u092a\u0930\u092e\u094b \u0927\u0930\u094d\u092e\u0903   \u2022   Service Before Self",
             size=17, bold=True, color=GOLD_LIGHT, align=PP_ALIGN.CENTER)
    add_text(s, 1.2, 6.35, SLIDE_W - 2.4, 0.4, "VALOUR   \u2022   DUTY   \u2022   LEGACY",
             size=13, color=CREAM, align=PP_ALIGN.CENTER)
    add_text(s, 1.2, 7.0, SLIDE_W - 2.4, 0.3, "Prepared with PPTmaker",
             size=10, color=RGBColor(0xAF, 0xBF, 0xB4), align=PP_ALIGN.CENTER)

    add_notes(s, "Welcome the audience. Introduce the topic: the Indian Army is India's land "
                 "warfare force and the guardian of the nation's borders and unity. Explain the "
                 "journey we will cover - from legacy of valour to modern transformation - and "
                 "set a tone of pride and gratitude.")


# ---------------------------------------------------------------------------
# SLIDE 2 : OVERVIEW
# ---------------------------------------------------------------------------
def slide_overview(prs):
    s = blank(prs)
    set_bg(s, CREAM)
    add_header(s, 2, "What Is the Indian Army?", kicker="Overview")
    add_bullets(s, 0.6, 2.1, 7.0, 4.5, [
        ("Land combat branch", "of the Indian Armed Forces - the largest of its three services"),
        ("World's largest standing army", "- about 1.24 million active troops, plus reserves"),
        ("All-volunteer force", "where every soldier joins by free choice and national pride"),
        ("Headquartered in New Delhi", "- the President of India is the Supreme Commander"),
        ("Guided by the motto", "\u201cService Before Self\u201d (\u0938\u0947\u0935\u093e \u092a\u0930\u092e\u094b \u0927\u0930\u094d\u092e\u0903)"),
    ], size=17)
    content_side(s, "overview")
    add_stat(s, STAT_X, 5.25, STAT_W, 1.45, "The largest standing army on Earth",
             sub="~1.24M active \u2022 ~0.9M reserves \u2022 100% volunteer")
    add_footer(s, 2)
    add_notes(s, "Define the Indian Army as the land-based and largest component of the Indian "
                 "Armed Forces. Emphasise that it is the largest standing army in the world "
                 "with over 1.2 million active personnel. The Army is all-volunteer and the "
                 "President of India is its Supreme Commander.")


# ---------------------------------------------------------------------------
# SLIDE 3 : HISTORY
# ---------------------------------------------------------------------------
def slide_history(prs):
    s = blank(prs)
    set_bg(s, CREAM)
    add_header(s, 3, "A Legacy of Valour", kicker="History")
    add_bullets(s, 0.6, 2.1, 7.0, 4.5, [
        ("Roots in 1895:", "the presidency armies were unified into the Indian Army"),
        ("World War I:", "1.3 million Indian soldiers served; over 74,000 made the supreme sacrifice"),
        ("World War II:", "the Army grew to 2.5 million - history's largest volunteer force"),
        ("1947-1950:", "a new Army built under Indian command after independence"),
        ("Army Day 15 January:", "marks Field Marshal K. M. Cariappa assuming command"),
    ], size=16)
    content_side(s, "history")
    add_stat(s, STAT_X, 5.25, STAT_W, 1.45, "Battle honours on three continents",
             sub="From the Somme to Kargil - a 131-year journey")
    add_footer(s, 3)
    add_notes(s, "Walk through the timeline: the Army was founded in 1895 and fought in the two "
                 "World Wars, becoming the largest volunteer army in history during WWII. After "
                 "independence it was restructured under Indian leadership. Army Day is 15 "
                 "January, when Field Marshal K. M. Cariappa took over as the first Indian "
                 "Commander-in-Chief.")


# ---------------------------------------------------------------------------
# SLIDE 4 : WARS
# ---------------------------------------------------------------------------
def slide_wars(prs):
    s = blank(prs)
    set_bg(s, CREAM)
    add_header(s, 4, "Four Wars, One Resolve", kicker="Conflicts")
    add_bullets(s, 0.6, 2.1, 7.0, 4.5, [
        ("1947-48:", "first defence of Jammu & Kashmir against invasion"),
        ("1962:", "the Sino-Indian conflict in the high Himalayas"),
        ("1965:", "Indo-Pak war - the Army held the Punjab front"),
        ("1971:", "a decisive victory that liberates Bangladesh today"),
        ("1999:", "Kargil War - icy peaks recaptured under Operation Vijay"),
    ], size=17)
    content_side(s, "wars")
    add_stat(s, STAT_X, 5.25, STAT_W, 1.45, "Victory in every war against Pakistan",
             sub="1971: ~93,000 POWs - largest surrender since WWII")
    add_footer(s, 4)
    add_notes(s, "Cover the four major wars. Use 1971 as the highlight: India's decisive "
                 "victory led to the birth of Bangladesh and the largest military surrender "
                 "since WWII. Mention Kargil 1999 as a recent example of valour at extreme "
                 "altitude.")


# ---------------------------------------------------------------------------
# SLIDE 5 : STRUCTURE
# ---------------------------------------------------------------------------
def slide_structure(prs):
    s = blank(prs)
    set_bg(s, CREAM)
    add_header(s, 5, "Structure & Organisation", kicker="Organisation")
    add_bullets(s, 0.6, 2.1, 7.0, 4.5, [
        ("Seven operational commands", "guard every frontier and region of India"),
        ("Combat arms:", "Infantry, Armoured Corps, Artillery, Mechanised Infantry"),
        ("Supporting corps:", "Engineers, Signals, Army Aviation, Army Air Defence"),
        ("Led by the Chief of the Army Staff", "under the President as Supreme Commander"),
        ("Field formations:", "regiment, brigade, division, corps"),
    ], size=17)
    content_side(s, "structure")
    add_stat(s, STAT_X, 5.25, STAT_W, 1.45, "A proud regimental system",
             sub="7 commands \u2022 more than 80% of the Armed Forces")
    add_footer(s, 5)
    add_notes(s, "Describe the organisation: the Army is divided into seven operational "
                 "commands. The combat arms - infantry, armour, artillery and mechanised "
                 "infantry - are supported by engineers, signals, aviation and air defence. "
                 "The professional head is the Chief of the Army Staff.")


# ---------------------------------------------------------------------------
# SLIDE 6 : ETHOS
# ---------------------------------------------------------------------------
def slide_ethos(prs):
    s = blank(prs)
    set_bg(s, CREAM)
    add_header(s, 6, "Core Ethos: Service Before Self", kicker="Values")
    add_bullets(s, 0.6, 2.1, 7.0, 4.5, [
        ("Motto:", "\u201c\u0938\u0947\u0935\u093e \u092a\u0930\u092e\u094b \u0927\u0930\u094d\u092e\u0903\u201d - service is the highest duty"),
        ("Courage", "that holds the line, even in the face of death"),
        ("Discipline, integrity and sacrifice", "- the pillars of military life"),
        ("Duty in extremes", "from Siachen's ice to the Thar's blazing sands"),
        ("Regimental brotherhood", "that binds soldiers for life"),
    ], size=16)
    content_side(s, "ethos")
    add_stat(s, STAT_X, 5.25, STAT_W, 1.45, "\u201cService Before Self\u201d",
             sub="The creed that defines every soldier")
    add_footer(s, 6)
    add_notes(s, "Speak about the Army's ethos. The motto Sev\u0101 Paramo Dharma\u1e25 means "
                 "'Service is the eternal duty.' Courage, discipline and selfless sacrifice "
                 "are visible in the extreme conditions soldiers face - freezing peaks, "
                 "deserts, jungles and flood plains.")


# ---------------------------------------------------------------------------
# SLIDE 7 : OPERATIONS
# ---------------------------------------------------------------------------
def slide_operations(prs):
    s = blank(prs)
    set_bg(s, CREAM)
    add_header(s, 7, "Landmark Operations", kicker="Operations")
    add_bullets(s, 0.6, 2.1, 7.0, 4.5, [
        ("Operation Meghdoot (1984):", "securing Siachen, the world's highest battlefield"),
        ("Operation Vijay (1961):", "liberation of Goa from Portuguese rule"),
        ("Operation Cactus (1988):", "foiling a coup attempt in the Maldives"),
        ("2016 surgical strikes:", "dismantling terror launchpads across the Line of Control"),
        ("UN peacekeeping:", "decades of service on missions across the globe"),
    ], size=16)
    content_side(s, "operations")
    add_stat(s, STAT_X, 5.25, STAT_W, 1.45, "Combat and compassion",
             sub="Siachen snowfields - the highest battlefield on Earth")
    add_footer(s, 7)
    add_notes(s, "Highlight famous operations: Meghdoot secured Siachen, the world's highest "
                 "battlefield; Operation Vijay liberated Goa in 1961; Operation Cactus saved "
                 "the Maldives in 1988; the 2016 surgical strikes showed precision "
                 "counter-terror ability. India is a major UN peacekeeping contributor.")


# ---------------------------------------------------------------------------
# SLIDE 8 : BEYOND THE BATTLEFIELD
# ---------------------------------------------------------------------------
def slide_humanitarian(prs):
    s = blank(prs)
    set_bg(s, CREAM)
    add_header(s, 8, "Beyond the Battlefield", kicker="Nation Building")
    add_bullets(s, 0.6, 2.1, 7.0, 4.5, [
        "First responders in floods, earthquakes and avalanches",
        ("Operation Surya Hope (2013):", "lifesaving rescues in the Uttarakhand deluge"),
        "Building strategic border roads, bridges and infrastructure",
        "Medical camps, relief and education in remote, disaster-hit areas",
        ("UN peacekeeping:", "among the world's largest troop contributors"),
    ], size=16)
    content_side(s, "relief")
    add_stat(s, STAT_X, 5.25, STAT_W, 1.45, "The Army saves lives every day",
             sub="Humanitarian aid & disaster relief across India")
    add_footer(s, 8)
    add_notes(s, "The Army's role extends far beyond war. It is India's first responder in "
                 "natural disasters - floods, earthquakes and avalanches - and builds vital "
                 "border infrastructure. It has contributed more troops to UN peacekeeping "
                 "than most nations on Earth.")


# ---------------------------------------------------------------------------
# SLIDE 9 : MODERNISATION
# ---------------------------------------------------------------------------
def slide_modern(prs):
    s = blank(prs)
    set_bg(s, CREAM)
    add_header(s, 9, "Modernising the Force", kicker="Future-Forward")
    add_bullets(s, 0.6, 2.1, 7.0, 4.5, [
        ("Agnipath (2022):", "young Agniveers join for 4 years of dynamic service"),
        ("Women in combat:", "women officers now serve in combat arms, incl. Army Aviation"),
        ("Integrated Battle Groups", "for agile, technology-enabled warfare"),
        ("Indigenisation:", "Indian-made equipment under Atmanirbhar Bharat"),
        ("Academies:", "NDA, IMA Dehradun and OTA groom tomorrow's leaders"),
    ], size=16)
    content_side(s, "modern")
    add_stat(s, STAT_X, 5.25, STAT_W, 1.45, "A leaner, smarter, tech-enabled Army",
             sub="Agniveers \u2022 women in combat \u2022 indigenous hardware")
    add_footer(s, 9)
    add_notes(s, "Talk about the future: Agnipath inducts young Agniveers for a 4-year short "
                 "service. Women officers now serve in combat roles including Army Aviation. "
                 "Integrated Battle Groups and indigenisation (Atmanirbhar Bharat) aim at a "
                 "leaner, more lethal force.")


# ---------------------------------------------------------------------------
# SLIDE 10 : HONOURING THE BRAVE
# ---------------------------------------------------------------------------
def slide_honour(prs):
    s = blank(prs)
    set_bg(s, CREAM)
    add_header(s, 10, "Honouring the Brave", kicker="Gallantry")
    add_bullets(s, 0.6, 2.1, 7.0, 4.5, [
        ("Param Vir Chakra:", "India's highest gallantry award for battlefield courage"),
        ("21 heroes", "have been awarded the PVC - many of them posthumously"),
        ("Kargil Vijay Diwas (26 July)", "and Army Day (15 Jan) honour their sacrifice"),
        ("War memorials", "keep the memory of the fallen alive"),
        ("Our duty:", "gratitude and respect for soldiers and their families"),
    ], size=17)
    content_side(s, "honour")
    add_stat(s, STAT_X, 5.25, STAT_W, 1.45, "\u201cJai Hind\u201d - the nation bows to its protectors",
             sub="21 Param Vir Chakra awardees \u2022 countless acts of valour")
    add_footer(s, 10)
    add_notes(s, "Recognise the sacrifice of the brave. The Param Vir Chakra is India's "
                 "highest wartime gallantry award, with only 21 recipients. Kargil Vijay Diwas "
                 "and Army Day remind us to honour the fallen and respect the families who "
                 "support our soldiers.")


# ---------------------------------------------------------------------------
# SLIDE 11 : CLOSING
# ---------------------------------------------------------------------------
def slide_closing(prs):
    s = blank(prs)
    s.shapes.add_picture(asset("closing"), 0, 0, Inches(SLIDE_W), Inches(SLIDE_H))
    add_rect(s, 0.3, 0.3, SLIDE_W - 0.6, SLIDE_H - 0.6, None, line_color=GOLD, line_w=1.5, no_fill=True)
    add_tricolor(s, 0.55, 0.5, w=1.15, band=0.1)

    add_rect(s, SLIDE_W / 2 - 0.43, 2.5, 0.86, 0.86, GOLD, shape_type=MSO_SHAPE.STAR_5_POINT)
    add_rect(s, SLIDE_W / 2 - 0.21, 2.72, 0.43, 0.43, OLIVE, shape_type=MSO_SHAPE.STAR_5_POINT)

    add_text(s, 1.2, 3.35, SLIDE_W - 2.4, 1.0, "JAI HIND!",
             size=58, bold=True, color=GOLD_LIGHT, font=TITLE_FONT,
             align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
    add_rect(s, SLIDE_W / 2 - 1.35, 4.45, 2.7, 0.045, GOLD)
    add_text(s, 1.2, 4.7, SLIDE_W - 2.4, 0.55, "\u201cService Before Self\u201d",
             size=24, italic=True, color=CREAM, font=TITLE_FONT, align=PP_ALIGN.CENTER)
    add_text(s, 1.2, 5.5, SLIDE_W - 2.4, 0.5, "Guarding 1.4 billion dreams - Thank You!",
             size=17, color=GOLD_LIGHT, align=PP_ALIGN.CENTER)
    add_text(s, 1.2, 7.0, SLIDE_W - 2.4, 0.3, "Prepared with PPTmaker",
             size=10, color=RGBColor(0xAF, 0xBF, 0xB4), align=PP_ALIGN.CENTER)

    add_notes(s, "Close with gratitude. Summarise the key message: the Indian Army guards the "
                 "nation's borders and its 1.4 billion citizens, embodied by the motto Service "
                 "Before Self. Thank the audience and invite questions.")


def main():
    prs = new_deck()
    builders = [
        slide_title, slide_overview, slide_history, slide_wars, slide_structure,
        slide_ethos, slide_operations, slide_humanitarian, slide_modern,
        slide_honour, slide_closing,
    ]
    for fn in builders:
        fn(prs)
    out = "The_Indian_Army_Presentation.pptx"
    prs.save(out)
    print("Saved: {0}".format(out))
    print("Slides: {0}".format(len(prs.slides)))


if __name__ == "__main__":
    main()