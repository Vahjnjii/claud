#!/usr/bin/env python3
"""
Complete Video Generation Script
Generates a complete video with voiceover, subtitles, and background
Can be run standalone or imported as a module
"""

import os
import sys
import json
import argparse
from datetime import datetime

# Import all modules
from voiceover_generator import generate_tts_audio, get_audio_duration
from subtitle_processor import process_voiceover_to_subtitles, split_text_into_lines, generate_srt_file
from video_composer import compose_video, calculate_target_dimensions
from dataset_manager import get_random_video_file, get_random_music_file, get_dataset_by_name
from config import (
    DEFAULT_VOICE,
    DEFAULT_QUALITY,
    DEFAULT_ASPECT_RATIO,
    EXPORTS_FOLDER,
    AVAILABLE_VOICES,
    ASPECT_RATIOS
)


def generate_complete_video(
    script_text,
    voice_name=DEFAULT_VOICE,
    title=None,
    video_dataset=None,
    music_dataset=None,
    aspect_ratio=DEFAULT_ASPECT_RATIO,
    quality=DEFAULT_QUALITY,
    output_filename=None,
    progress_callback=None
):
    """
    Generate a complete video from script text

    Args:
        script_text (str): Text script for voiceover
        voice_name (str): Voice to use for TTS
        title (str, optional): Video title overlay
        video_dataset (str, optional): Path to video dataset folder
        music_dataset (str, optional): Path to music dataset folder
        aspect_ratio (str): Video aspect ratio
        quality (str): Video quality level
        output_filename (str, optional): Custom output filename
        progress_callback (callable, optional): Progress callback function

    Returns:
        dict: Result dictionary with 'success', 'video_path', and 'message' keys
    """
    print("\n" + "=" * 70)
    print("🎬 COMPLETE VIDEO GENERATION")
    print("=" * 70)
    print(f"📝 Script: {script_text[:100]}...")
    print(f"🎤 Voice: {voice_name}")
    print(f"📐 Aspect Ratio: {aspect_ratio}")
    print(f"🎨 Quality: {quality}")
    if title:
        print(f"🎯 Title: {title}")

    try:
        # Create temporary working directory
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        work_dir = os.path.join(EXPORTS_FOLDER, f"temp_{timestamp}")
        os.makedirs(work_dir, exist_ok=True)

        # Step 1: Generate voiceover
        if progress_callback:
            progress_callback("Generating voiceover...", 10)

        print("\n📢 Step 1: Generating voiceover...")
        voiceover_path = os.path.join(work_dir, "voiceover.wav")
        audio_path, status = generate_tts_audio(
            script_text,
            voice_name=voice_name,
            output_path=voiceover_path,
            use_rotation=True
        )

        if not audio_path:
            return {
                'success': False,
                'video_path': None,
                'message': f"Voiceover generation failed: {status}"
            }

        audio_duration = get_audio_duration(audio_path)
        print(f"✅ Voiceover generated: {audio_duration:.2f}s")

        # Step 2: Transcribe and create subtitles
        if progress_callback:
            progress_callback("Creating subtitles...", 30)

        print("\n📝 Step 2: Creating subtitles...")
        word_data = process_voiceover_to_subtitles(audio_path)
        subtitles = split_text_into_lines(word_data)

        # Save subtitles to JSON
        subtitles_json = os.path.join(work_dir, "subtitles.json")
        with open(subtitles_json, 'w') as f:
            json.dump(subtitles, f)

        # Also generate SRT file
        subtitles_srt = os.path.join(work_dir, "subtitles.srt")
        generate_srt_file(subtitles, subtitles_srt)

        print(f"✅ Created {len(subtitles)} subtitle lines")

        # Step 3: Select background video
        if progress_callback:
            progress_callback("Selecting background video...", 50)

        print("\n🎬 Step 3: Selecting background video...")
        background_video = None

        if video_dataset:
            # Use specified dataset
            background_video = get_random_video_file(video_dataset)

        if not background_video:
            # Try to find default video datasets
            from dataset_manager import scan_available_folders
            folders = scan_available_folders()

            if folders['videos']:
                # Use first available video dataset
                video_folder = folders['videos'][0]['path']
                background_video = get_random_video_file(video_folder)

        if not background_video:
            return {
                'success': False,
                'video_path': None,
                'message': "No background video available. Please provide video_dataset path."
            }

        print(f"✅ Background video: {os.path.basename(background_video)}")

        # Step 4: Select background music
        if progress_callback:
            progress_callback("Selecting background music...", 60)

        print("\n🎵 Step 4: Selecting background music...")
        background_music = None

        if music_dataset:
            background_music = get_random_music_file(music_dataset)

        if not background_music:
            # Try to find default music datasets
            from dataset_manager import scan_available_folders
            folders = scan_available_folders()

            if folders['music']:
                music_folder = folders['music'][0]['path']
                background_music = get_random_music_file(music_folder)

        if background_music:
            print(f"✅ Background music: {os.path.basename(background_music)}")
        else:
            print("⚠️ No background music found (video will have voiceover only)")

        # Step 5: Compose final video
        if progress_callback:
            progress_callback("Composing final video...", 70)

        print("\n🎭 Step 5: Composing final video...")

        # Determine output filename
        if not output_filename:
            output_filename = f"video_{timestamp}.mp4"

        output_path = os.path.join(EXPORTS_FOLDER, output_filename)

        # Compose video
        final_video = compose_video(
            voiceover_path=audio_path,
            background_video_path=background_video,
            subtitles=subtitles,
            output_path=output_path,
            title_text=title,
            music_path=background_music,
            aspect_ratio=aspect_ratio,
            quality=quality,
            progress_callback=progress_callback
        )

        if progress_callback:
            progress_callback("Video generation complete!", 100)

        print("\n" + "=" * 70)
        print("✅ VIDEO GENERATION COMPLETE!")
        print("=" * 70)
        print(f"📁 Output: {final_video}")
        print(f"⏱️  Duration: {audio_duration:.2f}s")
        print(f"📝 Subtitles: {len(subtitles)} lines")
        print("=" * 70)

        return {
            'success': True,
            'video_path': final_video,
            'message': 'Video generated successfully',
            'duration': audio_duration,
            'subtitle_count': len(subtitles),
            'voiceover_path': audio_path,
            'subtitles_path': subtitles_srt
        }

    except Exception as e:
        import traceback
        error_trace = traceback.format_exc()
        error_msg = f"Video generation failed: {str(e)}"
        print(f"\n❌ {error_msg}")
        print(error_trace)

        return {
            'success': False,
            'video_path': None,
            'message': error_msg,
            'error': str(e)
        }


