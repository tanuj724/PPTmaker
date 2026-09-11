import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


def get_gemini_api_key() -> str:
    """
    Safely retrieves the GEMINI_API_KEY from environment variables.
    
    Returns:
        str: The Gemini API key.
        
    Raises:
        ValueError: If GEMINI_API_KEY is not set or empty.
    """
    api_key = os.getenv("GEMINI_API_KEY")
    
    if not api_key:
        raise ValueError(
            "GEMINI_API_KEY not found in environment variables. "
            "Please set it in your .env file."
        )
    
    return api_key


if __name__ == "__main__":
    # Test configuration loading
    try:
        key = get_gemini_api_key()
        print("Configuration loaded successfully!")
        print(f"GEMINI_API_KEY is set: {'*' * len(key)}")
    except ValueError as e:
        print(f"Configuration Error: {e}")
