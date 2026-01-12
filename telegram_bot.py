#!/usr/bin/env python3
"""
Telegram Bot for Video Generation System
Handles voiceover, subtitle, and video generation with flexible pipeline control
"""

import os
import sys
import json
import time
import requests
import threading
from datetime import datetime

from config import TELEGRAM_BOT_TOKEN, TELEGRAM_API_URL, DEFAULT_VOICE, DEFAULT_ASPECT_RATIO, DEFAULT_QUALITY
from voiceover_generator import generate_tts_audio, generate_voiceover_batch, get_audio_duration
from subtitle_processor import process_voiceover_to_subtitles, split_text_into_lines, generate_srt_file
from generate_video import generate_complete_video, generate_batch_videos


# ============================================================================
# TELEGRAM API FUNCTIONS
# ============================================================================

def send_message(chat_id, text, parse_mode="Markdown"):
    """Send text message to Telegram"""
    url = f"{TELEGRAM_API_URL}{TELEGRAM_BOT_TOKEN}/sendMessage"
    data = {
        "chat_id": chat_id,
        "text": text,
        "parse_mode": parse_mode
    }
    try:
        response = requests.post(url, json=data, timeout=30)
        return response.json()
    except Exception as e:
        print(f"Error sending message: {e}")
        return None


def send_audio(chat_id, audio_path, caption=None):
    """Send audio file to Telegram"""
    url = f"{TELEGRAM_API_URL}{TELEGRAM_BOT_TOKEN}/sendAudio"

    try:
        with open(audio_path, 'rb') as audio_file:
            files = {'audio': audio_file}
            data = {'chat_id': chat_id}
            if caption:
                data['caption'] = caption

            response = requests.post(url, data=data, files=files, timeout=60)
            return response.json()
    except Exception as e:
        print(f"Error sending audio: {e}")
        return None


def send_document(chat_id, file_path, caption=None):
    """Send document file to Telegram"""
    url = f"{TELEGRAM_API_URL}{TELEGRAM_BOT_TOKEN}/sendDocument"

    try:
        with open(file_path, 'rb') as doc_file:
            files = {'document': doc_file}
            data = {'chat_id': chat_id}
            if caption:
                data['caption'] = caption

            response = requests.post(url, data=data, files=files, timeout=60)
            return response.json()
    except Exception as e:
        print(f"Error sending document: {e}")
        return None


def send_video(chat_id, video_path, caption=None):
    """Send video file to Telegram"""
    url = f"{TELEGRAM_API_URL}{TELEGRAM_BOT_TOKEN}/sendVideo"

    try:
        with open(video_path, 'rb') as video_file:
            files = {'video': video_file}
            data = {'chat_id': chat_id}
            if caption:
                data['caption'] = caption

            response = requests.post(url, data=data, files=files, timeout=300)
            return response.json()
    except Exception as e:
        print(f"Error sending video: {e}")
        return None


def get_updates(offset=None):
    """Get updates from Telegram"""
    url = f"{TELEGRAM_API_URL}{TELEGRAM_BOT_TOKEN}/getUpdates"
    params = {"timeout": 30, "offset": offset}

    try:
        response = requests.get(url, params=params, timeout=35)
        return response.json()
    except Exception as e:
        print(f"Error getting updates: {e}")
        return None


# ============================================================================
# COMMAND HANDLERS
# ============================================================================

def handle_start(chat_id):
    """Handle /start command"""
    message = """
🎬 **Welcome to Video Generation Bot!**

I can help you create professional videos with AI voiceover and subtitles!

**📋 Available Commands:**

🎤 **Voiceover Only:**
`/voiceover Your text here`
Generates voiceover and sends audio back

📝 **Subtitle Only:**
`/subtitle audio_file`
Reply to an audio file with this command

🎬 **Complete Video:**
`/video Your script here`
Generates complete video with voiceover, subtitles, and effects

⚡ **Batch Mode:**
Use `---` to separate multiple items:
`/voiceover Text 1 --- Text 2 --- Text 3`

**🎨 Options:**
- Voice: Puck, Charon, Kore, Fenrir, Aoede
- Aspect: 9:16, 4:5, 16:9, 1:1
- Quality: High, Standard

**📚 Examples:**

Generate voiceover:
`/voiceover Hello world!`

Batch voiceovers:
`/voiceover Script 1 --- Script 2 --- Script 3`

Generate video:
`/video Amazing content for TikTok!`

**💡 Tips:**
- Each command works independently
- Results sent back to you immediately
- Batch mode generates multiple items

Ready to create? Send me a command! 🚀
"""
    send_message(chat_id, message)


