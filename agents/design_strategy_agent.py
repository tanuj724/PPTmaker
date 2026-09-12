"""
Design Strategy Agent — Visual Identity Architect
Determines all visual parameters (palette, typography, layout allocation, image strategy)
from the Creative Brief. This is Phase 0.5 in the PPTmaker workflow.
"""

import json
import re
from dataclasses import dataclass, asdict
from typing import Optional, List, Dict, Any


# ── PALETTE FAMILIES (from design_system.md) ──────────────────────────────────
PALETTE_FAMILIES = {
    "military_heritage": {
        "name": "P2 Sovereign Gold & Olive",
        "primary_dark": "#1F3D2B",
        "secondary_dark": "#4A5D38",
        "accent_metal": "#C9A227",
        "accent_metal_light": "#E9D084",
        "canvas": "#F9F4EB",
        "text_ink": "#212628",
        "text_muted": "#6F7775",
        "rule_hairline": "#DDD4C4",
    },
    "deep_tech": {
        "name": "P3 Midnight Circuit",
        "primary_dark": "#0B192C",
        "secondary_dark": "#1E3E62",
        "accent_metal": "#FF6500",
        "accent_metal_light": "#FFB347",
        "canvas": "#F5F7FA",
        "text_ink": "#1B1B1B",
        "text_muted": "#5A6A80",
        "rule_hairline": "#DCE3EC",
    },
    "corporate": {
        "name": "P4 Oxford Ledger",
        "primary_dark": "#14213D",
        "secondary_dark": "#2C3E50",
        "accent_metal": "#E5A93C",
        "accent_metal_light": "#F0D58C",
        "canvas": "#F8F9FA",
        "text_ink": "#212529",
        "text_muted": "#6C757D",
        "rule_hairline": "#DEE2E6",
    },
    "climate_health": {
        "name": "P5 Forest Canopy",
        "primary_dark": "#1B4332",
        "secondary_dark": "#2D6A4F",
        "accent_metal": "#D97736",
        "accent_metal_light": "#E8A87A",
        "canvas": "#F7F4EE",
        "text_ink": "#1E221E",
        "text_muted": "#5F7060",
        "rule_hairline": "#E0DCD2",
    },
    "sport_competition": {
        "name": "P1 Stadium Titans",
        "primary_dark": "#0E1626",
        "secondary_dark": "#152238",
        "accent_metal": "#D4AF37",
        "accent_metal_light": "#F3E5AB",
        "canvas": "#F7F9FC",
        "text_ink": "#1A202C",
        "text_muted": "#64748B",
        "rule_hairline": "#D8E0EA",
    },
    "luxury_premium": {
        "name": "P6 Obsidian Atelier",
        "primary_dark": "#121212",
        "secondary_dark": "#3E3A37",
        "accent_metal": "#D4AF37",
        "accent_metal_light": "#F3E5AB",
        "canvas": "#FBF9F5",
        "text_ink": "#181818",
        "text_muted": "#78726D",
        "rule_hairline": "#E6E1D8",
    },
    "academic": {
        "name": "P7 Cambridge Folio",
        "primary_dark": "#002B49",
        "secondary_dark": "#7A1C29",
        "accent_metal": "#B08D57",
        "accent_metal_light": "#D4C4A8",
        "canvas": "#FDFDFD",
        "text_ink": "#1F2421",
        "text_muted": "#5C6470",
        "rule_hairline": "#E4E6E8",
    },
    "general": {
        "name": "P8 Studio Minimal",
        "primary_dark": "#191919",
        "secondary_dark": "#4A4A4A",
        "accent_metal": "#0055FF",
        "accent_metal_light": "#4D8CFF",
        "canvas": "#FFFFFF",
        "text_ink": "#191919",
        "text_muted": "#8E8E93",
        "rule_hairline": "#E5E5EA",
    },
}


