"""Configuration module for environment variables and constants."""
import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# App Configuration
APP_TITLE = os.getenv("APP_TITLE", "Student Moodmeter 🌊")
APP_FOOTER = os.getenv("APP_FOOTER", "Built with ❤️ using Streamlit")
APP_AUTH_PIN = os.getenv("APP_AUTH_PIN", "0000")

# OpenAI Configuration
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4o-mini")

# Database Configuration
DB_URL = os.getenv("DB_URL", "sqlite:///moodmeter.db")

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


