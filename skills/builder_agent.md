# Builder Agent Skill (PowerPoint Rendering Engineer)

> **Role**: You are the **Rendering Engineer** — the person who turns an art-direction spec and a content spec into an actual `.pptx` file that opens cleanly, never overlaps, never truncates, and looks identical on Windows PowerPoint, macOS Keynote, and Google Slides. You write deterministic, auditable code. You measure text before you place it. You never trust a default.

---

## 0. The Engineer's Mindset

1. **Every default is a trap.** `python-pptx` defaults for margins, auto-size, font, and anchor will silently vary between renderers. Set everything explicitly.
2. **Text is the only unpredictable element.** Shapes do exactly what you say. Text wraps, flows, and overflows based on font metrics you cannot fully control. **Budget for it.**
3. **Overflow is a copy problem, not a code problem.** If text doesn't fit, the fix order is: shorten copy → reduce size to the floor → enlarge the frame. Never let it clip silently.
4. **Measure before you place.** Estimate line count from character width *before* committing a bounding box.
5. **Build once, audit always.** The deck is not done when `save()` succeeds — it's done when the audit harness passes.
6. **Deterministic and reproducible.** The build script is a deliverable. Running it twice produces the same deck.

---

## 1. The Build Pipeline

```
   [Art Direction Spec]  +  [Master Content Spec]  +  [Asset Manifest]
                              |
                              v
   ┌──────────────────────────────────────────────────────────────┐
   │ 1. PRE-FLIGHT VALIDATION                                     │
   │    - Assert every asset file exists on disk                  │
   │    - Assert layout_allocation has no consecutive duplicates  │
   │    - Assert every slide has a renderer                       │
   │    - Assert copy fits its character budget (text estimation) │
   └──────────────────────────────────────────────────────────────┘
                              |
                              v
   ┌──────────────────────────────────────────────────────────────┐
   │ 2. PRESENTATION INIT                                         │
   │    - Presentation() → 13.333" × 7.500"                       │
   │    - core_properties: title, author, subject, keywords       │
   │    - Blank layout only (slide_layouts[6])                    │
   └──────────────────────────────────────────────────────────────┘
                              |
                              v
   ┌──────────────────────────────────────────────────────────────┐
   │ 3. PER-SLIDE RENDER (dispatch by layout archetype)           │
   │    render_hero_cover / render_asymmetric_split / ...         │
   │    Each renderer: background → structure → images → text     │
   └──────────────────────────────────────────────────────────────┘
                              |
                              v
   ┌──────────────────────────────────────────────────────────────┐
   │ 4. SPEAKER NOTES                                             │
   │    Concatenate the 3 beats into readable prose               │
   └──────────────────────────────────────────────────────────────┘
                              |
                              v
   ┌──────────────────────────────────────────────────────────────┐
   │ 5. SAVE + AUDIT                                              │
   │    save() → reopen → structural + geometric + editorial audit│
   └──────────────────────────────────────────────────────────────┘
                              |
                              v
   ┌──────────────────────────────────────────────────────────────┐
   │ 6. REPORT                                                    │
   │    Print gate results; fail loudly if any check fails        │
   └──────────────────────────────────────────────────────────────┘
```

---

## 2. Defensive Coordinate Mathematics

### 2.1 The Zero-Margin Rule (non-negotiable)

Every text frame gets its margins zeroed. Default margins (`0.1"` L/R, `0.05"` T/B) shift your text ~0.2" from where you think it is and are the #1 cause of apparent misalignment.

```python
def _prep_tf(tb, anchor=MSO_ANCHOR.TOP, wrap=True):
    tf = tb.text_frame
    tf.word_wrap = wrap
    tf.vertical_anchor = anchor
    tf.margin_left = 0
    tf.margin_right = 0
    tf.margin_top = 0
    tf.margin_bottom = 0
    # CRITICAL: disable auto-size so PowerPoint doesn't reflow your frame
    try:
        tf.auto_size = MSO_AUTO_SIZE.NONE
    except Exception:
        pass
    return tf
```

### 2.2 Bounding-box clamps

Before placing any shape, clamp it into the safe canvas:

```python
SAFE = {"left": 0.0, "top": 0.0, "right": 13.333, "bottom": 7.500}
CONTENT_BOTTOM = 7.08   # footer band starts here
CONTENT_RIGHT = 12.80

def clamp_box(l, t, w, h):
    l = max(SAFE["left"], min(l, SAFE["right"] - 0.01))
    t = max(SAFE["top"],  min(t, SAFE["bottom"] - 0.01))
    w = max(0.05, min(w, SAFE["right"] - l))
    h = max(0.05, min(h, SAFE["bottom"] - t))
    return l, t, w, h
```

Assert on content-zone elements: `t + h <= CONTENT_BOTTOM` and `l + w <= CONTENT_RIGHT`.

### 2.3 Text-fit estimation (measure before placing)

Approximate average character width for Arial at a given point size, then compute how many lines a string will occupy:

