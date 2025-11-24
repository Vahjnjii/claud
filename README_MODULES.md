# 🎬 Modular Video Generation System

A complete, modular video generation system with AI voiceover, subtitles, and professional composition. Each module can be used independently or combined for complete video production.

## 📦 Project Structure

```
.
├── config.py                  # Configuration and settings
├── api_manager.py             # API key management and rotation
├── voiceover_generator.py     # TTS voiceover generation (MAIN MODULE)
├── subtitle_processor.py      # Subtitle generation and transcription
├── video_composer.py          # Video composition and rendering
├── dataset_manager.py         # Video/music dataset management
├── generate_video.py          # Complete video generation script
├── requirements.txt           # Python dependencies
└── README_MODULES.md          # This file
```

## 🚀 Quick Start

### Installation

```bash
# Install dependencies
pip install -r requirements.txt

# Or install individually
pip install moviepy pillow numpy openai-whisper google-genai requests
```

### Basic Usage

#### 1. Generate Voiceover Only

```bash
# Using command line
python voiceover_generator.py "Hello world! This is a test."

# With specific voice
python voiceover_generator.py Charon "Your text here"

# From Python
from voiceover_generator import generate_tts_audio

audio_path, status = generate_tts_audio("Your text here", "Puck")
if audio_path:
    print(f"Voiceover saved to: {audio_path}")
```

#### 2. Generate Subtitles from Audio

```bash
# Using command line
python subtitle_processor.py voiceover.wav subtitles.srt

# From Python
from subtitle_processor import process_voiceover_to_subtitles, split_text_into_lines

word_data = process_voiceover_to_subtitles("voiceover.wav")
subtitles = split_text_into_lines(word_data)
```

#### 3. Generate Complete Video

```bash
# Simple usage
python generate_video.py "Your video script text here"

# With all options
python generate_video.py "Your script" \
  --voice Charon \
  --title "My Video Title" \
  --aspect 9:16 \
  --quality "High Quality" \
  --video-dataset /path/to/videos \
  --music-dataset /path/to/music

# Batch mode (multiple videos)
python generate_video.py "Script 1 --- Script 2 --- Script 3"
```

## 📚 Module Documentation

### 1. voiceover_generator.py 🎤

**Main voiceover generation module using Google Gemini TTS.**

#### Functions:

- `generate_tts_audio(text, voice_name, output_path, use_rotation)` - Generate voiceover from text
- `generate_voiceover_batch(texts, voice_name, output_dir)` - Batch generation
- `get_audio_duration(audio_path)` - Get audio duration
- `test_voice(voice_name, test_text)` - Test a voice

#### Available Voices:
- Puck (US English)
- Charon (US English)
- Kore (US English)
- Fenrir (US English)
- Aoede (US English)

#### Standalone Usage:

```bash
# Test mode (no arguments)
python voiceover_generator.py

# Generate with default voice
python voiceover_generator.py "Hello world"

# Generate with specific voice
python voiceover_generator.py Charon "Hello from Charon"
```

#### Python API:

```python
from voiceover_generator import generate_tts_audio, AVAILABLE_VOICES

# Generate voiceover
audio_path, status = generate_tts_audio(
    text_input="Hello, this is my voiceover!",
    voice_name="Puck",  # or any from AVAILABLE_VOICES
    output_path="my_voiceover.wav",  # optional
    use_rotation=True  # enable API key rotation
)

if audio_path:
    print(f"Success! Saved to: {audio_path}")
else:
    print(f"Failed: {status}")
```

---

### 2. subtitle_processor.py 📝

**Subtitle generation with multi-language support using OpenAI Whisper.**

#### Functions:

- `process_voiceover_to_subtitles(audio_path, language)` - Transcribe audio to word-level data
- `split_text_into_lines(word_data)` - Format into subtitle lines
- `generate_srt_file(subtitles, output_path)` - Create SRT file
- `detect_language(text)` - Auto-detect text language
- `get_subtitle_font_path(text)` - Get appropriate font for text

#### Standalone Usage:

```bash
# Generate subtitles from audio
python subtitle_processor.py voiceover.wav output.srt
```

#### Python API:

