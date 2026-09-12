"""
PPTmaker - Autonomous Creative Multi-Agent Presentation Studio
Main Entry Point
"""

import argparse
import sys
import json
from typing import Optional

from config import get_gemini_api_key
from agents.planner import PlannerAgent
from agents.design_strategy_agent import run_design_strategy, VisualStrategySpec


def run_pipeline(
    topic: str,
    target_audience: str = "Executive & General Professional",
    slide_count: int = 8,
    output_path: Optional[str] = None,
) -> None:
    print("=" * 60)
    print(" PPTmaker — Autonomous Multi-Agent Presentation Studio")
    print("=" * 60)
    print(f"[*] Topic:           {topic}")
    print(f"[*] Target Audience: {target_audience}")
    print(f"[*] Target Slides:   {slide_count}")
    print("-" * 60)

    # 1. Verification of Configuration
    try:
        get_gemini_api_key()
        print("[+] Environment & API Keys verified.")
    except ValueError as e:
        print(f"[!] Configuration warning: {e}")
        print("[!] Proceeding in offline/dry-run mode.")

    # 2. Phase 0: Design Strategy & Visual Identity Formulation
    print("\n[Phase 0] Synthesizing Design Strategy & Visual System...")
    brief = {
        "brief_id": "brief_auto",
        "topic": topic,
        "target_audience": target_audience,
        "slide_count": slide_count,
        "tone": ["authoritative", "inspiring"],
        "emotional_arc": "tension_and_release",
        "controlling_argument": f"A strategic exploration of {topic}.",
        "deck_archetype": "investigative",
    }
    strategy = run_design_strategy(brief)
    
    print(f"  -> Strategy:    {strategy.strategy_name}")
    print(f"  -> Palette:     {strategy.palette.get('name', 'Custom')}")
    print(f"  -> Typography:  {strategy.typography.get('title_font', 'Georgia')} / {strategy.typography.get('body_font', 'Arial')}")
    distinct_count = strategy.diversity_audit.get('distinct_layouts', len(strategy.layout_allocation))
    print(f"  -> Layouts:     {len(strategy.layout_allocation)} slides allocated across {distinct_count} distinct archetypes")

    # 3. Phase 1: Deck Planning & Outline Generation
    print("\n[Phase 1] Generating Deck Plan via Planner Agent...")
    try:
        planner = PlannerAgent()
        plan = planner.generate_plan(
            topic=topic,
            target_audience=target_audience,
            slide_count=slide_count,
        )
        print(f"[+] Successfully generated Deck Plan with {len(plan.slides)} slides:")
        for slide in plan.slides:
            print(f"    Slide {slide.slide_number:02d} [{slide.layout.value}]: {slide.title}")
    except Exception as e:
        print(f"[-] Planner notice (live LLM call): {e}")

    print("\n" + "=" * 60)
    print(" Presentation Architecture Initialized Successfully.")
    print("=" * 60)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="PPTmaker: Autonomous Creative Presentation Generator"
    )
    parser.add_argument(
        "--topic",
        "-t",
        type=str,
        default="The Future of Artificial Intelligence and Human Agency",
        help="Topic of the presentation",
    )
    parser.add_argument(
        "--audience",
        "-a",
        type=str,
        default="Executive & Professional",
        help="Target audience for the presentation",
    )
    parser.add_argument(
        "--slides",
        "-s",
        type=int,
        default=8,
        help="Number of slides to generate (default: 8)",
    )
    parser.add_argument(
        "--output",
        "-o",
        type=str,
        default=None,
        help="Destination path for generated .pptx output",
    )

    args = parser.parse_args()
    run_pipeline(
        topic=args.topic,
        target_audience=args.audience,
        slide_count=args.slides,
        output_path=args.output,
    )


if __name__ == "__main__":
    main()
