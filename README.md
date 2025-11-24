# 🎬 Modular Video Generation System

**Generate professional videos with AI voiceover, auto-subtitles, and beautiful composition!**

This repository contains a complete, modular video generation system extracted from the original notebook. Each component can be used independently or combined for full video production.

## ✨ Features

- 🎤 **AI Voiceover** - Google Gemini TTS with 5 voices
- 📝 **Auto Subtitles** - OpenAI Whisper transcription
- 🎬 **Video Composition** - Professional editing with titles, music, effects
- 📐 **Multiple Formats** - 9:16, 4:5, 16:9, 1:1 aspect ratios
- 🎨 **Quality Options** - 1080p or 720p output
- 🔄 **API Rotation** - Automatic key rotation (20 keys)
- 🌍 **Multi-language** - Supports multiple languages and scripts
- ⚡ **Batch Processing** - Generate multiple videos at once
- 📦 **Modular Design** - Use any component independently

## 🚀 Quick Start

```bash
# Install dependencies
pip install -r requirements.txt

# Run interactive mode
python main.py

# Or generate directly
python generate_video.py "Your amazing video script here!"
```

📖 **[Read the Quick Start Guide →](QUICKSTART.md)**

## 📦 Modules

| Module | Purpose | Standalone |
|--------|---------|------------|
| **voiceover_generator.py** | Generate TTS voiceovers | ✅ Yes |
| **subtitle_processor.py** | Create subtitles from audio | ✅ Yes |
| **video_composer.py** | Compose final videos | ✅ Yes |
| **dataset_manager.py** | Manage video/music files | ✅ Yes |
| **generate_video.py** | Complete video generation | ✅ Yes |
| **api_manager.py** | API key rotation | Library |
| **config.py** | Configuration settings | Library |

## 💡 Usage Examples

### Generate Complete Video

```python
from generate_video import generate_complete_video

result = generate_complete_video(
    script_text="Hello! Welcome to my channel.",
    voice_name="Puck",
    title="My First Video",
    aspect_ratio="9:16",
    quality="High Quality"
)

print(f"Video: {result['video_path']}")
```

### Just Voiceover

```python
from voiceover_generator import generate_tts_audio

audio_path, status = generate_tts_audio(
    "Hello world!",
    voice_name="Charon"
)
```

### Just Subtitles

```python
from subtitle_processor import process_voiceover_to_subtitles, split_text_into_lines

words = process_voiceover_to_subtitles("audio.wav")
subtitles = split_text_into_lines(words)
```

### Batch Generation

```bash
python generate_video.py "Script 1 --- Script 2 --- Script 3"
```

## 📚 Documentation

- 📖 **[Quick Start Guide](QUICKSTART.md)** - Get started in 5 minutes
- 📘 **[Full Documentation](README_MODULES.md)** - Complete module reference
- ⚙️ **[Configuration](config.py)** - Customize settings

## 🎤 Available Voices

- Puck (US English)
- Charon (US English)
- Kore (US English)
- Fenrir (US English)
- Aoede (US English)

## 📐 Aspect Ratios

- **9:16** - Vertical (TikTok, Instagram Reels, YouTube Shorts)
- **4:5** - Portrait (Instagram Feed)
- **16:9** - Horizontal (YouTube, TV)
- **1:1** - Square (Instagram, Facebook)

## 🎨 Quality Presets

- **High Quality** - 1080p resolution
- **Standard Quality** - 720p resolution

## 🔧 Configuration

Edit `config.py` to customize:

```python
# Add your API keys
GOOGLE_GEMINI_API_KEYS = [
    "YOUR_API_KEY_1",
    "YOUR_API_KEY_2",
    # Up to 20 keys
]

# Change defaults
DEFAULT_VOICE = "Puck"
DEFAULT_QUALITY = "High Quality"
DEFAULT_ASPECT_RATIO = "9:16"
```

## 📁 Project Structure

```
.
├── config.py                  # Settings and configuration
├── api_manager.py             # API key management
├── voiceover_generator.py     # 🎤 TTS generation
├── subtitle_processor.py      # 📝 Subtitle creation
├── video_composer.py          # 🎬 Video composition
├── dataset_manager.py         # 📁 File management
├── generate_video.py          # 🎯 Complete generation
├── main.py                    # Interactive interface
├── requirements.txt           # Dependencies
├── QUICKSTART.md              # Quick start guide
└── README_MODULES.md          # Full documentation
```

## 🌟 Use Cases

- 🎥 **Content Creation** - TikTok, Reels, Shorts
- 📚 **Educational Videos** - Tutorials, lessons
- 🎬 **Marketing** - Product demos, ads
- 📱 **Social Media** - Engaging posts
- 🎙️ **Podcasts** - Audio to video conversion
- 🌐 **Multi-language** - Global content

## 🔄 Workflow

```
Script Text → Voiceover → Subtitles → Video Composition → Final Video
     ↓           ↓           ↓              ↓               ↓
  Input       TTS API    Whisper      MoviePy          MP4 Output
```

## 💻 Requirements

- Python 3.8+
- moviepy
- pillow
- numpy
- openai-whisper
- google-genai
- requests

## 🎯 Perfect For

- ✅ Kaggle notebooks
- ✅ Local development
- ✅ Cloud environments
- ✅ Automated pipelines
- ✅ Batch processing

## 📄 License

Provided as-is for educational and commercial use.

## 🤝 Contributing

Each module is independent and can be modified separately. Feel free to:
- Add new voices
- Implement new effects
- Add more aspect ratios
- Enhance subtitle formatting
- Optimize performance

## 🆘 Support

- 📖 Check [QUICKSTART.md](QUICKSTART.md) for common issues
- 📘 Read [README_MODULES.md](README_MODULES.md) for detailed docs
- ⚙️ Review [config.py](config.py) for settings

---

**🎬 Start creating amazing videos now!**

```bash
python main.py
```