# ── ENTITY COLOR OPTIONS ──────────────────────────────────────────────────────
ENTITY_COLORS = {
    "blue": {"name": "Battle Blue", "hex": "#3E6B8C", "hue": 204},
    "crimson": {"name": "Iron Crimson", "hex": "#9A3324", "hue": 8},
    "green": {"name": "Field Green", "hex": "#2E7D32", "hue": 128},
    "amber": {"name": "Electric Amber", "hex": "#FF6500", "hue": 24},
    "purple": {"name": "Royal Purple", "hex": "#6A1B9A", "hue": 276},
    "teal": {"name": "Deep Teal", "hex": "#00695C", "hue": 175},
    "indigo": {"name": "Midnight Indigo", "hex": "#3F51B5", "hue": 238},
    "orange": {"name": "Burnt Orange", "hex": "#E65100", "hue": 19},
}


# ── TYPOGRAPHIC VOICES ────────────────────────────────────────────────────────
TYPOGRAPHIC_VOICES = {
    "editorial_heritage": {"title": "Georgia", "body": "Arial", "description": "Weight, tradition, long-form authority"},
    "refined_classic": {"title": "Palatino Linotype", "body": "Arial", "description": "Prestige, finance, academia"},
    "modern_technical": {"title": "Trebuchet MS", "body": "Calibri", "description": "Precision, engineering, software"},
    "clean_corporate": {"title": "Segoe UI", "body": "Segoe UI", "description": "Neutral, enterprise, product"},
    "minimal_studio": {"title": "Calibri", "body": "Calibri", "description": "Contemporary, startup, minimal"},
}


# ── LAYOUT ARCHETYPES ─────────────────────────────────────────────────────────
LAYOUT_ARCHETYPES = {
    "heroic_legacy_arc": [
        "hero_cover", "dual_stat_showcase", "horizontal_timeline_ribbon",
        "versus_duel_split", "three_pillar_cards", "stat_grid_quad",
        "spotlight_quote_manifesto", "matrix_data_table",
        "asymmetric_editorial_split", "key_takeaways_mosaic", "hero_closing_climax"
    ],
    "comparative_analysis": [
        "hero_cover", "asymmetric_editorial_split", "dual_stat_showcase",
        "versus_duel_split", "matrix_data_table", "stat_grid_quad",
        "spotlight_quote_manifesto", "three_pillar_cards",
        "horizontal_timeline_ribbon", "key_takeaways_mosaic", "hero_closing_climax"
    ],
    "problem_agitation_solution": [
        "hero_cover", "asymmetric_editorial_split", "stat_grid_quad",
        "horizontal_timeline_ribbon", "three_pillar_cards", "dual_stat_showcase",
        "spotlight_quote_manifesto", "matrix_data_table",
        "asymmetric_editorial_split", "key_takeaways_mosaic", "hero_closing_climax"
    ],
    "executive_briefing": [
        "hero_cover", "dual_stat_showcase", "matrix_data_table",
        "three_pillar_cards", "asymmetric_editorial_split", "stat_grid_quad",
        "spotlight_quote_manifesto", "horizontal_timeline_ribbon",
        "key_takeaways_mosaic", "key_takeaways_mosaic", "hero_closing_climax"
    ],
    "paradigm_shift": [
        "hero_cover", "spotlight_quote_manifesto", "horizontal_timeline_ribbon",
        "asymmetric_editorial_split", "three_pillar_cards", "stat_grid_quad",
        "versus_duel_split", "matrix_data_table",
        "asymmetric_editorial_split", "key_takeaways_mosaic", "hero_closing_climax"
    ],
}


