# 🚀 Quick Start Guide

Get started generating videos in under 5 minutes!

## 📦 Installation

```bash
# Install dependencies
pip install -r requirements.txt
```

## 🎯 Three Ways to Use

### 1. Interactive Mode (Easiest)

```bash
python main.py
```

Follow the prompts to:
1. Enter your script
2. Choose a voice
3. Set video title (optional)
4. Select aspect ratio
5. Choose quality

### 2. Command Line (Fast)

```bash
# Simple usage
python generate_video.py "Your video script here"

# With options
python generate_video.py "Your script" --voice Charon --title "My Video" --aspect 9:16
```

### 3. Python Code (Flexible)

```python
from generate_video import generate_complete_video

result = generate_complete_video(
    script_text="Your amazing script here!",
    voice_name="Puck",
    title="My First Video"
)

print(f"Video created: {result['video_path']}")
```

## 🎤 Generate Voiceover Only

```bash
# Command line
python voiceover_generator.py "Hello world!"

# With specific voice
python voiceover_generator.py Charon "Your text here"
```

```python
# Python
from voiceover_generator import generate_tts_audio

audio_path, status = generate_tts_audio("Hello world!", "Puck")
print(f"Audio saved: {audio_path}")
```

## 📝 Generate Subtitles Only

```bash
# Command line
python subtitle_processor.py voiceover.wav subtitles.srt
```

```python
# Python
from subtitle_processor import process_voiceover_to_subtitles, split_text_into_lines

words = process_voiceover_to_subtitles("voiceover.wav")
subtitles = split_text_into_lines(words)
```

## 🎬 Batch Mode (Multiple Videos)

Separate scripts with `---`:

```bash
python generate_video.py "Video 1 script --- Video 2 script --- Video 3 script"
```

Or in Python:

```python
from generate_video import generate_batch_videos

scripts = [
    "First video script",
    "Second video script",
    "Third video script"
]

results = generate_batch_videos(scripts, voice_name="Charon")
```

## 🎨 Available Options

### Voices
- Puck (default)
- Charon
- Kore
- Fenrir
- Aoede

### Aspect Ratios
- 9:16 - Vertical (TikTok, Reels) [default]
- 4:5 - Portrait (Instagram)
- 16:9 - Horizontal (YouTube)
- 1:1 - Square

### Quality
- High Quality - 1080p [default]
- Standard Quality - 720p

## 📁 Output Location

All generated videos are saved in the `exports/` folder:

```
exports/
├── video_001_20241124_120000.mp4
├── video_002_20241124_120100.mp4
└── ...
```

## 🔧 Configuration

Edit `config.py` to:
- Add your Google Gemini API keys
- Change default voice, quality, aspect ratio
- Modify video encoding settings
- Adjust subtitle timing

## 💡 Examples

### TikTok/Reels Video

```bash
python generate_video.py "Amazing fact!" --voice Puck --aspect 9:16 --quality High
```

### YouTube Video

```bash
python generate_video.py "My tutorial" --voice Charon --aspect 16:9 --title "How To Tutorial"
```

### Instagram Post

```bash
python generate_video.py "Quick tip" --voice Kore --aspect 1:1
```

## 🆘 Troubleshooting

### "No video datasets found"

Solution: Specify video dataset path:

```bash
python generate_video.py "text" --video-dataset /path/to/videos
```

### "API quota exceeded"

Solution: The system automatically rotates through 20 API keys. Add more keys in `config.py`:

```python
GOOGLE_GEMINI_API_KEYS = [
    "YOUR_KEY_1",
    "YOUR_KEY_2",
    # Add up to 20 keys
]
```

### "Module not found"

Solution: Install dependencies:

```bash
pip install -r requirements.txt
```

## 📚 Next Steps

- Read [README_MODULES.md](README_MODULES.md) for detailed documentation
- Explore individual modules for custom workflows
- Check configuration options in `config.py`

## 🎉 That's It!

You're ready to create amazing videos! Start with:

```bash
python main.py
```

---

**Need help?** Check out the full documentation in [README_MODULES.md](README_MODULES.md)
