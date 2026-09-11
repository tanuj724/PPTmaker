"""
PPTmaker - Agentic Presentation Generator

Usage with Opencode:
    opencode --continue "Your presentation topic here"

The framework will automatically:
1. Launch orchestrator agent to plan the presentation
2. Spawn content agent for slide content generation
3. Spawn theme agent for design/theme selection
4. Use builder agent to construct the final .pptx file
"""

import sys
from config import get_gemini_api_key

def main():
    """Entry point for PPTmaker."""
    api_key = get_gemini_api_key()
    
    if not api_key:
        print("Error: GEMINI_API_KEY not found. Please set it in your .env file.")
        sys.exit(1)
    
    # Get topic from command line or use default
    if len(sys.argv) > 1:
        topic = " ".join(sys.argv[1:])
    else:
        topic = input("Enter presentation topic: ")
    
    print(f"\n🎯 PPTmaker initialized for topic: {topic}")
    print("📡 Ready for Opencode agent orchestration...")
    print("\nNext steps (handled by Opencode agents):")
    print("  1. Orchestrator: Plan presentation structure")
    print("  2. Content Agent: Generate slide content")
    print("  3. Theme Agent: Select design theme")
    print("  4. Builder Agent: Create PowerPoint file")

if __name__ == "__main__":
    main()