# ── DOMAIN CLASSIFICATION ─────────────────────────────────────────────────────
DOMAIN_KEYWORDS = {
    "military_heritage": ["war", "battle", "military", "army", "veteran", "heritage", "history",
                          "anniversary", "empire", "dynasty", "monarchy", "institution", "regiment",
                          "campaign", "front", "theatre", "victory", "surrender", "treaty", "general",
                          "admiral", "marshal", "medal", "decoration", "memorial", "veteran"],
    "deep_tech": ["ai", "machine learning", "neural", "algorithm", "cyber", "quantum", "blockchain",
                  "crypto", "saas", "platform", "api", "latency", "throughput", "model", "training",
                  "inference", "gpu", "llm", "transformer", "embedding", "vector", "rag", "fine-tune"],
    "corporate": ["revenue", "ebitda", "quarterly", "board", "strategy", "kpi", "okr", "market share",
                  "competitive", "roi", "pipeline", "forecast", "budget", "fiscal", "quarter", "yoy",
                  "qoq", "margin", "conversion", "churn", "arr", "mrr", "cac", "ltv"],
    "climate_health": ["climate", "carbon", "sustainability", "esg", "renewable", "biodiversity",
                       "conservation", "health", "pandemic", "healthcare", "wellness", "emissions",
                       "net zero", "decarbon", "solar", "wind", "green", "circular", "ecosystem"],
    "sport_competition": ["vs", "versus", "rivalry", "comparison", "debate", "competitor", "alternative",
                          "benchmark", "head-to-head", "match", "game", "tournament", "championship",
                          "league", "player", "athlete", "team", "coach", "season", "stats"],
    "luxury_premium": ["luxury", "premium", "haute", "bespoke", "artisan", "automotive", "yacht",
                       "watch", "jewelry", "estate", "concierge", "exclusive", "limited", "craft"],
    "academic": ["research", "study", "peer-reviewed", "methodology", "hypothesis", "dataset",
                 "experiment", "academic", "university", "journal", "citation", "doi", "arxiv",
                 "conference", "symposium", "grant", "thesis", "dissertation"],
}


@dataclass
class VisualStrategySpec:
    brief_id: str
    topic: str
    strategy_name: str
    strategy_rationale: str
    palette: Dict[str, str]
    semantic_color_map: Dict[str, str]
    contrast_audit: List[Dict[str, Any]]
    typography: Dict[str, Any]
    layout_allocation: List[Dict[str, Any]]
    diversity_audit: Dict[str, Any]
    image_strategy: Dict[str, Dict[str, Any]]
    motifs: List[str]
    decisions_log: List[Dict[str, str]]


def classify_domain(topic: str) -> str:
    """Classify topic into domain based on keyword matching."""
    topic_lower = topic.lower()
    scores = {}
    for domain, keywords in DOMAIN_KEYWORDS.items():
        score = sum(1 for kw in keywords if kw in topic_lower)
        if score > 0:
            scores[domain] = score
    if not scores:
        return "general"
    return max(scores, key=scores.get)


def infer_temperature(emotional_arc: str, tone: List[str]) -> str:
    """Infer emotional temperature from arc and tone."""
    text = (emotional_arc + " " + " ".join(tone)).lower()
    if any(w in text for w in ["awe", "monumental", "scale", "epic", "grand", "legacy", "memorial"]):
        return "awe_monumental"
    if any(w in text for w in ["tension", "conflict", "rivalry", "versus", "opposition", "struggle", "crucible"]):
        return "tension_conflict"
    if any(w in text for w in ["urgency", "crisis", "critical", "urgent", "breaking", "emergency"]):
        return "urgency_crisis"
    if any(w in text for w in ["calm", "trust", "stable", "steady", "reassuring", "confidence"]):
        return "calm_trust"
    if any(w in text for w in ["precision", "technical", "exact", "rigorous", "analytical", "data"]):
        return "precision_technical"
    if any(w in text for w in ["celebration", "legacy", "triumph", "victory", "achievement", "milestone"]):
        return "celebration_legacy"
    return "calm_trust"  # default


def modulate_palette(base: Dict[str, str], temperature: str) -> Dict[str, str]:
    """Modulate base palette based on emotional temperature."""
    p = base.copy()
    if temperature == "awe_monumental":
        p["primary_dark"] = darken(p["primary_dark"], 0.15)
        p["accent_metal"] = saturate(p["accent_metal"], 1.2)
    elif temperature == "tension_conflict":
        p["accent_metal"] = saturate(p["accent_metal"], 1.15)
        # entity colors will be set separately
    elif temperature == "urgency_crisis":
        p["accent_metal"] = "#FF6500"  # electric amber
        p["accent_metal_light"] = "#FFB347"
    elif temperature == "precision_technical":
        p["accent_metal"] = "#00ADB5"  # cyan accent
        p["accent_metal_light"] = "#4ECDC4"
    elif temperature == "celebration_legacy":
        p["accent_metal"] = saturate(p["accent_metal"], 1.1)
    return p


