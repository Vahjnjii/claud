"""
Video Composition Module
Handles video composition, title overlays, and final rendering
"""

import os
import random
from datetime import datetime
from moviepy.editor import (
    VideoFileClip, AudioFileClip, TextClip,
    CompositeVideoClip, CompositeAudioClip, concatenate_videoclips, vfx
)
from PIL import Image, ImageDraw, ImageFilter, ImageFont
import numpy as np

from config import (
    ASPECT_RATIO_DIMENSIONS,
    TITLE_DURATION,
    SLOW_MOTION_FACTOR,
    MUSIC_VOLUME,
    VOICEOVER_VOLUME,
    VIDEO_CODEC,
    AUDIO_CODEC,
    VIDEO_BITRATE,
    AUDIO_BITRATE,
    FPS,
    EXPORTS_FOLDER
)


def calculate_target_dimensions(aspect_ratio, quality):
    """
    Calculate target video dimensions based on aspect ratio and quality

    Args:
        aspect_ratio (str): Aspect ratio (9:16, 4:5, 16:9, 1:1)
        quality (str): Quality level (High Quality, Standard Quality)

    Returns:
        tuple: (width, height) in pixels
    """
    if aspect_ratio in ASPECT_RATIO_DIMENSIONS:
        if quality in ASPECT_RATIO_DIMENSIONS[aspect_ratio]:
            return ASPECT_RATIO_DIMENSIONS[aspect_ratio][quality]

    # Default fallback
    return (1080, 1920)


def get_subtitle_position(aspect_ratio, frame_height):
    """
    Get subtitle position based on aspect ratio

    Args:
        aspect_ratio (str): Video aspect ratio
        frame_height (int): Video height in pixels

    Returns:
        tuple: (x, y) position for subtitle ('center', bottom_offset)
    """
    # Position subtitles at bottom of frame
    bottom_offset = int(frame_height * 0.85)

    return ('center', bottom_offset)


def get_subtitle_font_size(aspect_ratio, frame_height):
    """
    Calculate subtitle font size based on resolution and aspect ratio

    Args:
        aspect_ratio (str): Video aspect ratio
        frame_height (int): Video height in pixels

    Returns:
        int: Font size in pixels
    """
    # Base font size calculation (5% of height)
    base_size = int(frame_height * 0.05)

    # Boost for vertical formats
    if aspect_ratio == "9:16":
        base_size = int(base_size * 1.05)

    return base_size


def ensure_even_dimensions(clip):
    """
    Ensure video clip has even dimensions (required by some codecs)

    Args:
        clip (VideoClip): Input video clip

    Returns:
        VideoClip: Clip with even dimensions
    """
    width, height = clip.size

    # Make dimensions even
    if width % 2 != 0:
        width -= 1
    if height % 2 != 0:
        height -= 1

    if (width, height) != clip.size:
        clip = clip.resize((width, height))

    return clip


def create_title_overlay(title_text, framesize, duration=TITLE_DURATION, aspect_ratio="9:16"):
    """
    Create animated title overlay with 3D effect

    Args:
        title_text (str): Title text to display
        framesize (tuple): (width, height) of video
        duration (float): Duration in seconds
        aspect_ratio (str): Video aspect ratio

    Returns:
        VideoClip: Title overlay clip
    """
    width, height = framesize

    # Calculate font size based on resolution
    font_size = int(height * 0.08)

    # Create text clip
    txt_clip = TextClip(
        title_text,
        fontsize=font_size,
        color='white',
        font='Arial-Bold',
        stroke_color='black',
        stroke_width=3,
        method='caption',
        size=(int(width * 0.8), None),
        align='center'
    )

    # Position at center
    txt_clip = txt_clip.set_position('center')

    # Set duration
    txt_clip = txt_clip.set_duration(duration)

    # Add fade in/out
    txt_clip = txt_clip.fadein(0.5).fadeout(0.5)

    return txt_clip


def get_random_subclip_and_slow(clip, target_duration=None, slow_factor=SLOW_MOTION_FACTOR):
    """
    Extract random subclip and apply slow motion effect

    Args:
        clip (VideoClip): Source video clip
        target_duration (float, optional): Desired duration. If None, uses full clip
        slow_factor (float): Slow motion factor (0.7 = 70% speed)

    Returns:
        VideoClip: Processed video clip
    """
    # Remove audio from background clip
    clip = clip.without_audio()

    # Apply slow motion
    clip = clip.fx(vfx.speedx, slow_factor)

    # Get random subclip if target duration specified
    if target_duration:
        clip_duration = clip.duration

        if clip_duration > target_duration:
            # Random start time
            max_start = clip_duration - target_duration
            start_time = random.uniform(0, max_start)

            clip = clip.subclip(start_time, start_time + target_duration)
        else:
            # Loop if too short
            repeats = int(target_duration / clip_duration) + 1
            clip = concatenate_videoclips([clip] * repeats)
            clip = clip.subclip(0, target_duration)

    return clip


