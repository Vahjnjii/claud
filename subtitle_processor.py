"""
Subtitle Processing Module
Handles audio transcription and subtitle generation with multi-language support
"""

import os
import re
import urllib.request
from functools import lru_cache
from moviepy.editor import TextClip
import whisper

from config import (
    MAX_CHARS_PER_LINE,
    MAX_DURATION_PER_LINE,
    MIN_GAP_BETWEEN_LINES,
    FONT_URLS,
    FONT_CACHE_DIR
)


# Global whisper model
whisper_model = None


def load_whisper_model(model_size="tiny"):
    """
    Load Whisper model for transcription

    Args:
        model_size (str): Model size (tiny, base, small, medium, large)

    Returns:
        whisper.Model: Loaded model
    """
    global whisper_model
    if whisper_model is None:
        print(f"📥 Loading Whisper model: {model_size}")
        whisper_model = whisper.load_model(model_size)
        print(f"✅ Whisper model loaded")
    return whisper_model


def process_voiceover_to_subtitles(voice_over_path, language=None):
    """
    Transcribe audio file and extract word-level timing information

    Args:
        voice_over_path (str): Path to audio file
        language (str, optional): Language code (e.g., 'en', 'es', 'zh')

    Returns:
        list: List of word dictionaries with 'word', 'start', 'end' keys
    """
    if not os.path.exists(voice_over_path):
        raise FileNotFoundError(f"Audio file not found: {voice_over_path}")

    print(f"🎧 Transcribing audio: {voice_over_path}")

    # Load Whisper model
    model = load_whisper_model()

    # Transcribe with word-level timestamps
    result = model.transcribe(
        voice_over_path,
        word_timestamps=True,
        language=language
    )

    # Extract word-level data
    word_data = []
    for segment in result.get('segments', []):
        for word_info in segment.get('words', []):
            word_data.append({
                'word': word_info['word'].strip(),
                'start': word_info['start'],
                'end': word_info['end']
            })

    print(f"✅ Transcribed {len(word_data)} words")

    return word_data


def split_text_into_lines(data, max_chars=MAX_CHARS_PER_LINE,
                          max_duration=MAX_DURATION_PER_LINE,
                          min_gap=MIN_GAP_BETWEEN_LINES):
    """
    Convert word-level timing data into formatted subtitle lines

    Args:
        data (list): List of word dictionaries with timing info
        max_chars (int): Maximum characters per line
        max_duration (float): Maximum duration per line in seconds
        min_gap (float): Minimum gap between lines in seconds

    Returns:
        list: List of subtitle dictionaries with 'text', 'start', 'end' keys
    """
    if not data:
        return []

    subtitles = []
    current_line = []
    current_start = None
    current_chars = 0

    def is_sentence_end(word):
        """Check if word ends with sentence-ending punctuation"""
        return bool(re.search(r'[.!?。！？।]$', word))

    for i, word_info in enumerate(data):
        word = word_info['word']
        start = word_info['start']
        end = word_info['end']

        # Start new line
        if current_start is None:
            current_start = start

        # Add word to current line
        current_line.append(word)
        current_chars += len(word) + 1  # +1 for space

        # Check if we should end the line
        should_break = False

        # Check character limit
        if current_chars >= max_chars:
            should_break = True

        # Check duration limit
        if end - current_start >= max_duration:
            should_break = True

        # Check sentence ending
        if is_sentence_end(word):
            should_break = True

        # Check minimum gap to next word
        if i + 1 < len(data):
            next_start = data[i + 1]['start']
            if next_start - end >= min_gap:
                should_break = True

        # End of data
        if i == len(data) - 1:
            should_break = True

        # Create subtitle line
        if should_break and current_line:
            subtitle_text = ' '.join(current_line)
            subtitles.append({
                'text': subtitle_text,
                'start': current_start,
                'end': end
            })

            # Reset for next line
            current_line = []
            current_start = None
            current_chars = 0

    return subtitles


def detect_language(text):
    """
    Detect the primary language/script of text

    Args:
        text (str): Text to analyze

    Returns:
        str: Language category (cjk, devanagari, arabic, latin)
    """
    if not text:
        return 'latin'

    # Check for CJK characters (Chinese, Japanese, Korean)
    if re.search(r'[\u4e00-\u9fff\u3040-\u309f\u30a0-\u30ff\uac00-\ud7af]', text):
        return 'cjk'

    # Check for Devanagari (Hindi, Sanskrit, etc.)
    if re.search(r'[\u0900-\u097f]', text):
        return 'devanagari'

    # Check for Arabic
    if re.search(r'[\u0600-\u06ff]', text):
        return 'arabic'

    # Default to Latin
    return 'latin'


def download_font(font_type):
    """
    Download font file if not already cached

    Args:
        font_type (str): Font type (cjk, devanagari, arabic)

    Returns:
        str: Path to font file, or None if download failed
    """
    if font_type not in FONT_URLS:
        return None

    font_url = FONT_URLS[font_type]
    font_filename = os.path.basename(font_url)
    font_path = os.path.join(FONT_CACHE_DIR, font_filename)

    # Check if already downloaded
    if os.path.exists(font_path):
        return font_path

    # Download font
    try:
        print(f"📥 Downloading {font_type} font...")
        urllib.request.urlretrieve(font_url, font_path)
        print(f"✅ Font downloaded: {font_path}")
        return font_path
    except Exception as e:
        print(f"❌ Failed to download font: {e}")
        return None


