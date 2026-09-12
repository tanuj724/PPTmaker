import os
from typing import Optional
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


def get_unsplash_key() -> Optional[str]:
    """Retrieves the optional UNSPLASH_ACCESS_KEY from environment variables."""
    return os.getenv("UNSPLASH_ACCESS_KEY")


def get_pexels_key() -> Optional[str]:
    """Retrieves the optional PEXELS_API_KEY from environment variables."""
    return os.getenv("PEXELS_API_KEY")


def get_brave_key() -> Optional[str]:
    """Retrieves the optional BRAVE_API_KEY from environment variables."""
    return os.getenv("BRAVE_API_KEY")


if __name__ == "__main__":
    try:
        key = get_gemini_api_key()
        print("Configuration loaded successfully!")
        print(f"GEMINI_API_KEY is set: {'*' * len(key)}")
        if get_unsplash_key():
            print("UNSPLASH_ACCESS_KEY is set.")
        if get_pexels_key():
            print("PEXELS_API_KEY is set.")
    except ValueError as e:
        print(f"Configuration Warning: {e}")
