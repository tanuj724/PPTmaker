"""Pydantic v2 data models shared across PPTmaker agents."""

from enum import Enum
from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field


class SlideLayout(str, Enum):
    # Core Legacy / Basic Layouts
    TITLE = "title"
    BULLETS = "bullets"
    TWO_COLUMN = "two_column"
    QUOTE = "quote"
    
    # 12 Modern Layout Archetypes
    HERO_COVER = "hero_cover"
    VERSUS_DUEL_SPLIT = "versus_duel_split"
    STAT_GRID_QUAD = "stat_grid_quad"
    THREE_PILLAR_CARDS = "three_pillar_cards"
    HORIZONTAL_TIMELINE_RIBBON = "horizontal_timeline_ribbon"
    SPOTLIGHT_QUOTE_MANIFESTO = "spotlight_quote_manifesto"
    MATRIX_DATA_TABLE = "matrix_data_table"
    ASYMMETRIC_EDITORIAL_SPLIT = "asymmetric_editorial_split"
    KEY_TAKEAWAYS_MOSAIC = "key_takeaways_mosaic"
    SECTION_HEADER_DIVIDER = "section_header_divider"
    DUAL_STAT_SHOWCASE = "dual_stat_showcase"
    HERO_CLOSING_CLIMAX = "hero_closing_climax"


class SlidePlan(BaseModel):
    slide_number: int
    title: str
    intent: str
    layout: SlideLayout = SlideLayout.BULLETS


class DeckPlan(BaseModel):
    topic: str
    target_audience: str
    total_slides: int
    slides: List[SlidePlan]


class SlideContent(BaseModel):
    slide_number: int
    title: str
    bullet_points: List[str] = Field(default_factory=list)
    kicker: Optional[str] = None
    presenter_notes: Optional[str] = None
    layout: SlideLayout = SlideLayout.BULLETS
    quote: Optional[str] = None
    quote_author: Optional[str] = None
    stats: Optional[List[Dict[str, Any]]] = None
    pillars: Optional[List[Dict[str, Any]]] = None
    timeline_nodes: Optional[List[Dict[str, Any]]] = None
    table_data: Optional[Dict[str, Any]] = None
    image_slot: Optional[str] = None


class DeckContent(BaseModel):
    topic: str
    title: str
    author: str = "PPTmaker Studio"
    slides: List[SlideContent]


class PaletteDefinition(BaseModel):
    primary_dark: str
    secondary_dark: str
    accent_metal: str
    accent_metal_light: str
    canvas: str
    text_ink: str
    text_muted: str
    rule_hairline: str
    entity_a: Optional[str] = None
    entity_b: Optional[str] = None


class ThemeSpec(BaseModel):
    palette: PaletteDefinition
    title_font: str = "Georgia"
    body_font: str = "Arial"
    style_voice: str = "editorial heritage"


class ExecutionResult(BaseModel):
    success: bool
    output_path: Optional[str] = None
    error_message: Optional[str] = None
    retry_count: int = 0