```python
from subtitle_processor import (
    process_voiceover_to_subtitles,
    split_text_into_lines,
    generate_srt_file
)

# Transcribe audio
word_data = process_voiceover_to_subtitles("audio.wav")

# Format into subtitle lines
subtitles = split_text_into_lines(word_data)

# Save as SRT file
generate_srt_file(subtitles, "output.srt")

# Each subtitle has: {'text': '...', 'start': 0.0, 'end': 2.5}
for sub in subtitles:
    print(f"[{sub['start']:.2f}s] {sub['text']}")
```

---

### 3. video_composer.py 🎬

**Video composition and rendering with all effects.**

#### Functions:

- `compose_video(...)` - Compose final video with all elements
- `create_title_overlay(...)` - Create animated title
- `adapt_vertical_to_format(...)` - Adapt videos to aspect ratios
- `calculate_target_dimensions(aspect_ratio, quality)` - Get dimensions

#### Standalone Usage:

```bash
python video_composer.py voiceover.wav background.mp4 subtitles.json output.mp4 "Title" music.mp3
```

#### Python API:

```python
from video_composer import compose_video

result = compose_video(
    voiceover_path="voiceover.wav",
    background_video_path="background.mp4",
    subtitles=subtitles_list,
    output_path="final_video.mp4",
    title_text="My Video",
    music_path="background_music.mp3",
    aspect_ratio="9:16",
    quality="High Quality"
)
```

---

### 4. dataset_manager.py 📁

**Dataset scanning and file selection.**

#### Functions:

- `scan_available_folders(base_path)` - Scan for video/music datasets
- `get_random_video_file(folder_path)` - Get random video
- `get_random_music_file(folder_path)` - Get random music
- `get_video_files(folder_path)` - List all videos
- `get_music_files(folder_path)` - List all music

#### Standalone Usage:

```bash
# Scan datasets
python dataset_manager.py /kaggle/input
```

#### Python API:

```python
from dataset_manager import (
    scan_available_folders,
    get_random_video_file,
    get_random_music_file
)

# Scan for datasets
datasets = scan_available_folders("/kaggle/input")
print(f"Found {len(datasets['videos'])} video datasets")

# Get random files
video = get_random_video_file("/path/to/videos")
music = get_random_music_file("/path/to/music")
```

---

### 5. api_manager.py 🔑

**API key rotation and management.**

#### Functions:

- `load_api_key()` - Load current API key
- `get_next_api_key()` - Rotate to next key
- `get_api_rotation_status()` - Get rotation status
- `should_rotate_key(error_message)` - Check if rotation needed

#### Python API:

```python
from api_manager import load_api_key, get_next_api_key

# Get current key
api_key = load_api_key()

# Rotate on error
if quota_error:
    api_key = get_next_api_key()
```

---

### 6. generate_video.py 🎯

**Complete video generation pipeline.**

#### Command Line:

```bash
# Basic
python generate_video.py "Your script here"

# Full options
python generate_video.py "Your script" \
  --voice Charon \
  --title "Video Title" \
  --aspect 16:9 \
  --quality "High Quality" \
  --video-dataset /path/to/videos \
  --music-dataset /path/to/music \
  --output my_video.mp4

# From file
python generate_video.py --script-file script.txt

# Batch mode
python generate_video.py "Script 1 --- Script 2 --- Script 3"
```

#### Python API:

```python
from generate_video import generate_complete_video, generate_batch_videos

# Single video
result = generate_complete_video(
    script_text="Your script here",
    voice_name="Puck",
    title="My Video",
    video_dataset="/path/to/videos",
    music_dataset="/path/to/music",
    aspect_ratio="9:16",
    quality="High Quality",
    output_filename="my_video.mp4"
)

if result['success']:
    print(f"Video created: {result['video_path']}")
    print(f"Duration: {result['duration']:.2f}s")

# Batch generation
scripts = ["Script 1", "Script 2", "Script 3"]
results = generate_batch_videos(scripts, voice_name="Charon")
```

---

## 🎨 Configuration

Edit `config.py` to customize:

- **Voices**: Available TTS voices
- **Quality Settings**: Video resolution presets
- **Aspect Ratios**: 9:16, 4:5, 16:9, 1:1
- **File Paths**: Output directories
- **API Keys**: Google Gemini API keys
- **Video Settings**: Codecs, bitrates, FPS
- **Subtitle Settings**: Font sizes, timing