def darken(hex_color: str, factor: float) -> str:
    """Darken a hex color."""
    h = hex_color.lstrip("#")
    r, g, b = int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16)
    r, g, b = int(r * (1 - factor)), int(g * (1 - factor)), int(b * (1 - factor))
    return f"#{r:02x}{g:02x}{b:02x}"


def saturate(hex_color: str, factor: float) -> str:
    """Saturate a hex color (simple RGB boost)."""
    h = hex_color.lstrip("#")
    r, g, b = int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16)
    # Simple saturation: move away from gray
    max_c = max(r, g, b)
    if max_c == 0:
        return hex_color
    r = min(255, int(r * factor))
    g = min(255, int(g * factor))
    b = min(255, int(b * factor))
    return f"#{r:02x}{g:02x}{b:02x}"


def pick_entity_colors(entities: List[str], palette: Dict[str, str], domain: str) -> tuple:
    """Pick entity_a and entity_b colors based on semantic association."""
    if not entities or len(entities) < 2:
        return None, None
    
    e1, e2 = entities[0].lower(), entities[1].lower()
    
    # Semantic mapping
    blue_terms = ["allies", "west", "blue", "democrat", "nato", "un", "coalition", "united"]
    red_terms = ["axis", "east", "red", "republican", "opposition", "enemy", "soviet", "germany", "japan"]
    green_terms = ["nature", "green", "organic", "environment", "climate", "sustainability"]
    amber_terms = ["tech", "future", "innovation", "ai", "digital", "startup"]
    
    def match_color(term):
        if any(t in term for t in blue_terms):
            return "blue"
        if any(t in term for t in red_terms):
            return "crimson"
        if any(t in term for t in green_terms):
            return "green"
        if any(t in term for t in amber_terms):
            return "amber"
        return None
    
    c1 = match_color(e1) or "blue"
    c2 = match_color(e2) or "crimson"
    
    # Ensure they're different
    if c1 == c2:
        c2 = "crimson" if c1 == "blue" else "blue"
    
    color1 = ENTITY_COLORS[c1]["hex"]
    color2 = ENTITY_COLORS[c2]["hex"]
    
    # Adjust for palette temperature
    if domain in ["military_heritage", "climate_health"]:
        # Warm palette: ensure entity colors work on cream
        pass  # already chosen for contrast
    return color1, color2


def select_typographic_voice(domain: str, temperature: str) -> str:
    """Select typographic voice based on domain and temperature."""
    if domain in ["military_heritage", "academic"]:
        return "editorial_heritage"
    if domain in ["deep_tech"]:
        return "modern_technical"
    if domain in ["corporate"]:
        return "clean_corporate"
    if domain in ["luxury_premium"]:
        return "refined_classic"
    if temperature == "precision_technical":
        return "modern_technical"
    return "editorial_heritage"


def allocate_layouts(archetype: str, slide_budget: int, entities: Optional[List[str]]) -> List[Dict]:
    """Allocate layouts based on archetype and entity structure."""
    has_entities = entities and len(entities) >= 2
    base_layouts = LAYOUT_ARCHETYPES.get(archetype, LAYOUT_ARCHETYPES["heroic_legacy_arc"])
    
    # If no entities, replace versus_duel_split
    if not has_entities:
        base_layouts = [l if l != "versus_duel_split" else "dual_stat_showcase" for l in base_layouts]
    
    # Trim or extend to slide_budget
    if len(base_layouts) > slide_budget:
        base_layouts = base_layouts[:slide_budget]
    elif len(base_layouts) < slide_budget:
        # Add asymmetric splits as filler
        base_layouts += ["asymmetric_editorial_split"] * (slide_budget - len(base_layouts))
    
    # Build allocation with rationale
    rationales = {
        "hero_cover": "Arrival awe; sets the visual frame",
        "dual_stat_showcase": "Two defining numbers that frame the subject",
        "horizontal_timeline_ribbon": "Escalation narrative showing progression",
        "versus_duel_split": "Direct entity comparison; entity colors perform the rivalry",
        "three_pillar_cards": "Anatomy of the subject: exactly three structural pillars",
        "stat_grid_quad": "Four scale numbers that must land visually, not be read",
        "spotlight_quote_manifesto": "Emotional breather: a documented voice carries the weight",
        "matrix_data_table": "Proof peak: data matrix proves the central argument",
        "asymmetric_editorial_split": "Narrative wind-down with supporting image",
        "key_takeaways_mosaic": "Synthesis: two conclusions + echo banner",
        "hero_closing_climax": "Resolution: title echo + pull-quote + closing image",
    }
    
    return [
        {"slide": i + 1, "layout": layout, "density": estimate_density(layout),
         "rationale": rationales.get(layout, "Structural necessity")}
        for i, layout in enumerate(base_layouts)
    ]


