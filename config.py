"""
Configuration settings for video generation system
"""

import os

# ============================================================================
# VOICE SETTINGS
# ============================================================================
AVAILABLE_VOICES = {
    "Puck": "Puck (US English)",
    "Charon": "Charon (US English)",
    "Kore": "Kore (US English)",
    "Fenrir": "Fenrir (US English)",
    "Aoede": "Aoede (US English)"
}

DEFAULT_VOICE = "Puck"

# ============================================================================
# VIDEO QUALITY SETTINGS
# ============================================================================
QUALITY_SETTINGS = {
    "High Quality": "High Quality (1080p)",
    "Standard Quality": "Standard Quality (720p)"
}

DEFAULT_QUALITY = "High Quality"

# ============================================================================
# ASPECT RATIO SETTINGS
# ============================================================================
ASPECT_RATIOS = {
    "9:16": "9:16 (Vertical - TikTok/Reels)",
    "4:5": "4:5 (Portrait - Instagram)",
    "16:9": "16:9 (Horizontal - YouTube)",
    "1:1": "1:1 (Square - Instagram)"
}

ASPECT_RATIO_DIMENSIONS = {
    "9:16": {"High Quality": (1080, 1920), "Standard Quality": (720, 1280)},
    "4:5": {"High Quality": (1080, 1350), "Standard Quality": (720, 900)},
    "16:9": {"High Quality": (1920, 1080), "Standard Quality": (1280, 720)},
    "1:1": {"High Quality": (1080, 1080), "Standard Quality": (720, 720)}
}

DEFAULT_ASPECT_RATIO = "9:16"

# ============================================================================
# FILE PATHS
# ============================================================================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
EXPORTS_FOLDER = os.path.join(BASE_DIR, "exports")
STATE_FILE = os.path.join(BASE_DIR, "ui_state.json")
HISTORY_FILE = os.path.join(BASE_DIR, "history.json")
STATUS_FILE = os.path.join(BASE_DIR, "generation_status.json")
BATCH_STATUS_FILE = os.path.join(BASE_DIR, "batch_status.json")
API_KEY_FILE = os.path.join(BASE_DIR, "last_api_key.txt")

# Kaggle input paths
KAGGLE_INPUT_DIR = "/kaggle/input"

# ============================================================================
# GOOGLE GEMINI TTS API KEYS
# ============================================================================
GOOGLE_GEMINI_API_KEYS = [
    "AIzaSyCx8qV1wm4YjQv9vHnhD1x2B3c4E5f6G7h",
    "AIzaSyD9xW2vN5mK6pQ8oR7tY4uI3oP1aS2dF3g",
    "AIzaSyE5mK8pL2nM3oQ9rS6tU7vI4wP2bT3eG4h",
    "AIzaSyF2nL9qM4oP5rT8uW9xJ6kQ3sR5cU7vH8i",
    "AIzaSyG8oM3rN6pQ9sU2vX5yK8lS4tW7dV9xI0j",
    "AIzaSyH4pN9sM8qR3tW6vY9zL2mU5sX8eW0yJ1k",
    "AIzaSyI9qO5tN2rU7vY0zM5nW8sV3uX9fZ1yK2l",
    "AIzaSyJ2rP8uO5sW9vZ3nA8oX1tY6uW0gB3zL4m",
    "AIzaSyK5sQ2vP8uX3wA6oB1pY9uZ4vX1hC5nM6o",
    "AIzaSyL8tR5wQ2vY6xB9pC4qZ3wA7vY2iD8oN7p",
    "AIzaSyM2uS8xR5wZ9yC3qD7rA6xB0wZ3jE2pO8q",
    "AIzaSyN5vT2yS8xA3zD6rE0sB9yC4xA5kF5qP9r",
    "AIzaSyO8wU5zT2yB6AD9sF3tC2zD7yB8lG8rQ0s",
    "AIzaSyP2xV8AU5zC9BE3tG6uD5AC0zC2mH2sR1t",
    "AIzaSyQ5yW2BV8AD3CF6uH9vE8BD4AD5nI5tS2u",
    "AIzaSyR8zX5CW2BE6DG9vI2wF2CE7BE8oJ8uT3v",
    "AIzaSyS2AY8DX5CF9EH3wJ5xG5DF0CF2pK2vU4w",
    "AIzaSyT5BY2EY8DG3FI6xK8yH8EG4DG5qL5wV5x",
    "AIzaSyU8CZ5FZ2EH6GJ9yL2zI2FH7EH8rM8xW6y",
    "AIzaSyV2DA8GA5FI9HK3zM5AJ5GI0FI2sN2yX7z"
]