def handle_voiceover(chat_id, text, voice="Puck"):
    """Handle /voiceover command - generates and sends voiceovers"""
    if not text or not text.strip():
        send_message(chat_id, "❌ Please provide text for voiceover!\n\nExample: `/voiceover Hello world!`")
        return

    # Check for batch mode
    if '---' in text:
        scripts = [s.strip() for s in text.split('---') if s.strip()]
        send_message(chat_id, f"🎤 **Batch Voiceover Generation**\n\nGenerating {len(scripts)} voiceovers...")

        # Generate batch
        results = []
        for i, script in enumerate(scripts, 1):
            send_message(chat_id, f"⏳ Generating voiceover {i}/{len(scripts)}...")

            audio_path, status = generate_tts_audio(
                script,
                voice_name=voice,
                output_path=f"exports/voiceover_{i:03d}.wav",
                use_rotation=True
            )

            if audio_path:
                # Send audio back to Telegram
                duration = get_audio_duration(audio_path)
                caption = f"🎤 Voiceover {i}/{len(scripts)}\n⏱️ Duration: {duration:.2f}s\n🔊 Voice: {voice}"
                send_audio(chat_id, audio_path, caption)
                results.append(("success", audio_path))
            else:
                send_message(chat_id, f"❌ Voiceover {i} failed: {status}")
                results.append(("failed", status))

        # Summary
        successful = sum(1 for r in results if r[0] == "success")
        send_message(chat_id, f"✅ **Batch Complete!**\n\nSuccessful: {successful}/{len(scripts)}")

    else:
        # Single voiceover
        send_message(chat_id, f"🎤 Generating voiceover with {voice} voice...")

        audio_path, status = generate_tts_audio(
            text,
            voice_name=voice,
            use_rotation=True
        )

        if audio_path:
            duration = get_audio_duration(audio_path)
            caption = f"🎤 Voiceover Generated\n⏱️ Duration: {duration:.2f}s\n🔊 Voice: {voice}"
            send_audio(chat_id, audio_path, caption)
            send_message(chat_id, f"✅ Voiceover generated successfully!")
        else:
            send_message(chat_id, f"❌ Failed to generate voiceover: {status}")


def handle_subtitle(chat_id, audio_path):
    """Handle /subtitle command - generates and sends subtitles"""
    if not audio_path or not os.path.exists(audio_path):
        send_message(chat_id, "❌ Please reply to an audio file with `/subtitle` command!")
        return

    send_message(chat_id, "📝 Generating subtitles...")

    try:
        # Transcribe audio
        word_data = process_voiceover_to_subtitles(audio_path)

        # Generate subtitles
        subtitles = split_text_into_lines(word_data)

        # Save SRT file
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        srt_path = f"exports/subtitles_{timestamp}.srt"
        generate_srt_file(subtitles, srt_path)

        # Send SRT file
        caption = f"📝 Subtitles Generated\n📊 Lines: {len(subtitles)}"
        send_document(chat_id, srt_path, caption)

        # Send preview
        preview = "\n\n".join([f"{i}. {sub['text']}" for i, sub in enumerate(subtitles[:5], 1)])
        if len(subtitles) > 5:
            preview += f"\n\n... and {len(subtitles) - 5} more lines"

        send_message(chat_id, f"✅ **Subtitles Generated!**\n\n**Preview:**\n{preview}")

    except Exception as e:
        send_message(chat_id, f"❌ Failed to generate subtitles: {str(e)}")