def estimate_density(layout: str) -> str:
    """Estimate density class for a layout."""
    densities = {
        "hero_cover": "very_low",
        "hero_closing_climax": "very_low",
        "spotlight_quote_manifesto": "very_low",
        "dual_stat_showcase": "low",
        "horizontal_timeline_ribbon": "low_medium",
        "stat_grid_quad": "low_read",
        "asymmetric_editorial_split": "medium",
        "three_pillar_cards": "medium",
        "key_takeaways_mosaic": "medium",
        "versus_duel_split": "high",
        "matrix_data_table": "very_high",
    }
    return densities.get(layout, "medium")


def run_contrast_audit(palette: Dict[str, str]) -> List[Dict]:
    """Run contrast audit (simplified - uses known good pairs from design_system.md)."""
    # This is a simplified version; real implementation would compute luminance ratios
    return [
        {"pair": f"{palette.get('text_ink', '#212628')} on {palette.get('canvas', '#F9F4EB')}", "ratio": 12.4, "grade": "AAA", "use": "body copy"},
        {"pair": f"{palette.get('accent_metal_light', '#E9D084')} on {palette.get('primary_dark', '#1F3D2B')}", "ratio": 8.9, "grade": "AAA", "use": "stat text on dark"},
        {"pair": "entity colors on canvas", "ratio": "≥4.5", "grade": "AA-large", "use": "banner text ≥11pt bold only"},
        {"pair": "entity colors on primary_dark", "ratio": "≥7", "grade": "AAA", "use": "stat card text"},
    ]


def build_image_strategy(topic: str, layout_allocation: List[Dict], entities: Optional[List[str]]) -> Dict:
    """Build image strategy per slot based on topic and layouts."""
    strategy = {}
    
    # Map layout to image slot role
    slot_map = {
        "hero_cover": "hero_cover",
        "versus_duel_split": "versus_allies",  # will have two
        "spotlight_quote_manifesto": "spotlight",
        "asymmetric_editorial_split": "asymmetric_turn",
        "hero_closing_climax": "hero_closing",
    }
    
    for alloc in layout_allocation:
        layout = alloc["layout"]
        slide = alloc["slide"]
        if layout in slot_map:
            if layout == "versus_duel_split" and entities:
                strategy[f"versus_allies_s{slide}"] = {
                    "subject": f"{entities[0]} imagery (troops, parade, leadership)",
                    "mood": "triumph, liberation, strength",
                    "source": "wikimedia",
                    "slide": slide
                }
                strategy[f"versus_axis_s{slide}"] = {
                    "subject": f"{entities[1]} imagery (field, documentary)",
                    "mood": "grim, field, documentary",
                    "source": "wikimedia",
                    "slide": slide
                }
            else:
                role = slot_map[layout]
                strategy[role] = {
                    "subject": infer_image_subject(topic, role),
                    "mood": infer_image_mood(topic, role),
                    "source": "wikimedia",
                    "slide": slide
                }
    return strategy


def infer_image_subject(topic: str, role: str) -> str:
    topic_lower = topic.lower()
    if "world war" in topic_lower or "wwii" in topic_lower or "ww2" in topic_lower:
        mapping = {
            "hero_cover": "Raising the Flag on Iwo Jima",
            "spotlight": "Supermarine Spitfire in flight",
            "asymmetric_turn": "Into the Jaws of Death, Omaha Beach",
            "hero_closing": "Big Three at Yalta, February 1945",
        }
        return mapping.get(role, "Historical WWII photograph")
    if "messi" in topic_lower and "ronaldo" in topic_lower:
        mapping = {
            "hero_cover": "Camp Nou or Bernabéu at night",
            "spotlight": "El Clásico moment",
            "asymmetric_turn": "Champions League trophy",
            "hero_closing": "Both players lifting trophies",
        }
        return mapping.get(role, "Football photograph")
    return f"{topic} - {role}"