def get_subtitle_font_path(text, bold=True):
    """
    Get appropriate font path based on text language/script

    Args:
        text (str): Text to display
        bold (bool): Whether to use bold font

    Returns:
        str: Path to font file, or None for default font
    """
    language = detect_language(text)

    # Map language to font
    font_map = {
        'cjk': 'cjk',
        'devanagari': 'devanagari',
        'arabic': 'arabic'
    }

    # Try to get custom font
    if language in font_map:
        font_path = download_font(font_map[language])
        if font_path:
            return font_path

    # Fallback to system fonts
    system_fonts = [
        '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf',
        '/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf',
        '/System/Library/Fonts/Helvetica.ttc',
        'Arial-Bold',
        'Arial'
    ]

    for font in system_fonts:
        if os.path.exists(font):
            return font

    return None  # Use MoviePy default


@lru_cache(maxsize=128)
def get_cached_text_clip(text, font, fontsize, color):
    """
    Create text clip with caching for better performance

    Args:
        text (str): Text to display
        font (str): Font path or name
        fontsize (int): Font size
        color (str): Text color

    Returns:
        TextClip: MoviePy TextClip object
    """
    # Determine font based on text
    actual_font = get_subtitle_font_path(text) if font is None else font

    return TextClip(
        text,
        fontsize=fontsize,
        color=color,
        font=actual_font,
        stroke_color='black',
        stroke_width=2,
        method='caption'
    )


def create_subtitle_clips(subtitles, video_width, video_height, aspect_ratio="9:16"):
    """
    Create MoviePy TextClip objects from subtitle data

    Args:
        subtitles (list): List of subtitle dictionaries
        video_width (int): Video width in pixels
        video_height (int): Video height in pixels
        aspect_ratio (str): Video aspect ratio

    Returns:
        list: List of positioned TextClip objects
    """
    from video_composer import get_subtitle_position, get_subtitle_font_size

    clips = []

    # Get position and font size
    position = get_subtitle_position(aspect_ratio, video_height)
    fontsize = get_subtitle_font_size(aspect_ratio, video_height)

    for subtitle in subtitles:
        text = subtitle['text']
        start = subtitle['start']
        end = subtitle['end']

        # Get appropriate font
        font = get_subtitle_font_path(text)

        # Create text clip
        txt_clip = TextClip(
            text,
            fontsize=fontsize,
            color='white',
            font=font,
            stroke_color='black',
            stroke_width=2,
            method='caption',
            size=(int(video_width * 0.9), None),
            align='center'
        )

        # Set timing and position
        txt_clip = txt_clip.set_start(start).set_end(end)
        txt_clip = txt_clip.set_position(position)

        clips.append(txt_clip)

    return clips


def generate_srt_file(subtitles, output_path):
    """
    Generate SRT subtitle file from subtitle data

    Args:
        subtitles (list): List of subtitle dictionaries
        output_path (str): Path to save SRT file

    Returns:
        str: Path to generated SRT file
    """
    def format_time(seconds):
        """Convert seconds to SRT time format (00:00:00,000)"""
        hours = int(seconds // 3600)
        minutes = int((seconds % 3600) // 60)
        secs = int(seconds % 60)
        millis = int((seconds % 1) * 1000)
        return f"{hours:02d}:{minutes:02d}:{secs:02d},{millis:03d}"

    with open(output_path, 'w', encoding='utf-8') as f:
        for i, subtitle in enumerate(subtitles, 1):
            f.write(f"{i}\n")
            f.write(f"{format_time(subtitle['start'])} --> {format_time(subtitle['end'])}\n")
            f.write(f"{subtitle['text']}\n\n")

    print(f"✅ SRT file generated: {output_path}")
    return output_path


# ============================================================================
# STANDALONE EXECUTION
# ============================================================================
if __name__ == "__main__":
    import sys

    print("=" * 70)
    print("📝 SUBTITLE PROCESSOR")
    print("=" * 70)

    if len(sys.argv) < 2:
        print("\n❌ No audio file provided!")
        print("\n📋 Usage:")
        print("  python subtitle_processor.py <audio_file> [output_srt]")
        print("\nExample:")
        print("  python subtitle_processor.py voiceover.wav subtitles.srt")
        sys.exit(1)

    audio_file = sys.argv[1]
    output_srt = sys.argv[2] if len(sys.argv) > 2 else "subtitles.srt"

    if not os.path.exists(audio_file):
        print(f"\n❌ Audio file not found: {audio_file}")
        sys.exit(1)

    print(f"\n📁 Audio file: {audio_file}")
    print(f"📄 Output SRT: {output_srt}")
    print("\n⏳ Processing...\n")

    try:
        # Transcribe audio
        word_data = process_voiceover_to_subtitles(audio_file)

        # Generate subtitles
        subtitles = split_text_into_lines(word_data)

        print(f"\n📊 Generated {len(subtitles)} subtitle lines")

        # Save SRT file
        generate_srt_file(subtitles, output_srt)

        # Print preview
        print("\n📺 Subtitle preview:")
        print("=" * 70)
        for i, subtitle in enumerate(subtitles[:5], 1):
            print(f"{i}. [{subtitle['start']:.2f}s - {subtitle['end']:.2f}s]")
            print(f"   {subtitle['text']}\n")

        if len(subtitles) > 5:
            print(f"... and {len(subtitles) - 5} more lines")

        print("=" * 70)
        print("\n✅ SUCCESS!")

    except Exception as e:
        print(f"\n❌ FAILED: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