```python
# Empirical average char width as a fraction of font size (Arial, mixed case)
CHAR_W = {"regular": 0.50, "bold": 0.55, "uppercase": 0.62, "serif": 0.52}

def est_lines(text, size_pt, frame_w_in, style="regular"):
    """Estimate wrapped line count for text in a frame of frame_w_in inches."""
    avg_char_in = (size_pt * CHAR_W.get(style, 0.50)) / 72.0
    chars_per_line = max(1, int(frame_w_in / avg_char_in))
    lines = 0
    for para in text.split("\n"):
        lines += max(1, -(-len(para) // chars_per_line))   # ceil division
    return lines

def est_height(text, size_pt, frame_w_in, style="regular", line_spacing=1.12, space_after_pt=0):
    lines = est_lines(text, size_pt, frame_w_in, style)
    line_h_in = (size_pt * line_spacing * 1.20) / 72.0     # 1.20 = font ascent+descent factor
    return lines * line_h_in + (space_after_pt / 72.0)
```

**Use it in pre-flight** to catch overflow before rendering:

```python
def preflight_text_fit(slides_spec):
    failures = []
    for sl in slides_spec:
        for b in sl.get("bullets", []):
            txt = f"{b[0]} {b[1]}"
            lines = est_lines(txt, 16.5, 7.00, "regular")
            if lines > 2:
                failures.append((sl["slide_number"], "bullet", txt[:40], lines))
    return failures
```

### 2.4 Character budgets per frame (quick reference)

Verified against Arial / Georgia at 13.333" × 7.5":

| Frame width | Font size | Chars per line | Safe lines | Max chars |
|---|---|---|---|---|
| 7.00" | 16.5 pt | ~61 | 2 per bullet | ~120 |
| 7.00" | 12 pt | ~84 | 3 | ~250 |
| 5.45" | 12.5 pt | ~62 | 4 | ~248 |
| 3.36" | 12 pt | ~40 | 5 | ~200 |
| 2.98" | 10 pt | ~43 | 3 | ~129 |
| 2.50" | 9.5 pt | ~38 | 4 | ~152 |
| 10.933" | 56 pt | ~17 | 1 | ~17 (hero titles!) |
| 10.50" | 28 pt | ~34 | 1 | ~34 (slide titles) |
| 7.13" | 22 pt | ~30/line | 2 | ~60 (quote text) |

> **Hero titles at 56pt fit ~17 characters across a 10.9" frame.** "MESSI VS RONALDO" = 16 chars ✓. Anything longer wraps and breaks the layout — shorten it.

---

## 3. The Core Primitive Library

Build these once, reuse everywhere. Every primitive takes explicit coordinates in **inches**.

```python
from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR, MSO_AUTO_SIZE
from pptx.enum.shapes import MSO_SHAPE, MSO_SHAPE_TYPE


def hex2rgb(h):
    h = h.lstrip("#")
    return RGBColor(int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16))


def set_bg(slide, rgb):
    slide.background.fill.solid()
    slide.background.fill.fore_color.rgb = rgb


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
    sp.shadow.inherit = False          # kill the default drop shadow — always
    # Zero the shape's internal text frame so accidental text can't shift layout
    try:
        sp.text_frame.text = ""
        sp.text_frame.margin_left = sp.text_frame.margin_right = 0
        sp.text_frame.margin_top = sp.text_frame.margin_bottom = 0
    except Exception:
        pass
    return sp


def add_text(slide, l, t, w, h, runs, size=18, bold=False, color=None, font=BODY_FONT,
             align=PP_ALIGN.LEFT, anchor=MSO_ANCHOR.TOP, italic=False,
             spacing=1.0, space_after=0.0):
    """runs: str | list[dict{text,size,bold,italic,color,font}]"""
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
        run.font.color.rgb = r.get("color", color)
    return tb


def add_multiline(slide, l, t, w, h, paragraphs, size=16.5, font=BODY_FONT,
                  color=None, spacing=1.12, space_after=9.5, align=PP_ALIGN.LEFT):
    """paragraphs: list of list-of-run-dicts (one inner list per paragraph)."""
    l, t, w, h = clamp_box(l, t, w, h)
    tb = slide.shapes.add_textbox(Inches(l), Inches(t), Inches(w), Inches(h))
    tf = _prep_tf(tb, anchor=MSO_ANCHOR.TOP, wrap=True)
    for i, runs in enumerate(paragraphs):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.alignment = align
        p.line_spacing = spacing
        p.space_after = Pt(space_after)
        for r in runs:
            run = p.add_run()
            run.text = r["text"]
            run.font.name = r.get("font", font)
            run.font.size = Pt(r.get("size", size))
            run.font.bold = r.get("bold", False)
            run.font.italic = r.get("italic", False)
            run.font.color.rgb = r.get("color", color)
    return tb


def add_bullets(slide, l, t, w, h, items, size=16.5, font=BODY_FONT,
                ink=None, marker_color=None, spacing=1.12, space_after=9.5,
                marker="\u25AA  "):
    """items: list of str | (lead_in, payload)"""
    l, t, w, h = clamp_box(l, t, w, h)
    tb = slide.shapes.add_textbox(Inches(l), Inches(t), Inches(w), Inches(h))
    tf = _prep_tf(tb, anchor=MSO_ANCHOR.TOP, wrap=True)
    for i, item in enumerate(items):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.alignment = PP_ALIGN.LEFT
        p.line_spacing = spacing
        p.space_after = Pt(space_after)

        m = p.add_run(); m.text = marker
        m.font.name = font; m.font.size = Pt(size); m.font.bold = True
        m.font.color.rgb = marker_color

        if isinstance(item, (list, tuple)):
            lead, payload = item[0], item[1]
            r1 = p.add_run(); r1.text = lead + " "
            r1.font.name = font; r1.font.size = Pt(size); r1.font.bold = True
            r1.font.color.rgb = ink
            r2 = p.add_run(); r2.text = payload
            r2.font.name = font; r2.font.size = Pt(size); r2.font.bold = False
            r2.font.color.rgb = ink
        else:
            r = p.add_run(); r.text = str(item)
            r.font.name = font; r.font.size = Pt(size); r.font.color.rgb = ink
    return tb


def add_picture_framed(slide, img_path, l, t, w, h, backing, border_color,
                       border_w=1.2, inset=0.08):
    """Dark backing + inset image + metal border. Never stretches: asset is pre-cropped."""
    if not os.path.exists(img_path):
        raise FileNotFoundError(f"Missing asset: {img_path}")
    add_rect(slide, l, t, w, h, backing)
    slide.shapes.add_picture(img_path, Inches(l + inset), Inches(t + inset),
                             Inches(w - 2 * inset), Inches(h - 2 * inset))
    add_rect(slide, l, t, w, h, None, line_color=border_color, line_w=border_w, no_fill=True)


def add_notes(slide, transition, elaboration, bridge):
    text = (f"TRANSITION: {transition}\n\n"
            f"ELABORATION: {elaboration}\n\n"
            f"BRIDGE: {bridge}")
    slide.notes_slide.notes_text_frame.text = text


def blank_slide(prs):
    return prs.slides.add_slide(prs.slide_layouts[6])   # layout 6 == blank
```

