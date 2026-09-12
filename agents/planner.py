"""Planner agent: designs the structural outline of a presentation deck."""

import google.generativeai as genai

from config import get_gemini_api_key
from schemas import DeckPlan


SYSTEM_PROMPT = (
    "You are an executive presentation strategist. Your job is to design the "
    "outline of a professional, focused slide deck.\n\n"
    "Rules:\n"
    "- The first slide (slide_number 1) must use the TITLE layout.\n"
    "- Intermediate slides must have concise, actionable intents and use "
    "BULLETS, TWO_COLUMN, or QUOTE layouts.\n"
    "- Every intermediate slide must earn its place: no generic filler slides "
    "such as 'Introduction' or 'Conclusion'.\n"
    "- Keep intents brief and outcome-oriented.\n"
    "- Respond only with valid JSON matching the provided schema."
)


class PlannerAgent:
    """Generates a DeckPlan using Gemini's structured output."""

    def __init__(self, model_name: str = "gemini-2.0-flash") -> None:
        genai.configure(api_key=get_gemini_api_key())
        self.model = genai.GenerativeModel(
            model_name,
            system_instruction=SYSTEM_PROMPT,
        )

    def generate_plan(
        self,
        topic: str,
        target_audience: str = "General",
        slide_count: int = 5,
    ) -> DeckPlan:
        """Produce a structured DeckPlan for the given topic."""
        generation_config = genai.GenerationConfig(
            response_mime_type="application/json",
            response_schema=DeckPlan,
        )

        user_prompt = (
            f"Create a presentation plan for the topic: '{topic}'.\n"
            f"Target audience: {target_audience}.\n"
            f"Total number of slides: {slide_count}."
        )

        response = self.model.generate_content(
            user_prompt,
            generation_config=generation_config,
        )

        return DeckPlan.model_validate_json(response.text)


if __name__ == "__main__":
    planner = PlannerAgent()
    plan = planner.generate_plan(
        topic="The Future of Renewable Energy",
        target_audience="C-level executives",
        slide_count=5,
    )
    print(plan.model_dump_json(indent=2))