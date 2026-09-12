"""Pydantic v2 data models shared across PPTmaker agents."""

from enum import Enum

from pydantic import BaseModel


class SlideLayout(str, Enum):
    TITLE = "title"
    BULLETS = "bullets"
    TWO_COLUMN = "two_column"
    QUOTE = "quote"


class SlidePlan(BaseModel):
    slide_number: int
    title: str
    intent: str
    layout: SlideLayout


class DeckPlan(BaseModel):
    topic: str
    target_audience: str
    total_slides: int
    slides: list[SlidePlan]


class SlideContent(BaseModel):
    slide_number: int
    title: str
    bullet_points: list[str]
    presenter_notes: str | None = None
    layout: SlideLayout


class DeckContent(BaseModel):
    topic: str
    title: str
    author: str
    slides: list[SlideContent]


class ExecutionResult(BaseModel):
    success: bool
    output_path: str | None = None
    error_message: str | None = None
    retry_count: int = 0