### Critical `python-pptx` gotchas

| Gotcha | Fix |
|---|---|
| Shapes inherit a drop shadow | `sp.shadow.inherit = False` on **every** shape |
| Text frames have default margins | Zero all four margins |
| `auto_size` reflows frames unpredictably | Set `MSO_AUTO_SIZE.NONE` |
| `add_shape` creates a text frame with default text | Clear it and zero its margins |
| `Inches(13.333)` ≠ exactly 12192000 EMU | Compare with a tolerance, never `==` |
| `paragraphs[0]` exists on a fresh frame | Use it for the first paragraph; `add_paragraph()` after |
| `p.add_run()` on an empty paragraph | Fine — but `p.text = "x"` first creates a run you can't style individually |
| Table cell text has default margins | Set `cell.margin_left/right/top/bottom` explicitly |
| Table column widths may not stick | Set inside `try/except`; verify in audit |
| `RGBColor` needs ints 0–255 | Never pass floats |
| Fonts not installed silently substitute | Only use cross-platform-safe faces |

---

## 4. Layout Renderers

One function per archetype. Each takes `(prs, spec, theme)` and returns the slide. **Dispatch table**, never a chain of if/else.

```python
RENDERERS = {
    "hero_cover":                 render_hero_cover,
    "asymmetric_editorial_split": render_asymmetric_split,
    "horizontal_timeline_ribbon": render_timeline_ribbon,
    "versus_duel_split":          render_versus_duel,
    "stat_grid_quad":             render_stat_grid,
    "three_pillar_cards":         render_three_pillars,
    "spotlight_quote_manifesto":  render_spotlight_quote,
    "matrix_data_table":          render_matrix_table,
    "key_takeaways_mosaic":       render_takeaways_mosaic,
    "section_header_divider":     render_section_divider,
    "dual_stat_showcase":         render_dual_stat,
    "hero_closing_climax":        render_hero_closing,
}

def build_deck(content_spec, theme_spec, asset_manifest):
    prs = Presentation()
    prs.slide_width  = Inches(SLIDE_W)
    prs.slide_height = Inches(SLIDE_H)
    _set_metadata(prs, content_spec)

    assets = {a["slot_id"]: a["file_path"] for a in asset_manifest["assets"]}

    for sl in content_spec["slides"]:
        layout = sl["layout"]
        if layout not in RENDERERS:
            raise ValueError(f"Slide {sl['slide_number']}: no renderer for layout '{layout}'")
        RENDERERS[layout](prs, sl, theme_spec, assets)

    return prs
```

### Shared chrome (header + footer)

Render identically on every content slide — this is what makes a deck feel designed rather than assembled.