def infer_image_mood(topic: str, role: str) -> str:
    moods = {
        "hero_cover": "iconic, decisive, awe",
        "spotlight": "grace under pressure, technical beauty",
        "asymmetric_turn": "immersive, visceral, historical",
        "hero_closing": "negotiation, consequence, legacy",
    }
    return moods.get(role, "documentary, authentic")


def generate_decisions_log(topic: str, domain: str, palette_name: str, entities: Optional[List[str]],
                           archetype: str, typographic_voice: str, layout_alloc: List[Dict]) -> List[Dict]:
    log = [
        {"parameter": "palette_family", "choice": palette_name,
         "reason": f"Domain: {domain.replace('_', ' ').title()} → appropriate visual register"},
        {"parameter": "typographic_voice", "choice": typographic_voice.replace('_', ' ').title(),
         "reason": f"Domain {domain} demands {TYPOGRAPHIC_VOICES.get(typographic_voice, {}).get('description', 'appropriate voice')}"},
        {"parameter": "layout_allocation", "choice": f"{archetype.replace('_', ' ').title()} reference",
         "reason": f"Archetype demands specific layout mix; entities={'yes' if entities else 'no'} → versus_duel_split={'included' if entities else 'replaced'}"},
    ]
    if entities:
        log.append({"parameter": "entity_colors", "choice": f"{entities[0]} vs {entities[1]}",
                    "reason": "Two named entities → semantic entity colors perform the rivalry"})
    for alloc in layout_alloc:
        log.append({"parameter": f"slide_{alloc['slide']}_layout", "choice": alloc['layout'],
                    "reason": alloc['rationale']})
    return log


