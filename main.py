#!/usr/bin/env python3
"""
Main Entry Point for Video Generation System
Simple interface to generate videos quickly
"""

import sys
from generate_video import generate_complete_video, generate_batch_videos


def main():
    """
    Simple interactive mode for video generation
    """
    print("=" * 70)
    print("🎬 VIDEO GENERATION SYSTEM")
    print("=" * 70)
    print("\nWelcome! This system generates complete videos with:")
    print("  ✅ AI Voiceover (Google Gemini TTS)")
    print("  ✅ Auto-generated Subtitles")
    print("  ✅ Background Video & Music")
    print("  ✅ Professional Composition")

    # Check if script provided as argument
    if len(sys.argv) > 1:
        script = " ".join(sys.argv[1:])
        print(f"\n📝 Using provided script: {script[:100]}...")
    else:
        # Interactive mode
        print("\n" + "-" * 70)
        print("📝 Enter your video script:")
        print("   (Press Enter twice when done)")
        print("   (Use '---' to separate multiple scripts for batch mode)")
        print("-" * 70)

        lines = []
        while True:
            try:
                line = input()
                if line == "" and lines and lines[-1] == "":
                    break
                lines.append(line)
            except EOFError:
                break

        script = "\n".join(lines).strip()

    if not script:
        print("\n❌ No script provided!")
        print("\n💡 Usage:")
        print("   python main.py \"Your script here\"")
        print("   python main.py  (for interactive mode)")
        sys.exit(1)

    # Voice selection
    print("\n" + "-" * 70)
    print("🎤 Select Voice:")
    print("   1. Puck (Default)")
    print("   2. Charon")
    print("   3. Kore")
    print("   4. Fenrir")
    print("   5. Aoede")
    print("-" * 70)

    voice_map = {
        "1": "Puck",
        "2": "Charon",
        "3": "Kore",
        "4": "Fenrir",
        "5": "Aoede",
        "": "Puck"
    }

    voice_choice = input("Enter choice (1-5, or press Enter for default): ").strip()
    voice = voice_map.get(voice_choice, "Puck")
    print(f"✅ Selected voice: {voice}")

    # Title
    print("\n" + "-" * 70)
    title = input("🎯 Enter video title (or press Enter to skip): ").strip()
    if title:
        print(f"✅ Title: {title}")
    else:
        title = None
        print("⏭️  Skipping title")

    # Aspect ratio
    print("\n" + "-" * 70)
    print("📐 Select Aspect Ratio:")
    print("   1. 9:16 - Vertical (TikTok, Reels, Shorts) [Default]")
    print("   2. 4:5 - Portrait (Instagram)")
    print("   3. 16:9 - Horizontal (YouTube)")
    print("   4. 1:1 - Square (Instagram)")
    print("-" * 70)

    aspect_map = {
        "1": "9:16",
        "2": "4:5",
        "3": "16:9",
        "4": "1:1",
        "": "9:16"
    }

    aspect_choice = input("Enter choice (1-4, or press Enter for default): ").strip()
    aspect = aspect_map.get(aspect_choice, "9:16")
    print(f"✅ Selected aspect ratio: {aspect}")

    # Quality
    print("\n" + "-" * 70)
    print("🎨 Select Quality:")
    print("   1. High Quality (1080p) [Default]")
    print("   2. Standard Quality (720p)")
    print("-" * 70)

    quality_map = {
        "1": "High Quality",
        "2": "Standard Quality",
        "": "High Quality"
    }

    quality_choice = input("Enter choice (1-2, or press Enter for default): ").strip()
    quality = quality_map.get(quality_choice, "High Quality")
    print(f"✅ Selected quality: {quality}")

    # Check for batch mode
    print("\n" + "=" * 70)
    if '---' in script:
        scripts = [s.strip() for s in script.split('---') if s.strip()]
        print(f"🎬 BATCH MODE: Generating {len(scripts)} videos")
        print("=" * 70)

        results = generate_batch_videos(
            scripts,
            voice_name=voice,
            title=title,
            aspect_ratio=aspect,
            quality=quality
        )

        # Display results
        print("\n" + "=" * 70)
        print("📊 RESULTS")
        print("=" * 70)

        for i, result in enumerate(results, 1):
            if result['success']:
                print(f"✅ Video {i}: {result['video_path']}")
            else:
                print(f"❌ Video {i}: {result['message']}")

    else:
        print("🎬 SINGLE VIDEO MODE")
        print("=" * 70)

        result = generate_complete_video(
            script_text=script,
            voice_name=voice,
            title=title,
            aspect_ratio=aspect,
            quality=quality
        )

        print("\n" + "=" * 70)
        if result['success']:
            print("✅ SUCCESS!")
            print("=" * 70)
            print(f"📁 Video: {result['video_path']}")
            print(f"⏱️  Duration: {result['duration']:.2f} seconds")
            print(f"📝 Subtitles: {result['subtitle_count']} lines")
            print(f"🎤 Voiceover: {result['voiceover_path']}")
            print(f"📄 Subtitles SRT: {result['subtitles_path']}")
        else:
            print("❌ FAILED")
            print("=" * 70)
            print(f"Error: {result['message']}")
            sys.exit(1)

    print("=" * 70)
    print("🎉 Video generation complete!")
    print("=" * 70)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️  Generation cancelled by user")
        sys.exit(0)
    except Exception as e:
        print(f"\n\n❌ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