### Adding API Keys

```python
# In config.py, add your keys:
GOOGLE_GEMINI_API_KEYS = [
    "AIzaSyYOUR_KEY_HERE_1",
    "AIzaSyYOUR_KEY_HERE_2",
    # Add up to 20 keys for rotation
]
```

## 📊 Complete Workflow Example

```python
#!/usr/bin/env python3
"""Complete video generation example"""

from generate_video import generate_complete_video

# Define your script
script = """
Welcome to my channel!
Today we're going to explore amazing destinations.
Don't forget to like and subscribe!
"""

# Generate video
result = generate_complete_video(
    script_text=script,
    voice_name="Puck",
    title="Amazing Destinations",
    video_dataset="/kaggle/input/nature-videos",
    music_dataset="/kaggle/input/background-music",
    aspect_ratio="9:16",
    quality="High Quality"
)

if result['success']:
    print(f"✅ Success! Video: {result['video_path']}")
    print(f"Duration: {result['duration']:.2f} seconds")
    print(f"Subtitles: {result['subtitle_count']} lines")
else:
    print(f"❌ Failed: {result['message']}")
```

## 🔧 Individual Module Usage

### Just Voiceover:

```python
from voiceover_generator import generate_tts_audio

audio, status = generate_tts_audio("Hello world!", "Puck")
```

### Just Subtitles:

```python
from subtitle_processor import process_voiceover_to_subtitles, split_text_into_lines

words = process_voiceover_to_subtitles("audio.wav")
subs = split_text_into_lines(words)
```

### Just Video Composition:

```python
from video_composer import compose_video

compose_video(
    voiceover_path="voice.wav",
    background_video_path="bg.mp4",
    subtitles=subs,
    output_path="output.mp4"
)
```

## 🌐 Kaggle Integration

All modules work seamlessly in Kaggle notebooks:

```python
# In Kaggle notebook
!pip install -r requirements.txt

# Import modules
from generate_video import generate_complete_video

# Use Kaggle datasets automatically
result = generate_complete_video(
    script_text="Your script",
    voice_name="Puck"
)
# Automatically scans /kaggle/input for datasets
```

## 📝 Output Structure

```
exports/
├── video_001_20241124_120000.mp4  # Final video
├── temp_20241124_120000/          # Working directory
│   ├── voiceover.wav              # Generated audio
│   ├── subtitles.srt              # Subtitle file
│   └── subtitles.json             # Subtitle data
```

## 🎯 Aspect Ratios

- **9:16** - Vertical (TikTok, Instagram Reels, YouTube Shorts)
- **4:5** - Portrait (Instagram Feed)
- **16:9** - Horizontal (YouTube, TV)
- **1:1** - Square (Instagram, Facebook)

## 🎨 Quality Presets

- **High Quality**: 1080p resolution
- **Standard Quality**: 720p resolution

## ⚡ Performance Tips

1. **Use API rotation**: Set `use_rotation=True` to avoid quota limits
2. **Cache fonts**: Fonts are automatically cached after first download
3. **Batch processing**: Use `generate_batch_videos()` for multiple videos
4. **Parallel execution**: Run multiple instances for faster batch processing

## 🐛 Troubleshooting

### No video datasets found
```bash
# Check datasets location
python dataset_manager.py /kaggle/input

# Or specify manually
python generate_video.py "text" --video-dataset /path/to/videos
```

### API quota exceeded
- System automatically rotates through 20 API keys
- Add more keys in `config.py`

### Font not found
- Fonts are auto-downloaded on first use
- Check `font_cache/` directory

## 📄 License

This project is provided as-is for educational and commercial use.

## 🤝 Contributing

Each module is independent. To modify:
1. Edit the specific module file
2. Test standalone: `python module_name.py`
3. Integration test: `python generate_video.py "test"`

## 📞 Support

For issues with specific modules:
- **Voiceover issues**: Check `voiceover_generator.py`
- **Subtitle issues**: Check `subtitle_processor.py`
- **Video composition**: Check `video_composer.py`
- **Dataset scanning**: Check `dataset_manager.py`

---

**Made with ❤️ for creators and developers**