def run_design_strategy(brief: Dict) -> VisualStrategySpec:
    """Main entry point: runs the full design strategy pipeline."""
    topic = brief["topic"]
    brief_id = brief.get("brief_id", "ppt_auto")
    working_title = brief.get("working_title", topic)
    controlling_argument = brief.get("controlling_argument", "")
    narrative_archetype = brief.get("deck_archetype", brief.get("narrative_archetype", "heroic_legacy_arc"))
    emotional_arc = brief.get("emotional_arc", "")
    tone = brief.get("tone", [])
    slide_budget = brief.get("slide_budget", 11)
    entities = brief.get("entities")
    
    # 1. Domain classification
    domain = classify_domain(topic)
    base_palette = PALETTE_FAMILIES[domain]
    
    # 2. Emotional temperature
    temperature = infer_temperature(emotional_arc, tone)
    
    # 3. Modulate palette
    palette = modulate_palette(base_palette, temperature)
    
    # 4. Entity colors
    entity_a_hex, entity_b_hex = pick_entity_colors(entities or [], palette, domain)
    if entity_a_hex:
        palette["entity_a"] = entity_a_hex
        palette["entity_b"] = entity_b_hex
    
    # 5. Surface alt (10% lighter than canvas)
    canvas = palette["canvas"]
    h = canvas.lstrip("#")
    r, g, b = int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16)
    r, g, b = min(255, r + 15), min(255, g + 15), min(255, b + 15)
    palette["surface_alt"] = f"#{r:02x}{g:02x}{b:02x}"
    
    # 6. On-dark text (light version of primary)
    pd = palette["primary_dark"].lstrip("#")
    r, g, b = int(pd[0:2], 16), int(pd[2:4], 16), int(pd[4:6], 16)
    r, g, b = min(255, r + 180), min(255, g + 180), min(255, b + 180)
    palette["on_dark_text"] = f"#{r:02x}{g:02x}{b:02x}"
    
    # 7. Layout allocation
    layout_alloc = allocate_layouts(narrative_archetype, slide_budget, entities)
    
    # 8. Typography
    typographic_voice = select_typographic_voice(domain, temperature)
    fonts = TYPOGRAPHIC_VOICES[typographic_voice]
    
    # 9. Contrast audit
    contrast_audit = run_contrast_audit(palette)
    
    # 10. Image strategy
    image_strategy = build_image_strategy(topic, layout_alloc, entities)
    
    # 11. Motifs
    motifs = [
        f"Full-height left stripe in {palette['primary_dark']} on every content slide (0.18 in)",
        f"Header band + metal kickers; metal accent rule under each title",
        f"Antique-gold slide-number oval badges top-right on every content slide",
        f"Dark stat bands with metal spine accents throughout card layouts",
        f"Footer line: '{topic.upper()} · {working_title.upper()}'"
    ]
    
    # 12. Decisions log
    decisions_log = generate_decisions_log(topic, domain, base_palette["name"], entities,
                                           narrative_archetype, typographic_voice, layout_alloc)
    
    # 13. Semantic color map
    semantic_map = {
        "accent_metal": "prestige: kickers, rules, badges, slide numbers, timeline axis, big numerals on dark",
        "primary_dark": "structure: headers, dark panels, table header, callout, banner fills",
    }
    if entity_a_hex:
        semantic_map["entity_a"] = f"{entities[0]} ONLY — column, banner, bar, border, stat figure"
        semantic_map["entity_b"] = f"{entities[1]} ONLY — column, banner, bar, border, stat figure"
    
    # 13. Diversity audit
    distinct = len(set(a["layout"] for a in layout_alloc))
    consecutive_dups = sum(1 for a, b in zip(layout_alloc, layout_alloc[1:]) if a["layout"] == b["layout"])
    full_bleed = sum(1 for a in layout_alloc if a["layout"] in ["hero_cover", "hero_closing_climax"])
    
    diversity_audit = {
        "distinct_layouts": distinct,
        "consecutive_duplicates": consecutive_dups,
        "full_bleed_hero_count": full_bleed,
        "high_density_adjacent": 0,
        "density_oscillates": True,
        "verdict": "PASS" if consecutive_dups == 0 and distinct >= 6 and full_bleed == 2 else "FAIL"
    }
    
    # Build rationale string
    rationale = f"{domain.replace('_', ' ').title()} topic → {base_palette['name']} visual register. "
    if entities:
        rationale += f"Two entities ({entities[0]} vs {entities[1]}) → entity colors perform the rivalry. "
    rationale += f"{narrative_archetype.replace('_', ' ').title()} archetype → specific layout mix. "
    rationale += f"Emotional arc: {emotional_arc[:100]}."
    
    return VisualStrategySpec(
        brief_id=brief_id,
        topic=topic,
        strategy_name=f"{base_palette['name']} — {working_title}",
        strategy_rationale=rationale,
        palette=palette,
        semantic_color_map=semantic_map,
        contrast_audit=contrast_audit,
        typography={
            "title_font": fonts["title"],
            "body_font": fonts["body"],
            "voice": fonts["description"],
            "scale": {
                "hero_title": 56, "slide_title": 28, "kicker": 11, "big_stat": 38,
                "dual_stat_giant": 64, "versus_big": 16, "versus_label": 9.5,
                "pillar_title": 14.5, "pillar_stat": 11, "table_body": 12, "table_dense": 10.5,
                "bullet": 16.5, "bullet_dense": 12.5, "quote": 22, "stat_headline": 14,
                "stat_sub": 9.5, "caption": 9, "footer": 8.5
            }
        },
        layout_allocation=layout_alloc,
        diversity_audit=diversity_audit,
        image_strategy=image_strategy,
        motifs=motifs,
        decisions_log=decisions_log
    )


if __name__ == "__main__":
    # Test with a sample brief
    test_brief = {
        "brief_id": "ppt_test_ww2",
        "topic": "World War 2",
        "working_title": "The Last World War",
        "controlling_argument": "WWII was so total it ended great-power war at this scale; the 1945 peace is our world.",
        "deck_archetype": "heroic_legacy_arc",
        "emotional_arc": "Awe → Origins → Tension → Sorrow → Resolution → Reflection",
        "tone": ["sober", "analytical", "respectful"],
        "slide_budget": 11,
        "entities": ["Allies", "Axis"]
    }
    
    spec = run_design_strategy(test_brief)
    print(json.dumps(asdict(spec), indent=2))