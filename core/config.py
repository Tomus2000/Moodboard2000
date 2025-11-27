"""Configuration module for environment variables and constants."""
import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables for local development
load_dotenv()

# Helper function to get config from Streamlit secrets or environment variables
def get_config(key: str, default: str = "") -> str:
    """
    Get configuration value from Streamlit secrets (in cloud) or environment variables (local).
    Streamlit Cloud: st.secrets is available
    Local dev: Use os.getenv() with .env file
    """
    # Try Streamlit secrets first (for Streamlit Cloud deployment)
    try:
        import streamlit as st
        if hasattr(st, 'secrets'):
            try:
                # Streamlit secrets can be accessed like a dict
                # Try using .get() method if available (safer)
                if hasattr(st.secrets, 'get'):
                    value = st.secrets.get(key, None)
                    if value and str(value).strip():
                        return str(value).strip()
                # Try direct access
                elif hasattr(st.secrets, '__contains__') and key in st.secrets:
                    value = st.secrets[key]
                    if value and str(value).strip():
                        return str(value).strip()
                # Try attribute access (for nested secrets)
                if hasattr(st.secrets, key):
                    value = getattr(st.secrets, key)
                    if value and str(value).strip():
                        return str(value).strip()
            except (KeyError, AttributeError, TypeError, Exception):
                # Secrets might not be available or accessed differently
                pass
    except (ImportError, AttributeError, RuntimeError):
        # Not in Streamlit context or secrets not available - continue to env vars
        pass
    
    # Fall back to environment variables (local development)
    env_value = os.getenv(key, default)
    return env_value if env_value else default

# App Configuration
APP_TITLE = get_config("APP_TITLE", "Student Moodmeter 🌊")
APP_FOOTER = get_config("APP_FOOTER", "Built with ❤️ using Streamlit")
APP_AUTH_PIN = get_config("APP_AUTH_PIN", "0000")

# OpenAI Configuration
OPENAI_API_KEY = get_config("OPENAI_API_KEY", "")
OPENAI_MODEL = get_config("OPENAI_MODEL", "gpt-4o-mini")

# Database Configuration
DB_URL = get_config("DB_URL", "sqlite:///moodmeter.db")

# Directories
BASE_DIR = Path(__file__).parent.parent
PROMPTS_DIR = BASE_DIR / "prompts"
ASSETS_DIR = BASE_DIR / "assets"

# Mood Score Bands
MOOD_BANDS = {
    "low": (0, 39),
    "medium_low": (40, 59),
    "medium_high": (60, 79),
    "high": (80, 100),
}

# Mood Emoji Mapping
MOOD_EMOJI = {
    "low": "🌧️",
    "medium_low": "😕",
    "medium": "😐",
    "medium_high": "🙂",
    "high": "🌞",
}

# Mood Colors
MOOD_COLORS = {
    "low": "#ef4444",  # red
    "medium_low": "#f59e0b",  # amber
    "medium_high": "#14b8a6",  # teal
    "high": "#10b981",  # green
}

# Emotions list
EMOTIONS = [
    "joy",
    "sad",
    "anger",
    "fear",
    "anticipation",
    "trust",
    "surprise",
    "disgust",
]


