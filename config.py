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
def load_api_keys_from_file():
    """Load API keys from api_keys.txt file"""
    api_keys_file = os.path.join(BASE_DIR, "api_keys.txt")

    if not os.path.exists(api_keys_file):
        print(f"⚠️  Warning: {api_keys_file} not found!")
        print("   Please create 'api_keys.txt' with your Google Gemini API keys (one per line)")
        print("   You can copy 'api_keys.example.txt' as a template")
        return []

    try:
        with open(api_keys_file, 'r') as f:
            # Read lines, strip whitespace, ignore empty lines and comments
            keys = [
                line.strip()
                for line in f.readlines()
                if line.strip() and not line.strip().startswith('#')
            ]

        if not keys:
            print("⚠️  Warning: No API keys found in api_keys.txt")
            return []

        print(f"✅ Loaded {len(keys)} API keys from api_keys.txt")
        return keys

    except Exception as e:
        print(f"❌ Error loading API keys: {e}")
        return []

# Load API keys from file
GOOGLE_GEMINI_API_KEYS = load_api_keys_from_file()

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
# Load Telegram bot token from file or use default
def load_telegram_token():
    """Load Telegram bot token from file or return configured token"""
    token_file = os.path.join(BASE_DIR, "telegram_token.txt")

    if os.path.exists(token_file):
        try:
            with open(token_file, 'r') as f:
                token = f.read().strip()
                if token:
                    print(f"✅ Loaded Telegram bot token from telegram_token.txt")
                    return token
        except Exception as e:
            print(f"⚠️  Error loading Telegram token: {e}")

    # Default token (configured)
    return "8308035860:AAG7YCkZq4bNiY3HCp8fPXNJ75FL0H3TOMo"

TELEGRAM_BOT_TOKEN = load_telegram_token()
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
