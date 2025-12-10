import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


class Config:
    """Application configuration settings."""
    
    # Base paths
    BASE_DIR = Path(__file__).parent
    MEMORY_DIR = BASE_DIR / "memory"
    EXAMPLES_DIR = BASE_DIR / "examples"
    
    # Google Gemini API
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
    GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-1.5-flash")
    
    # Google Search API
    GOOGLE_SEARCH_API_KEY = os.getenv("GOOGLE_SEARCH_API_KEY", "")
    GOOGLE_SEARCH_ENGINE_ID = os.getenv("GOOGLE_SEARCH_ENGINE_ID", "")
    
    # Application settings
    DEFAULT_LANGUAGE = os.getenv("DEFAULT_LANGUAGE", "tr")
    MAX_SEARCH_RESULTS = int(os.getenv("MAX_SEARCH_RESULTS", "5"))
    
    @classmethod
    def is_gemini_configured(cls) -> bool:
        """Check if Gemini API is configured."""
        return bool(cls.GEMINI_API_KEY)
    
    @classmethod
    def is_search_configured(cls) -> bool:
        """Check if Google Search API is configured."""
        return bool(cls.GOOGLE_SEARCH_API_KEY and cls.GOOGLE_SEARCH_ENGINE_ID)


# Create a singleton instance
config = Config()