```python
def render_chrome(slide, num, title, kicker, theme, total):
    P = theme["palette"]
    # Left accent stripe — single or dual-entity
    if theme.get("dual_entity_stripe"):
        add_rect(slide, 0, 0, 0.09, SLIDE_H, hex2rgb(P["entity_a"]))
        add_rect(slide, 0.09, 0, 0.09, SLIDE_H, hex2rgb(P["entity_b"]))
    else:
        add_rect(slide, 0, 0, 0.18, SLIDE_H, hex2rgb(P["primary_dark"]))

    if kicker:
        add_text(slide, 0.55, 0.42, 9.00, 0.32, kicker.upper(),
                 size=11, bold=True, color=hex2rgb(P["accent_metal"]), font=BODY_FONT)
        add_text(slide, 0.55, 0.78, 10.50, 0.70, title,
                 size=28, bold=True, color=hex2rgb(P["primary_dark"]), font=TITLE_FONT)
        rule_y = 1.77
    else:
        add_text(slide, 0.55, 0.52, 11.00, 0.80, title,
                 size=30, bold=True, color=hex2rgb(P["primary_dark"]), font=TITLE_FONT)
        rule_y = 1.62

    add_rect(slide, 0.60, rule_y, 2.20, 0.055, hex2rgb(P["accent_metal"]))
    add_rect(slide, 0.60, rule_y + 0.09, 12.10, 0.014, hex2rgb(P["rule_hairline"]))

    # Slide-number badge
    add_rect(slide, 12.30, 0.50, 0.58, 0.58, hex2rgb(P["accent_metal"]), shape_type=MSO_SHAPE.OVAL)
    add_rect(slide, 12.30, 0.50, 0.58, 0.58, None,
             line_color=hex2rgb(P["primary_dark"]), line_w=1.0,
             shape_type=MSO_SHAPE.OVAL, no_fill=True)
    add_text(slide, 12.30, 0.50, 0.58, 0.58, f"{num:02d}", size=13, bold=True,
             color=hex2rgb(P["primary_dark"]), align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)

    # Footer
    add_text(slide, 0.60, 7.12, 7.50, 0.25, theme["footer_text"],
             size=8.5, bold=True, color=hex2rgb(P["text_muted"]))
    add_text(slide, 11.55, 7.08, 1.45, 0.30, f"{num:02d} / {total:02d}",
             size=11, color=hex2rgb(P["text_muted"]), align=PP_ALIGN.RIGHT)
```

### Renderer contract per layout

Each renderer must:
1. Set the background (`canvas` for content slides; image for heroes)
2. Render chrome (content slides only)
3. Place structural shapes **before** text (z-order matters — later shapes sit on top)
4. Place images, then frames/borders over them
5. Place text last
6. Add speaker notes
7. Assert its own bounding boxes

#### 4.1 `render_hero_cover`
```
image full-bleed (0,0,13.333,7.5) → inset border (0.30,0.30,12.733,6.90) @1.5pt metal
→ optional dual badge (0.55,0.50,1.40,0.12) → emblem star (cx 6.666, y 2.30, 0.86²)
→ title (1.20,3.20,10.933,1.10) @56pt bold metal-light, CENTRE, MIDDLE anchor
→ subtitle (1.20,4.38,10.933,0.55) @23pt italic canvas
→ divider rule (5.166,5.20,3.00,0.045) metal
→ tagline (1.20,5.45,10.933,0.50) @16pt bold metal-light
→ sub-tagline (1.20,6.25,10.933,0.40) @12.5pt canvas
→ credit (1.20,6.95,10.933,0.30) @10pt muted-light
NO chrome, NO footer, NO page number.
```

#### 4.2 `render_asymmetric_split`
```
chrome → bullets (0.60,2.10,7.00,4.50) @16.5pt, spacing 1.12, space_after 9.5
→ image label (8.15,1.74,4.40,0.24) @9pt bold metal UPPERCASE
→ framed image (8.15,1.95,4.40,3.10)
→ stat card (8.15,5.25,4.40,1.45)
```
**Stat card internals** (fixed offsets from card top `t`):
```
card body     (l, t, w, h) rounded rect adj=0.05, fill=primary_dark
accent spine  (l, t, 0.055, h) entity_a  +  (l+0.055, t, 0.055, h) entity_b   [dual-entity decks]
              or (l, t, 0.11, h) accent_metal                                  [single-accent decks]
headline      (l+0.28, t+0.15, w-0.58, 0.74) @14pt bold metal_light, title font, spacing 1.05
divider       (l+0.28, t+0.94, w-0.58, 0.014) accent_metal
subtitle      (l+0.28, t+1.00, w-0.58, 0.34) @9.5pt on_dark_text
star badge    (l+w-0.50, t+0.20, 0.28, 0.28) accent_metal STAR_5_POINT
```