# TTS Model settings
TTS_MODEL = "gemini-2.5-flash-preview-tts"
AUDIO_SAMPLE_RATE = 24000

# ============================================================================
# SUBTITLE SETTINGS
# ============================================================================
MAX_CHARS_PER_LINE = 60
MAX_DURATION_PER_LINE = 2.5
MIN_GAP_BETWEEN_LINES = 1.5

# Font URLs and paths
FONT_URLS = {
    "cjk": "https://github.com/google/fonts/raw/main/ofl/notosanscjk/NotoSansCJK-Bold.ttc",
    "devanagari": "https://github.com/google/fonts/raw/main/ofl/notosansdevanagari/NotoSansDevanagari-Bold.ttf",
    "arabic": "https://github.com/google/fonts/raw/main/ofl/notosansarabic/NotoSansArabic-Bold.ttf"
}

# Font cache directory
FONT_CACHE_DIR = os.path.join(BASE_DIR, "font_cache")

# ============================================================================
# VIDEO SETTINGS
# ============================================================================
# Title overlay settings
TITLE_DURATION = 4  # seconds
TITLE_FADE_IN = 0.5  # seconds
TITLE_FADE_OUT = 0.5  # seconds

# Background video settings
SLOW_MOTION_FACTOR = 0.7  # 70% speed

# Audio settings
MUSIC_VOLUME = 0.15  # 15% volume for background music
VOICEOVER_VOLUME = 1.0  # 100% volume for voiceover

# Video codec settings
VIDEO_CODEC = "libx264"
AUDIO_CODEC = "aac"
VIDEO_BITRATE = "5000k"
AUDIO_BITRATE = "192k"
FPS = 30

# ============================================================================
# BATCH PROCESSING SETTINGS
# ============================================================================
BATCH_SEPARATOR = "---"
MAX_CONCURRENT_VIDEOS = 12
MAX_RETRIES = 3

# ============================================================================
# TELEGRAM BOT SETTINGS
# ============================================================================
TELEGRAM_BOT_TOKEN = ""  # Set this in environment or here
TELEGRAM_API_URL = "https://api.telegram.org/bot"

# Update interval for progress messages
UI_UPDATE_INTERVAL = 2  # seconds

# ============================================================================
# GENERATION SETTINGS
# ============================================================================
# Cancellation support
GENERATION_CANCELLED = False

# Progress tracking
PROGRESS_MESSAGE_TEMPLATE = """
🎬 **Video Generation Progress**

Status: {status}
Progress: {progress}%
Current Step: {step}

{details}
"""

# ============================================================================
# ERROR MESSAGES
# ============================================================================
ERROR_MESSAGES = {
    "quota": "API quota exceeded. Rotating to next API key...",
    "rate_limit": "Rate limit hit. Rotating to next API key...",
    "auth": "Authentication failed. Rotating to next API key...",
    "network": "Network error. Retrying...",
    "file_not_found": "Required file not found: {file}",
    "invalid_input": "Invalid input: {details}",
    "generation_failed": "Video generation failed: {error}",
    "cancelled": "Generation cancelled by user"
}

# ============================================================================
# ENVIRONMENT SETUP
# ============================================================================
def setup_environment():
    """Setup environment variables and create necessary directories"""
    # Set environment variables for headless operation
    os.environ['XDG_RUNTIME_DIR'] = '/tmp/runtime-root'
    os.environ['PULSE_RUNTIME_PATH'] = '/tmp/pulse'
    os.environ['DISPLAY'] = ':99'
    os.environ['MPLBACKEND'] = 'Agg'

    # Create necessary directories
    os.makedirs(EXPORTS_FOLDER, exist_ok=True)
    os.makedirs(FONT_CACHE_DIR, exist_ok=True)

    # Create runtime directories
    os.makedirs('/tmp/runtime-root', exist_ok=True)
    os.makedirs('/tmp/pulse', exist_ok=True)

# ============================================================================
# HELPER FUNCTIONS
# ============================================================================
def get_export_path(filename):
    """Get full path for export file"""
    return os.path.join(EXPORTS_FOLDER, filename)

def get_font_cache_path(font_name):
    """Get path for cached font file"""
    return os.path.join(FONT_CACHE_DIR, font_name)

# Initialize environment on import
setup_environment()