def adapt_vertical_to_format(clip, target_width, target_height, aspect_ratio):
    """
    Adapt background video to target aspect ratio with cropping and zoom

    Args:
        clip (VideoClip): Source video clip
        target_width (int): Target width
        target_height (int): Target height
        aspect_ratio (str): Target aspect ratio

    Returns:
        VideoClip: Adapted video clip
    """
    source_width, source_height = clip.size
    target_aspect = target_width / target_height
    source_aspect = source_width / source_height

    if abs(target_aspect - source_aspect) < 0.01:
        # Aspect ratios match, just resize
        return clip.resize((target_width, target_height))

    # Crop to match target aspect ratio
    if source_aspect > target_aspect:
        # Source is wider, crop width
        new_width = int(source_height * target_aspect)
        x_center = source_width / 2
        x1 = int(x_center - new_width / 2)
        clip = clip.crop(x1=x1, width=new_width)
    else:
        # Source is taller, crop height
        new_height = int(source_width / target_aspect)
        y_center = source_height / 2
        y1 = int(y_center - new_height / 2)
        clip = clip.crop(y1=y1, height=new_height)

    # Resize to target dimensions
    clip = clip.resize((target_width, target_height))

    # Apply subtle zoom for vertical content
    if aspect_ratio in ["9:16", "4:5"]:
        clip = clip.resize(1.05)  # 5% zoom
        # Center crop back to target size
        clip = clip.crop(
            x_center=clip.w / 2,
            y_center=clip.h / 2,
            width=target_width,
            height=target_height
        )

    return clip


def estimate_script_duration(text, words_per_minute=150):
    """
    Estimate video duration from text length

    Args:
        text (str): Script text
        words_per_minute (int): Average speaking rate

    Returns:
        float: Estimated duration in seconds
    """
    word_count = len(text.split())
    duration_minutes = word_count / words_per_minute
    duration_seconds = duration_minutes * 60

    # Add buffer for pauses
    duration_seconds *= 1.2

    return duration_seconds


def compose_video(
    voiceover_path,
    background_video_path,
    subtitles,
    output_path,
    title_text=None,
    music_path=None,
    aspect_ratio="9:16",
    quality="High Quality",
    progress_callback=None
):
    """
    Compose final video with all elements

    Args:
        voiceover_path (str): Path to voiceover audio file
        background_video_path (str): Path to background video
        subtitles (list): List of subtitle dictionaries
        output_path (str): Path for output video
        title_text (str, optional): Title to display at start
        music_path (str, optional): Path to background music
        aspect_ratio (str): Target aspect ratio
        quality (str): Video quality
        progress_callback (callable, optional): Callback for progress updates

    Returns:
        str: Path to generated video file
    """
    print("\n" + "=" * 70)
    print("🎬 COMPOSING VIDEO")
    print("=" * 70)

    # Calculate target dimensions
    target_width, target_height = calculate_target_dimensions(aspect_ratio, quality)
    print(f"📐 Target dimensions: {target_width}x{target_height}")

    # Load voiceover
    print(f"🎤 Loading voiceover: {voiceover_path}")
    voiceover = AudioFileClip(voiceover_path)
    voiceover_duration = voiceover.duration
    print(f"⏱️  Voiceover duration: {voiceover_duration:.2f}s")

    # Load and adapt background video
    print(f"🎬 Loading background video: {background_video_path}")
    background = VideoFileClip(background_video_path)

    # Adapt to target format
    print(f"🔄 Adapting to {aspect_ratio} format...")
    background = adapt_vertical_to_format(
        background,
        target_width,
        target_height,
        aspect_ratio
    )

    # Apply slow motion and get random subclip
    background = get_random_subclip_and_slow(
        background,
        target_duration=voiceover_duration + TITLE_DURATION if title_text else voiceover_duration
    )

    # Ensure even dimensions
    background = ensure_even_dimensions(background)

    print(f"✅ Background video prepared: {background.size}")

    # Create subtitle clips
    print(f"📝 Creating {len(subtitles)} subtitle clips...")
    from subtitle_processor import create_subtitle_clips
    subtitle_clips = create_subtitle_clips(
        subtitles,
        target_width,
        target_height,
        aspect_ratio
    )

    # Adjust subtitle timing if we have a title
    title_offset = TITLE_DURATION if title_text else 0
    if title_offset > 0:
        subtitle_clips = [
            clip.set_start(clip.start + title_offset)
            for clip in subtitle_clips
        ]

    # Create title overlay if provided
    video_clips = [background]
    if title_text:
        print(f"🎨 Creating title overlay: {title_text}")
        title_clip = create_title_overlay(
            title_text,
            (target_width, target_height),
            TITLE_DURATION,
            aspect_ratio
        )
        video_clips.append(title_clip)

    # Add subtitles
    video_clips.extend(subtitle_clips)

    # Composite video
    print("🎭 Compositing video layers...")
    final_video = CompositeVideoClip(video_clips)

    # Prepare audio
    print("🎵 Preparing audio...")
    audio_clips = []

    # Add voiceover (offset by title duration)
    voiceover_with_offset = voiceover.set_start(title_offset)
    audio_clips.append(voiceover_with_offset.volumex(VOICEOVER_VOLUME))

    # Add background music if provided
    if music_path and os.path.exists(music_path):
        print(f"🎶 Adding background music: {music_path}")
        music = AudioFileClip(music_path)

        # Loop music if needed
        if music.duration < final_video.duration:
            repeats = int(final_video.duration / music.duration) + 1
            music = concatenate_videoclips([music] * repeats)

        # Trim to video duration
        music = music.subclip(0, final_video.duration)

        # Lower volume
        music = music.volumex(MUSIC_VOLUME)

        audio_clips.append(music)

    # Composite audio
    if len(audio_clips) > 1:
        final_audio = CompositeAudioClip(audio_clips)
    else:
        final_audio = audio_clips[0]

    final_video = final_video.set_audio(final_audio)

    # Ensure output directory exists
    os.makedirs(os.path.dirname(output_path) if os.path.dirname(output_path) else '.', exist_ok=True)

    # Export video
    print(f"💾 Exporting video: {output_path}")
    print(f"⚙️  Codec: {VIDEO_CODEC}, Bitrate: {VIDEO_BITRATE}")

    final_video.write_videofile(
        output_path,
        codec=VIDEO_CODEC,
        audio_codec=AUDIO_CODEC,
        bitrate=VIDEO_BITRATE,
        audio_bitrate=AUDIO_BITRATE,
        fps=FPS,
        preset='medium',
        threads=4
    )

    # Clean up
    voiceover.close()
    background.close()
    if music_path and os.path.exists(music_path):
        music.close()
    final_video.close()

    print(f"✅ Video exported successfully!")
    print(f"📁 Output: {output_path}")

    return output_path


