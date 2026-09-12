# Creative Slide Layout Catalog & Coordinate Blueprints

> **Purpose**: A comprehensive reference catalog of 12 distinct, mathematically calibrated slide layout templates for 16:9 widescreen presentations (`13.333" × 7.500"`).

---

## Blueprint Index

1. `hero_cover` — Full-Bleed Cinematic Hero Title
2. `versus_duel_split` — Direct 50/50 Comparative Duel Matrix
3. `stat_grid_quad` — 4-Card Prominent Metric Showcase
4. `three_pillar_cards` — 3-Column Thematic Pillar Architecture
5. `horizontal_timeline_ribbon` — 4-Node Sequential Milestone Progression
6. `spotlight_quote_manifesto` — Editorial Focus Quote & Portrait Spotlight
7. `matrix_data_table` — Clean Row-Banded Comparative Data Matrix
8. `asymmetric_editorial_split` — 60/40 Storytelling Narrative + Media Panel
9. `key_takeaways_mosaic` — 2 Major Conclusion Cards + 1 Bottom Ribbon
10. `section_header_divider` — Dramatic Chapter Transition
11. `dual_stat_showcase` — 2 Massive Focal Figures with Context Cards
12. `hero_closing_climax` — Inspiring Cinematic Wrap-up Slide

---

## 1. `hero_cover` (Cinematic Full-Bleed Title)
- **Use Case**: Presentation Title Slide, Major Chapter Kickoff
- **Visual Structure**: Full slide background image with dark overlay blend (`0.45`), double outer border inset (`0.30"` margin), centered gold crest/badge, oversized hero title (`56pt`), italic subtitle (`23pt`), accent divider, and tagline badge.
- **Coordinates**:
  - Image: `left=0.0, top=0.0, width=13.333, height=7.50`
  - Inset Border: `left=0.30, top=0.30, width=12.733, height=6.90`, line=`GOLD (1.5pt)`
  - Badge Emblem: `center_x=6.666, top=2.30, w=0.86, h=0.86`
  - Title: `left=1.20, top=3.20, width=10.933, height=1.10` (56pt Bold Serif)
  - Subtitle: `left=1.20, top=4.38, width=10.933, height=0.55` (23pt Italic)
  - Divider: `left=5.166, top=5.20, width=3.00, height=0.045`
  - Tagline: `left=1.20, top=5.45, width=10.933, height=0.50` (16pt Bold Gold)

---

## 2. `versus_duel_split` (Direct 50/50 Comparative Duel Matrix)
- **Use Case**: Head-to-Head Player/Company/Product Comparison, Tactical DNA
- **Visual Structure**: 2 equal columns with contrasting entity accent colors (e.g. Cyan vs Crimson). Each column features a top header badge, framed picture panel, key metric badge, and 3–4 bullet points.
- **Coordinates**:
  - Header: `top=0.42`, Title: `28pt`, Gold bar: `top=1.77`
  - Column 1 (Left Entity): `left=0.60, top=2.00, width=5.85, height=4.90`
    - Container Card: `fill=WHITE_RGB, border=CYAN (1.2pt)`
    - Header Banner: `left=0.60, top=2.00, width=5.85, height=0.50, fill=CYAN`
    - Image Panel: `left=0.80, top=2.65, width=2.00, height=2.00`
    - Stat Badge: `left=2.95, top=2.65, width=3.30, height=2.00, fill=NAVY`
    - Bullets Box: `left=0.80, top=4.80, width=5.45, height=1.90`
  - Column 2 (Right Entity): `left=6.88, top=2.00, width=5.85, height=4.90`
    - Container Card: `fill=WHITE_RGB, border=CRIMSON (1.2pt)`
    - Header Banner: `left=6.88, top=2.00, width=5.85, height=0.50, fill=CRIMSON`
    - Image Panel: `left=7.08, top=2.65, width=2.00, height=2.00`
    - Stat Badge: `left=9.23, top=2.65, width=3.30, height=2.00, fill=NAVY`
    - Bullets Box: `left=7.08, top=4.80, width=5.45, height=1.90`
  - VS Central Badge: `left=6.166, top=3.40, width=1.00, height=0.55, fill=GOLD`

