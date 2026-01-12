# 🎬 Video Generation System with Telegram Bot

Complete video generation system with AI voiceover, subtitles, and Telegram bot integration.

## 🚀 Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure API Keys

Create `api_keys.txt` with your Google Gemini API keys (one per line):

```
AIzaSyYourKey1
AIzaSyYourKey2
AIzaSyYourKey3
```

### 3. Start Telegram Bot

```bash
python telegram_bot.py
```

### 4. Use Bot Commands

Open Telegram and send to your bot:

```
/start                           - Show help
/voiceover Your text here        - Generate voiceover
/voiceover A --- B --- C         - Batch voiceovers
/subtitle                        - Reply to audio file
/video Your script               - Generate complete video
/video Script1 --- Script2       - Batch videos
```

## 📦 Files

| File | Purpose |
|------|---------|
| `telegram_bot.py` | Main Telegram bot |
| `workflow_manager.py` | Pipeline control |
| `voiceover_generator.py` | TTS generation |
| `subtitle_processor.py` | Subtitle creation |
| `video_composer.py` | Video composition |
| `generate_video.py` | Complete pipeline |
| `dataset_manager.py` | File management |
| `api_manager.py` | API key rotation |
| `config.py` | Configuration |
| `requirements.txt` | Dependencies |

## 🎯 How It Works

### Standalone Mode
```
/voiceover text  → Audio file sent to Telegram ✅
/subtitle        → SRT file sent to Telegram ✅
```

### Pipeline Mode
```
/video script    → Voiceover → Subtitles → Video → Sent to Telegram ✅
```

### Batch Mode
```
/voiceover A --- B --- C    → 3 audio files sent ✅
/video X --- Y              → 2 videos sent ✅
```

## ⚙️ Configuration

Edit `config.py` to change:

```python
DEFAULT_VOICE = "Puck"              # Puck, Charon, Kore, Fenrir, Aoede
DEFAULT_ASPECT_RATIO = "9:16"       # 9:16, 4:5, 16:9, 1:1
DEFAULT_QUALITY = "High Quality"    # High Quality, Standard Quality
TELEGRAM_BOT_TOKEN = "your_token"   # Your bot token
```

## 🔒 Security

- `api_keys.txt` - Protected by .gitignore (NEVER commit)
- `telegram_token.txt` - Protected by .gitignore (optional)

## 💻 Command Line Usage

```bash
# Voiceover only
python voiceover_generator.py "Your text"

# Complete video
python generate_video.py "Your script"

# With options
python generate_video.py "Script" --voice Charon --aspect 16:9
```

## 🐍 Python Usage

```python
# Generate voiceover
from voiceover_generator import generate_tts_audio
audio_path, status = generate_tts_audio("Hello world!", "Puck")

# Generate complete video
from generate_video import generate_complete_video
result = generate_complete_video(
    script_text="Your script",
    voice_name="Puck",
    aspect_ratio="9:16"
)
```

## 🎤 Available Voices

- Puck (US English)
- Charon (US English)
- Kore (US English)
- Fenrir (US English)
- Aoede (US English)

## 📐 Aspect Ratios

- 9:16 - Vertical (TikTok, Reels, Shorts)
- 4:5 - Portrait (Instagram)
- 16:9 - Horizontal (YouTube)
- 1:1 - Square (Instagram, Facebook)

## 🆘 Troubleshooting

### Bot not responding
```bash
# Check if bot is running
python telegram_bot.py
```

### API quota exceeded
System automatically rotates through your API keys. Add more keys to `api_keys.txt`.

### Module not found
```bash
pip install -r requirements.txt
```

## 📋 Requirements

- Python 3.8+
- moviepy
- pillow
- numpy
- openai-whisper
- google-genai
- requests

## 🎉 Ready!

Start the bot:
```bash
python telegram_bot.py
```

Send `/start` to your bot on Telegram!