def handle_video(chat_id, text, voice="Puck", aspect="9:16", quality="High Quality"):
    """Handle /video command - generates complete videos"""
    if not text or not text.strip():
        send_message(chat_id, "❌ Please provide script for video!\n\nExample: `/video Amazing content!`")
        return

    # Check for batch mode
    if '---' in text:
        scripts = [s.strip() for s in text.split('---') if s.strip()]
        send_message(chat_id, f"🎬 **Batch Video Generation**\n\nGenerating {len(scripts)} videos...")

        # Generate batch
        results = generate_batch_videos(
            scripts,
            voice_name=voice,
            aspect_ratio=aspect,
            quality=quality
        )

        # Send each video
        for i, result in enumerate(results, 1):
            if result['success']:
                caption = (
                    f"🎬 Video {i}/{len(scripts)}\n"
                    f"⏱️ Duration: {result['duration']:.2f}s\n"
                    f"📝 Subtitles: {result['subtitle_count']} lines"
                )
                send_video(chat_id, result['video_path'], caption)
            else:
                send_message(chat_id, f"❌ Video {i} failed: {result['message']}")

        # Summary
        successful = sum(1 for r in results if r['success'])
        send_message(chat_id, f"✅ **Batch Complete!**\n\nSuccessful: {successful}/{len(scripts)}")

    else:
        # Single video
        send_message(chat_id, f"🎬 Generating video...\n\n⏳ This may take a few minutes...")

        result = generate_complete_video(
            script_text=text,
            voice_name=voice,
            aspect_ratio=aspect,
            quality=quality
        )

        if result['success']:
            caption = (
                f"🎬 Video Generated\n"
                f"⏱️ Duration: {result['duration']:.2f}s\n"
                f"📝 Subtitles: {result['subtitle_count']} lines\n"
                f"🔊 Voice: {voice}\n"
                f"📐 Aspect: {aspect}"
            )
            send_video(chat_id, result['video_path'], caption)
            send_message(chat_id, "✅ Video generated successfully!")
        else:
            send_message(chat_id, f"❌ Failed to generate video: {result['message']}")


# ============================================================================
# MESSAGE PROCESSING
# ============================================================================

def process_message(message):
    """Process incoming message"""
    chat_id = message.get('chat', {}).get('id')
    text = message.get('text', '')

    if not chat_id or not text:
        return

    print(f"📨 Message from {chat_id}: {text[:50]}...")

    # Handle commands
    if text.startswith('/start'):
        handle_start(chat_id)

    elif text.startswith('/voiceover'):
        # Extract text after command
        script = text.replace('/voiceover', '', 1).strip()
        handle_voiceover(chat_id, script)

    elif text.startswith('/subtitle'):
        # TODO: Handle audio file reply
        send_message(chat_id, "📝 Please send an audio file, then reply to it with `/subtitle`")

    elif text.startswith('/video'):
        # Extract text after command
        script = text.replace('/video', '', 1).strip()
        handle_video(chat_id, script)

    elif text.startswith('/'):
        send_message(chat_id, "❌ Unknown command! Use /start to see available commands.")

    else:
        # Default: treat as video generation request
        send_message(chat_id, "🎬 Generating video from your script...\n\nUse `/voiceover` for voiceover only or `/video` for complete video.")
        handle_video(chat_id, text)


# ============================================================================
# BOT MAIN LOOP
# ============================================================================

def run_bot():
    """Main bot loop"""
    print("=" * 70)
    print("🤖 TELEGRAM BOT STARTING")
    print("=" * 70)
    print(f"✅ Bot token configured")
    print(f"⏳ Waiting for messages...\n")

    offset = None

    while True:
        try:
            # Get updates
            updates = get_updates(offset)

            if not updates or not updates.get('ok'):
                time.sleep(1)
                continue

            # Process each update
            for update in updates.get('result', []):
                offset = update['update_id'] + 1

                # Handle message
                if 'message' in update:
                    message = update['message']

                    # Process in separate thread to avoid blocking
                    thread = threading.Thread(
                        target=process_message,
                        args=(message,),
                        daemon=True
                    )
                    thread.start()

        except KeyboardInterrupt:
            print("\n\n⚠️  Bot stopped by user")
            break

        except Exception as e:
            print(f"❌ Error in bot loop: {e}")
            time.sleep(5)


# ============================================================================
# MAIN ENTRY POINT
# ============================================================================

if __name__ == "__main__":
    if not TELEGRAM_BOT_TOKEN or TELEGRAM_BOT_TOKEN == "":
        print("❌ Error: TELEGRAM_BOT_TOKEN not configured!")
        print("Please set your bot token in config.py")
        sys.exit(1)

    try:
        run_bot()
    except KeyboardInterrupt:
        print("\n\n👋 Bot shutdown complete")
        sys.exit(0)