---

## 3. `stat_grid_quad` (4-Card Prominent Metric Showcase)
- **Use Case**: High-Impact Numerical Results, Milestone Figures, Records
- **Visual Structure**: 4 distinct rounded cards in a $2 \times 2$ grid. Each card features a massive bold metric (32–36pt), title label, short descriptive context, and a corner category icon/accent.
- **Coordinates**:
  - Header: `top=0.42`, Title: `28pt`
  - Card 1 (Top-Left): `left=0.60, top=2.00, width=5.85, height=2.25`
  - Card 2 (Top-Right): `left=6.88, top=2.00, width=5.85, height=2.25`
  - Card 3 (Bottom-Left): `left=0.60, top=4.55, width=5.85, height=2.25`
  - Card 4 (Bottom-Right): `left=6.88, top=4.55, width=5.85, height=2.25`
  - Inside each card:
    - Big Stat Number: `top=card_top + 0.20`, `size=34pt Bold`, `color=GOLD`
    - Stat Title: `top=card_top + 0.85`, `size=15pt Bold`, `color=NAVY`
    - Description: `top=card_top + 1.25`, `size=12pt`, `color=INK`

---

## 4. `three_pillar_cards` (3-Column Thematic Pillar Architecture)
- **Use Case**: 3 Strategic Core Pillars, 3 Dimensions of Greatness, 3 Phases
- **Visual Structure**: 3 tall vertical cards side-by-side. Each has a top color-coded badge, hero title, and 3 concise bullet points.
- **Coordinates**:
  - Header: `top=0.42`, Title: `28pt`
  - Card Width: `3.80"`, Card Height: `4.80"`, Gap: `0.36"`
  - Pillar 1: `left=0.60, top=2.05, width=3.80, height=4.80`
  - Pillar 2: `left=4.76, top=2.05, width=3.80, height=4.80`
  - Pillar 3: `left=8.92, top=2.05, width=3.80, height=4.80`
  - Inside each card:
    - Top Accent Bar: `height=0.10, fill=ACCENT_COLOR`
    - Pillar Number Badge: `w=0.45, h=0.45, fill=NAVY, text="01"`
    - Pillar Title: `size=18pt Bold Georgia`, `color=NAVY`
    - Bullets Frame: `top=card_top + 1.20, width=3.40, height=3.30`

---

## 5. `horizontal_timeline_ribbon` (Sequential Milestone Progression)
- **Use Case**: Chronological Career Path, History, Evolution over Time
- **Visual Structure**: Continuous horizontal connecting ribbon with 4 milestone node cards above and below the line, with bold dates, event titles, and impact summaries.
- **Coordinates**:
  - Header: `top=0.42`, Title: `28pt`
  - Timeline Axis Line: `left=0.60, top=4.30, width=12.133, height=0.06, fill=GOLD`
  - 4 Milestone Cards (`width=2.85, height=2.05`):
    - Node 1 (Top): `left=0.60, top=2.05` (Date badge on axis: `top=4.15`)
    - Node 2 (Bottom): `left=3.69, top=4.55` (Date badge on axis: `top=4.15`)
    - Node 3 (Top): `left=6.78, top=2.05` (Date badge on axis: `top=4.15`)
    - Node 4 (Bottom): `left=9.87, top=4.55` (Date badge on axis: `top=4.15`)

---