def generate_batch_videos(scripts, **kwargs):
    """
    Generate multiple videos from a list of scripts

    Args:
        scripts (list): List of script texts
        **kwargs: Additional arguments passed to generate_complete_video

    Returns:
        list: List of result dictionaries for each video
    """
    results = []

    print("\n" + "=" * 70)
    print(f"🎬 BATCH VIDEO GENERATION ({len(scripts)} videos)")
    print("=" * 70)

    for i, script in enumerate(scripts, 1):
        print(f"\n{'='*70}")
        print(f"📹 Generating video {i}/{len(scripts)}")
        print(f"{'='*70}")

        # Add index to filename
        if 'output_filename' not in kwargs:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            kwargs['output_filename'] = f"video_{i:03d}_{timestamp}.mp4"

        result = generate_complete_video(script, **kwargs)
        results.append(result)

        if result['success']:
            print(f"✅ Video {i} completed: {result['video_path']}")
        else:
            print(f"❌ Video {i} failed: {result['message']}")

    # Summary
    successful = sum(1 for r in results if r['success'])
    print("\n" + "=" * 70)
    print("📊 BATCH GENERATION SUMMARY")
    print("=" * 70)
    print(f"✅ Successful: {successful}/{len(scripts)}")
    print(f"❌ Failed: {len(scripts) - successful}/{len(scripts)}")
    print("=" * 70)

    return results


# ============================================================================
# COMMAND LINE INTERFACE
# ============================================================================
def main():
    parser = argparse.ArgumentParser(
        description='Generate complete videos with voiceover and subtitles',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Generate video from script text
  python generate_video.py "Hello world! This is my video."

  # With custom voice and title
  python generate_video.py "My script" --voice Charon --title "My Video"

  # With specific datasets
  python generate_video.py "My script" --video-dataset /path/to/videos --music-dataset /path/to/music

  # Custom aspect ratio and quality
  python generate_video.py "My script" --aspect 16:9 --quality Standard

  # Batch mode with separator
  python generate_video.py "Script 1 --- Script 2 --- Script 3"
        """
    )

    parser.add_argument('script', help='Script text or file path (use --- to separate multiple scripts)')
    parser.add_argument('--voice', default=DEFAULT_VOICE, choices=list(AVAILABLE_VOICES.keys()),
                        help=f'Voice to use (default: {DEFAULT_VOICE})')
    parser.add_argument('--title', help='Video title overlay')
    parser.add_argument('--video-dataset', help='Path to video dataset folder')
    parser.add_argument('--music-dataset', help='Path to music dataset folder')
    parser.add_argument('--aspect', default=DEFAULT_ASPECT_RATIO, choices=list(ASPECT_RATIOS.keys()),
                        help=f'Aspect ratio (default: {DEFAULT_ASPECT_RATIO})')
    parser.add_argument('--quality', default=DEFAULT_QUALITY,
                        choices=['High Quality', 'Standard Quality'],
                        help=f'Video quality (default: {DEFAULT_QUALITY})')
    parser.add_argument('--output', help='Output filename')
    parser.add_argument('--script-file', help='Read script from file instead of argument')

    args = parser.parse_args()

    # Get script text
    if args.script_file:
        if not os.path.exists(args.script_file):
            print(f"❌ Script file not found: {args.script_file}")
            sys.exit(1)
        with open(args.script_file, 'r') as f:
            script_text = f.read()
    else:
        script_text = args.script

    # Check for batch mode
    if '---' in script_text:
        scripts = [s.strip() for s in script_text.split('---') if s.strip()]
        print(f"📋 Batch mode: {len(scripts)} scripts detected")

        results = generate_batch_videos(
            scripts,
            voice_name=args.voice,
            title=args.title,
            video_dataset=args.video_dataset,
            music_dataset=args.music_dataset,
            aspect_ratio=args.aspect,
            quality=args.quality
        )

        # Exit with error if any failed
        if any(not r['success'] for r in results):
            sys.exit(1)

    else:
        # Single video mode
        result = generate_complete_video(
            script_text,
            voice_name=args.voice,
            title=args.title,
            video_dataset=args.video_dataset,
            music_dataset=args.music_dataset,
            aspect_ratio=args.aspect,
            quality=args.quality,
            output_filename=args.output
        )

        if not result['success']:
            sys.exit(1)


if __name__ == "__main__":
    main()