# ============================================================================
# STANDALONE EXECUTION
# ============================================================================
if __name__ == "__main__":
    import sys

    print("=" * 70)
    print("🎬 VIDEO COMPOSER")
    print("=" * 70)

    if len(sys.argv) < 4:
        print("\n❌ Insufficient arguments!")
        print("\n📋 Usage:")
        print("  python video_composer.py <voiceover> <background_video> <subtitles_json> [output] [title] [music]")
        print("\nExample:")
        print("  python video_composer.py voice.wav bg.mp4 subs.json output.mp4 \"My Video\" music.mp3")
        sys.exit(1)

    voiceover_path = sys.argv[1]
    background_path = sys.argv[2]
    subtitles_json = sys.argv[3]
    output_path = sys.argv[4] if len(sys.argv) > 4 else "output.mp4"
    title_text = sys.argv[5] if len(sys.argv) > 5 else None
    music_path = sys.argv[6] if len(sys.argv) > 6 else None

    # Validate inputs
    if not os.path.exists(voiceover_path):
        print(f"\n❌ Voiceover file not found: {voiceover_path}")
        sys.exit(1)

    if not os.path.exists(background_path):
        print(f"\n❌ Background video not found: {background_path}")
        sys.exit(1)

    if not os.path.exists(subtitles_json):
        print(f"\n❌ Subtitles file not found: {subtitles_json}")
        sys.exit(1)

    # Load subtitles
    import json
    with open(subtitles_json, 'r') as f:
        subtitles = json.load(f)

    print(f"\n📁 Voiceover: {voiceover_path}")
    print(f"🎬 Background: {background_path}")
    print(f"📝 Subtitles: {len(subtitles)} lines")
    if title_text:
        print(f"🎨 Title: {title_text}")
    if music_path:
        print(f"🎵 Music: {music_path}")
    print(f"💾 Output: {output_path}")

    print("\n⏳ Composing video...\n")

    try:
        result = compose_video(
            voiceover_path=voiceover_path,
            background_video_path=background_path,
            subtitles=subtitles,
            output_path=output_path,
            title_text=title_text,
            music_path=music_path
        )

        print("\n✅ SUCCESS!")
        print(f"📁 Video saved: {result}")

    except Exception as e:
        print(f"\n❌ FAILED: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