## 6. `spotlight_quote_manifesto` (Editorial Focus Quote & Media Frame)
- **Use Case**: Iconic Quotes, Philosophical Verdict, Emotional Turning Point
- **Visual Structure**: Left side features a framed high-impact portrait/scene. Right side features an oversized editorial quotation mark, a 24pt italic statement in Georgia, a citation card, and 2 summary takeaway bullets.
- **Coordinates**:
  - Header: `top=0.42`, Title: `28pt`
  - Left Picture Panel: `left=0.60, top=2.00, width=4.80, height=4.85`
  - Right Quote Container: `left=5.70, top=2.00, width=7.00, height=4.85`
    - Giant Quote Icon: `left=5.70, top=2.05, size=48pt, color=GOLD`
    - Quote Text: `left=5.70, top=2.65, width=7.00, height=1.80, size=22pt Italic Georgia`
    - Citation Ribbon: `left=5.70, top=4.60, width=7.00, height=0.60, fill=NAVY`
    - Context Bullets: `left=5.70, top=5.35, width=7.00, height=1.40`

---

## 7. `matrix_data_table` (Structured Row-Banded Comparison Grid)
- **Use Case**: Comprehensive Statistical Comparison, Head-to-Head Records
- **Visual Structure**: Clean tabular presentation with dark header row, contrasting column titles for Entity A vs Entity B, alternating row background colors for readability, and right-aligned numeric data.
- **Coordinates**:
  - Header: `top=0.42`, Title: `28pt`
  - Table Position: `left=0.60, top=2.05, width=8.20, height=4.75`
    - Rows: 6 rows (Header + 5 metric categories)
    - Columns: Category (3.20"), Messi (2.50"), Ronaldo (2.50")
  - Right Highlight Stat Card: `left=9.10, top=2.05, width=3.633, height=4.75, fill=NAVY`

---

## 8. `asymmetric_editorial_split` (60/40 Storytelling Narrative)
- **Use Case**: Deep Narrative Context, Overview, Complex Topic Explanation
- **Visual Structure**: Left 60% contains 4–5 scannable bullet points with bold lead-ins. Right 40% contains a gold-bordered image panel on top and a high-contrast stat card on the bottom.
- **Coordinates**:
  - Header: `top=0.42`, Title: `28pt`
  - Left Column (Bullets): `left=0.60, top=2.10, width=7.00, height=4.50`
  - Right Picture Panel: `left=8.15, top=1.95, width=4.40, height=3.10`
  - Right Stat Card: `left=8.15, top=5.25, width=4.40, height=1.45`

---

## 9. `key_takeaways_mosaic` (Synthesis & Conclusion Horizon)
- **Use Case**: Final Analytical Takeaways, Future Horizon, Strategy Summary
- **Visual Structure**: 2 top rectangular conclusion cards side-by-side + 1 full-width bottom summary banner with bold key metrics.
- **Coordinates**:
  - Header: `top=0.42`, Title: `28pt`
  - Top Left Card: `left=0.60, top=2.00, width=5.85, height=2.80`
  - Top Right Card: `left=6.88, top=2.00, width=5.85, height=2.80`
  - Bottom Banner: `left=0.60, top=5.05, width=12.133, height=1.75, fill=NAVY`

---

## 10. `hero_closing_climax` (Inspiring Wrap-Up Slide)
- **Use Case**: Final Slide, Q&A Invitation, Lasting Impression
- **Visual Structure**: Full-bleed background with dark overlay, gold inset framing, center star/trophy insignia, 56pt bold climax title, italic takeaway quote, and presenter metadata.
- **Coordinates**:
  - Image: `left=0.0, top=0.0, width=13.333, height=7.50`
  - Inset Border: `left=0.30, top=0.30, width=12.733, height=6.90`, line=`GOLD (1.5pt)`
  - Title: `left=1.20, top=3.20, width=10.933, height=1.10` (56pt Bold Serif)
  - Divider: `left=5.166, top=4.35, width=3.00, height=0.045`
  - Subtitle / Quote: `left=1.20, top=4.55, width=10.933, height=0.55` (24pt Italic)
  - Final Takeaway: `left=1.20, top=5.35, width=10.933, height=0.50` (18pt Bold Gold)