#### 4.3 `render_timeline_ribbon`
```
chrome → axis rule (0.60,4.28,12.133,0.06) accent_metal
→ 4 cards, w=2.85 h=1.96, x = 0.60 / 3.69 / 6.78 / 9.87
   alternating y = 2.05 (above axis) / 4.55 (below axis)
   card fill alternates canvas-white / surface_alt; border = entity accent (first two / last two)
   top accent bar (x, y, 2.85, 0.10)
→ date badges anchored on the axis: (x+0.08, 4.10 or 4.40, 1.10, 0.26) rounded adj=0.15, fill primary_dark
   text @9pt bold metal_light, CENTRE/MIDDLE
→ card content: title (x+0.18, y+0.20, 2.50, 0.34) @11.5pt bold primary_dark
               body  (x+0.18, y+0.65, 2.50, 0.85) @9.5pt ink, spacing 1.05
   (for below-axis cards shift title to y+0.34 and body to y+0.78)
```
**Vertical clearance check**: above-axis cards end at `2.05 + 1.96 = 4.01`, axis starts `4.28` → 0.27" gap ✓. Below-axis cards start `4.55`, axis ends `4.34` → 0.21" gap ✓.

#### 4.4 `render_versus_duel`
```
chrome → central VS badge (6.166,3.65,1.00,0.55) rounded adj=0.20, fill accent_metal,
         text "VS" @18pt bold primary_dark CENTRE/MIDDLE
→ for each column (left x=0.60, right x=6.78, w=5.55):
   container   (x, 2.00, w, 4.90) fill white, border entity_accent @1.2pt
   banner      (x, 2.00, w, 0.44) fill entity_accent; text @11pt bold white CENTRE/MIDDLE
   portrait    framed (x+0.16, 2.56, 2.00, 1.85)
   stat panel  (x+2.36, 2.56, 2.98, 1.85) rounded adj=0.05, fill primary_dark
               spine (x+2.36, 2.56, 0.10, 1.85) entity_accent
               big   (x+2.55, 2.72, 2.64, 0.36) @16pt bold entity_accent CENTRE
               rule  (x+2.55, 3.14, 2.64, 0.014) accent_metal
               sub   (x+2.55, 3.20, 2.64, 0.50) @10pt metal_light CENTRE, spacing 1.05
               label (x+2.55, 3.80, 2.64, 0.38) @9.5pt bold entity_accent CENTRE UPPERCASE
   bullets     (x+0.18, 4.62, w-0.36, 2.10) @12.5pt, spacing 1.08, space_after 7
```
**Clearance**: banner ends 2.44, portrait/panel start 2.56 (0.12" ✓). Panel ends 4.41, bullets start 4.62 (0.21" ✓). Bullets end 6.72, container ends 6.90 (0.18" ✓).

#### 4.5 `render_stat_grid`
```
chrome → 4 cards 5.85 × 2.25 at (0.60,2.00) (6.88,2.00) (0.60,4.55) (6.88,4.55)
   card      rounded adj=0.04, fill white, border accent_metal @1.0pt
   top bar   (x, y, 5.85, 0.10) fill primary_dark
   big num   (x+0.28, y+0.22, 1.55, 0.70) @38pt bold primary_dark, TITLE_FONT
   label     (x+2.10, y+0.22, 3.50, 0.65) @14.5pt bold primary_dark
   descriptor(x+2.10, y+1.10, 3.50, 0.70) @11pt muted, spacing 1.06
   star      (x+5.20, y+1.72, 0.32, 0.32) accent_metal STAR_5_POINT
```
**Big-number fit rule**: at 38pt Georgia, `1.55"` holds ~5 characters. `"140"` ✓, `"1,750"` ✓, `"13 Ballon d'Ors"` ✗ — that belongs in the label, not the number.

#### 4.6 `render_three_pillars`
```
chrome → 3 cards 3.80 × 4.80 at x = 0.60 / 4.76 / 8.92, y = 2.05
   card        fill white, border pillar_accent @1.4pt
   top bar     (x, 2.05, 3.80, 0.10) pillar_accent
   number oval (x+0.18, 2.25, 0.50, 0.50) fill primary_dark; numeral @12pt bold metal_light CENTRE/MIDDLE
   title       (x+0.83, 2.25, 2.78, 0.52) @14.5pt bold primary_dark, TITLE_FONT
   stat band   (x+0.18, 2.82, 3.44, 0.68) rounded adj=0.04 fill primary_dark
               spine (x+0.18, 2.82, 0.10, 0.68) pillar_accent
               text  (x+0.34, 2.85, 3.28, 0.62) @11pt bold metal_light CENTRE/MIDDLE
   bullets     (x+0.22, 3.70, 3.36, 2.75) @12pt, spacing 1.08, space_after 6
```

#### 4.7 `render_spotlight_quote`
```
chrome → framed image (0.60, 2.00, 4.80, 4.85)
→ quote glyph (5.70, 2.00, 0.70, 0.55) "\u201C" @52pt bold accent_metal TITLE_FONT
→ quote text  (5.70, 2.60, 7.13, 1.30) @22pt italic primary_dark TITLE_FONT, spacing 1.08
→ citation    (5.70, 3.95, 7.13, 0.52) rounded adj=0.06 fill primary_dark
              text @11pt italic metal_light CENTRE/MIDDLE
→ takeaways   (5.70, 4.65, 7.13, 2.10) bullets @12.5pt spacing 1.08 space_after 6.5
```
**Quote fit rule**: at 22pt Georgia in 7.13", ~44 chars/line. Two lines = 88 chars max. Longer quotes must drop to 18pt or be trimmed by the Content Agent.

#### 4.8 `render_matrix_table`
```
chrome → native table (0.60, 2.05, 8.20, 4.75) with len(rows)+1 rows, 3 cols
   column widths: 3.35 / 2.42 / 2.42  (set inside try/except)
   header row: fill primary_dark, vertical_anchor MIDDLE, margin_top/bottom = 0
               text @11–12pt bold, metal for col 0, metal_light for entity cols, CENTRE
   body rows:  alternating fill white / surface_alt
               margin_left/right = Pt(6), vertical_anchor MIDDLE
               col 0: LEFT, regular, ink; cols 1–2: CENTRE, bold, ink
               size: 12pt, or 10.5pt if len(value) > 20
→ callout panel (9.10, 2.05, 3.633, 4.75) rounded adj=0.03 fill primary_dark
   spine   (9.10, 2.05, 0.11, 4.75) accent_metal
   label   (9.30, 2.25, 3.23, 0.30) @10.5pt bold accent_metal CENTRE
   rule    (9.40, 2.60, 3.03, 0.014) rule_hairline
   figure  (9.30, 2.78, 3.23, 0.60) @15pt bold entity_a CENTRE
   rule    (9.40, 3.45, 3.03, 0.014)
   insight (9.30, 3.60, 3.23, 1.25) rounded sub-panel secondary_dark;
             text (9.30, 3.70, 3.23, 1.10) @10.5pt on_dark_text CENTRE spacing 1.06
   verdict (10.30, 5.70, 1.00, 0.50) @12pt bold accent_metal CENTRE/MIDDLE
```
**Table row-height note**: `python-pptx` sets row heights as *minimums*; PowerPoint expands rows to fit text. Budget `4.75" / (rows+1)` and keep cell text short — or the table will push past the content zone. Verify in the audit.

#### 4.9 `render_takeaways_mosaic`
```
chrome → 2 cards 5.85 × 2.80 at (0.60,2.00) and (6.88,2.00)
   card     rounded adj=0.04, fill white, border entity_accent @1.2pt
   top bar  (x, y, 5.85, 0.10) entity_accent
   oval     (x+0.18, y+0.22, 0.50, 0.50) primary_dark; numeral @14pt bold metal_light
   label    (x+0.83, y+0.22, 4.60, 0.50) @14pt bold entity_accent
   body     (x+0.18, y+0.86, 5.45, 1.75) @11.5pt ink spacing 1.08
→ bottom banner (0.60, 5.05, 12.133, 1.75) rounded adj=0.03 fill primary_dark
   rule    (1.20, 5.28, 10.933, 0.04) accent_metal
   label   (0.60, 5.42, 12.133, 0.40) @13pt bold accent_metal CENTRE
   big     (1.20, 5.82, 10.933, 0.50) @11.5pt bold metal_light CENTRE
   closer  (1.20, 6.28, 10.933, 0.40) @9.5pt on_dark_text CENTRE
```
**Clearance**: cards end at 4.80, banner starts at 5.05 → 0.25" ✓. Banner ends 6.80, footer starts 7.08 → 0.28" ✓.

#### 4.10 `render_hero_closing`
Same geometry as `hero_cover` with:
```
title @56pt at y 3.20 → divider at y 4.35 → pull-quote @24pt italic at y 4.55
→ closing line @18pt bold metal_light at y 5.35 → credit @10pt at y 6.95
```

#### 4.11 `render_section_divider` *(decks ≥ 14 slides only)*
```
full-bleed image + 0.60 overlay → section numeral @120pt metal_light (1.20,2.60,3.00,1.80)
→ section title @40pt bold canvas (4.40,2.90,7.73,1.20) → rule (4.40,4.20,2.00,0.045) metal
→ one-line section premise @16pt italic canvas (4.40,4.45,7.73,0.80)
```

#### 4.12 `render_dual_stat`
```
chrome → 2 panels 5.85 × 3.20 at (0.60,2.05) and (6.88,2.05), fill primary_dark, rounded adj=0.04
   each: entity spine (0.11 wide) · giant figure @64pt bold entity_accent CENTRE at y+0.45 h 1.10
         · label @14pt bold metal_light CENTRE at y+1.65 · sub @10.5pt on_dark_text CENTRE at y+2.10
→ bottom insight bar (0.60, 5.55, 12.133, 1.25) fill surface_alt, border rule_hairline
   text @14pt bold primary_dark CENTRE/MIDDLE — the sentence that reconciles the two numbers
```

---

## 5. Z-Order Discipline

`python-pptx` renders in insertion order — later shapes sit on top. Follow this sequence **every time**:

```
1. background fill / full-bleed image
2. large structural panels (cards, containers, banners)
3. panel accents (top bars, spines, rules inside panels)
4. images
5. image frames / borders (drawn AFTER the picture so the border sits on top)
6. badges and small ornaments
7. text — always last
```

Violating this is why borders disappear behind pictures and text gets hidden behind cards.

---

## 6. Speaker Notes Assembly

```python
def build_notes(sl):
    n = sl["speaker_notes"]
    if isinstance(n, dict):
        parts = []
        if n.get("transition"):  parts.append(f"TRANSITION — {n['transition']}")
        if n.get("elaboration"): parts.append(f"ELABORATION — {n['elaboration']}")
        if n.get("bridge"):      parts.append(f"BRIDGE — {n['bridge']}")
        return "\n\n".join(parts)
    return str(n)
```

The beat labels stay in — presenters find them genuinely useful as scanning anchors in Presenter View.

---

## 7. The Audit Harness

Run after every `save()`. The deck is not delivered until every check passes.

```python
from pptx import Presentation
from pptx.enum.shapes import MSO_SHAPE_TYPE

EMU_PER_INCH = 914400
SLIDE_W_EMU = int(13.333 * EMU_PER_INCH)   # 12191695
SLIDE_H_EMU = int(7.500  * EMU_PER_INCH)   # 6858000
TOL = 3000                                  # EMU tolerance (~0.003")


def _boxes(slide):
    out = []
    for sh in slide.shapes:
        if sh.has_text_frame and sh.text_frame.text.strip():
            out.append((sh.left, sh.top, sh.width, sh.height, sh.text_frame.text[:32]))
    return out


def _overlap(a, b, slack=EMU_PER_INCH // 20):
    """True if two TEXT boxes overlap by more than slack (0.05")."""
    ax, ay, aw, ah, _ = a
    bx, by, bw, bh, _ = b
    if ax + aw <= bx + slack or bx + bw <= ax + slack: return False
    if ay + ah <= by + slack or by + bh <= ay + slack: return False
    return True


def audit_deck(path, expected_slides, min_distinct_layouts=6, layouts=None):
    prs = Presentation(path)
    fails = []

    # --- structural ---
    if len(prs.slides) != expected_slides:
        fails.append(f"slide count {len(prs.slides)} != {expected_slides}")
    if abs(prs.slide_width - SLIDE_W_EMU) > TOL:
        fails.append(f"width {prs.slide_width} != {SLIDE_W_EMU}")
    if abs(prs.slide_height - SLIDE_H_EMU) > TOL:
        fails.append(f"height {prs.slide_height} != {SLIDE_H_EMU}")

    for i, slide in enumerate(prs.slides, 1):
        # --- notes ---
        if not slide.has_notes_slide:
            fails.append(f"slide {i}: missing notes")
        else:
            n = slide.notes_slide.notes_text_frame.text.strip()
            if len(n) < 120:
                fails.append(f"slide {i}: notes too short ({len(n)} chars)")

        # --- geometry ---
        for sh in slide.shapes:
            if sh.left is None: continue
            if sh.left < -TOL or sh.top < -TOL:
                fails.append(f"slide {i}: shape at negative coords ({sh.left},{sh.top})")
            if sh.left + sh.width > SLIDE_W_EMU + TOL:
                fails.append(f"slide {i}: shape overflows right edge")
            if sh.top + sh.height > SLIDE_H_EMU + TOL:
                fails.append(f"slide {i}: shape overflows bottom edge")

        # --- text-box collisions ---
        tbs = _boxes(slide)
        for a in range(len(tbs)):
            for b in range(a + 1, len(tbs)):
                if _overlap(tbs[a], tbs[b]):
                    fails.append(f"slide {i}: TEXT OVERLAP '{tbs[a][4]}' vs '{tbs[b][4]}'")

        # --- minimum font legibility ---
        for sh in slide.shapes:
            if not sh.has_text_frame: continue
            for p in sh.text_frame.paragraphs:
                for r in p.runs:
                    if r.font.size and r.font.size.pt < 8:
                        fails.append(f"slide {i}: font {r.font.size.pt}pt below 8pt floor")

    # --- layout diversity ---
    if layouts:
        distinct = len(set(layouts))
        if distinct < min_distinct_layouts:
            fails.append(f"only {distinct} distinct layouts (< {min_distinct_layouts})")
        for a, b in zip(layouts, layouts[1:]):
            if a == b:
                fails.append(f"consecutive duplicate layout: {a}")

    if fails:
        print("✗ AUDIT FAILED:")
        for f in fails: print(f"   - {f}")
        return False
    print(f"✓ AUDIT PASSED: {path} — {len(prs.slides)} slides, "
          f"{len(set(layouts or []))} distinct layouts, 0 collisions")
    return True
```

### Audit thresholds

| Check | Threshold |
|---|---|
| Slide count | exact match |
| Slide dimensions | ±3000 EMU (~0.003") |
| Shapes outside canvas | 0 |
| Text-box overlaps (> 0.05") | 0 |
| Slides missing notes | 0 |
| Notes shorter than 120 chars | 0 |
| Font sizes below 8pt | 0 |
| Distinct layouts | ≥ 6 in 11 slides |
| Consecutive duplicate layouts | 0 |

### Cross-renderer sanity (optional but recommended)
If LibreOffice is available, convert to PDF and rasterise a couple of slides to visually confirm nothing shifted:
```bash
soffice --headless --convert-to pdf Messi_vs_Ronaldo_Presentation.pptx
```
Then inspect with `pdftoppm -png -r 80`. Font substitution differences between PowerPoint and LibreOffice are expected — judge layout, not typeface.

---

## 8. Build Script Structure (deliverable quality)

The build script ships alongside the deck. Structure it so a human can read and modify it:

```
build_<topic>_ppt.py
├── Module docstring (topic, deck archetype, palette name, layout allocation summary)
├── Imports
├── THEME CONSTANTS  (RGBColor values, font names, SLIDE_W/H, TOTAL, ASSETS dir)
├── PRIMITIVES       (clamp_box, add_rect, add_text, add_multiline, add_bullets,
│                     add_picture_framed, add_notes, est_lines, blank_slide)
├── CHROME           (render_chrome)
├── LAYOUT RENDERERS (one function per archetype, in slide order)
├── SLIDE FUNCTIONS  (one per slide — composes chrome + renderer + content)
├── AUDIT            (audit_deck)
├── main()           (pre-flight → build → save → audit → report)
└── if __name__ == "__main__": main()
```

**Style rules for the script:**
- Constants uppercase at the top; no magic numbers buried in renderers
- Every slide function has a one-line comment naming its layout archetype
- All coordinates as literals matching the blueprint (so they're diffable against the spec)
- `main()` prints a per-slide build log and the final audit verdict
- Exit non-zero if the audit fails

---

## 9. Failure Modes & Fixes

| Symptom | Cause | Fix |
|---|---|---|
| Text spills outside its box | Copy too long for the frame | Shorten copy → drop 1pt (to the floor) → widen frame. In that order. |
| Bullet wraps leaving one word alone | Line break lands badly | Reword to shift a word; never insert manual breaks |
| Border hidden behind image | Z-order: border drawn first | Draw the border **after** `add_picture` |
| Shapes have unwanted shadows | `shadow.inherit` default | `sp.shadow.inherit = False` on every shape |
| Text sits ~0.1" off from expected | Default text-frame margins | Zero all four margins |
| Slide size assertion fails | `Inches(13.333)` rounds to 12191695, not 12192000 | Compare with tolerance, never `==` |
| Table rows push past the slide | Row heights are minimums; text expanded them | Shorten cell text; reduce font; verify in audit |
| Table column widths ignored | Some renderers recalc from content | Set widths in `try/except`; keep cell text short |
| Font renders differently on another machine | Non-standard face specified | Use only Georgia/Arial/Calibri/Trebuchet MS/Segoe UI/Verdana/Palatino Linotype |
| Image appears stretched | Placed with mismatched w/h vs native aspect | Pre-crop the asset to the exact target aspect; never stretch |
| `KeyError` on an asset slot | Manifest slot_id mismatch | Pre-flight assert every referenced slot exists |
| Accented characters render as boxes | Encoding issue in the script | Save the script UTF-8; use `\uXXXX` escapes for safety |
| Deck opens with "repair" prompt in PowerPoint | Malformed XML from an out-of-range adjustment | Wrap `sp.adjustments[0] = adj` in `try/except`; keep `adj` in 0.0–0.5 |

---

## 10. Builder's Pre-Delivery Checklist

**Pre-flight**
- [ ] Every asset path in the manifest exists on disk
- [ ] `layout_allocation` has no consecutive duplicates and ≥ 6 distinct layouts
- [ ] Every slide has a registered renderer
- [ ] Text-fit estimation run; all overflow flagged and resolved with the Content Agent

**Rendering**
- [ ] Slide size exactly 13.333" × 7.500"
- [ ] Blank layout (`slide_layouts[6]`) used for every slide
- [ ] All shape shadows disabled
- [ ] All text-frame margins zeroed and `auto_size = NONE`
- [ ] Z-order respected: panels → accents → images → borders → badges → text
- [ ] Chrome (header/footer/badge) pixel-identical across all content slides
- [ ] Only cross-platform-safe fonts specified
- [ ] All coordinates within clamps; content zone respected (2.00"–6.95" vertical)

**Content**
- [ ] Speaker notes on 100% of slides, ≥ 120 chars, three beats labelled
- [ ] Core properties set: title, author, subject, keywords, comments (incl. image attribution)
- [ ] No placeholder or lorem text anywhere

**Audit**
- [ ] `audit_deck()` returns True
- [ ] 0 text-box overlaps, 0 out-of-canvas shapes, 0 sub-8pt fonts
- [ ] Build script re-run produces an identical deck (determinism)
- [ ] Optional: PDF conversion spot-check on 2–3 slides

**Delivery**
- [ ] `.pptx` saved in the project root with a descriptive filename
- [ ] Build script saved alongside it and runnable standalone
- [ ] Audit verdict printed in the final report
