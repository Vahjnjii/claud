"""
Voiceover Generation Module
Generates speech audio from text using Google Gemini TTS API
"""

import os
import wave
import base64
import traceback
from google.genai import Client, types
from config import (
    TTS_MODEL,
    AUDIO_SAMPLE_RATE,
    AVAILABLE_VOICES,
    DEFAULT_VOICE,
    GENERATION_CANCELLED
)
from api_manager import (
    load_api_key,
    get_next_api_key,
    get_current_api_key,
    should_rotate_key
)


def wave_file(audio_bytes, channels=1, sample_width=2, framerate=AUDIO_SAMPLE_RATE):
    """
    Create WAV file from raw audio bytes

    Args:
        audio_bytes (bytes): Raw PCM audio data
        channels (int): Number of audio channels (1=mono, 2=stereo)
        sample_width (int): Sample width in bytes (2 = 16-bit)
        framerate (int): Sample rate in Hz (default: 24000)

    Returns:
        bytes: Complete WAV file data
    """
    import io

    wav_buffer = io.BytesIO()
    with wave.open(wav_buffer, 'wb') as wav_file:
        wav_file.setnchannels(channels)
        wav_file.setsampwidth(sample_width)
        wav_file.setframerate(framerate)
        wav_file.writeframes(audio_bytes)

    return wav_buffer.getvalue()


def generate_tts_audio(text_input, voice_name=DEFAULT_VOICE, output_path=None, use_rotation=False):
    """
    Generate text-to-speech audio using Google Gemini TTS API

    This function converts text to speech using Google's Gemini 2.5 Flash TTS model.
    It supports multiple voices and automatic API key rotation on quota errors.

    Args:
        text_input (str): Text to convert to speech
        voice_name (str): Voice to use (Puck, Charon, Kore, Fenrir, or Aoede)
        output_path (str, optional): Path to save the audio file. If None, auto-generates filename
        use_rotation (bool): Whether to use API key rotation on errors

    Returns:
        tuple: (audio_file_path, status_message)
            - audio_file_path (str): Path to generated WAV file, or None if failed
            - status_message (str): Status message describing result or error

    Raises:
        None: All exceptions are caught and returned as status messages

    Example:
        >>> audio_path, status = generate_tts_audio("Hello world!", "Puck")
        >>> if audio_path:
        ...     print(f"Audio saved to: {audio_path}")
        ... else:
        ...     print(f"Generation failed: {status}")
    """
    global GENERATION_CANCELLED

    # Check if generation was cancelled
    if GENERATION_CANCELLED:
        return None, "Generation cancelled by user"

    # Validate voice name
    if voice_name not in AVAILABLE_VOICES:
        return None, f"Invalid voice: {voice_name}. Available: {', '.join(AVAILABLE_VOICES.keys())}"

    # Validate text input
    if not text_input or not text_input.strip():
        return None, "Text input is empty"

    try:
        # Load current API key
        api_key = get_current_api_key() if use_rotation else load_api_key()

        # Initialize Gemini client
        client = Client(api_key=api_key)

        print(f"🎤 Generating voiceover with voice: {voice_name}")
        print(f"📝 Text length: {len(text_input)} characters")

        # Configure voice settings
        voice_config = types.VoiceConfig(
            voice_name=voice_name.lower()
        )

        # Configure speech parameters
        speech_config = types.SpeechConfig(
            voice_config=voice_config
        )

        # Generate speech
        response = client.models.generate_content(
            model=TTS_MODEL,
            contents=text_input,
            config=types.GenerateContentConfig(
                speech_config=speech_config
            )
        )

        # Check for cancellation
        if GENERATION_CANCELLED:
            return None, "Generation cancelled by user"

        # Extract audio data from response
        if not hasattr(response, 'candidates') or not response.candidates:
            return None, "No audio data received from API"

        # Get the audio bytes from the response
        audio_data = None
        for candidate in response.candidates:
            if hasattr(candidate, 'content') and hasattr(candidate.content, 'parts'):
                for part in candidate.content.parts:
                    if hasattr(part, 'inline_data') and hasattr(part.inline_data, 'data'):
                        audio_data = part.inline_data.data
                        break
            if audio_data:
                break

        if not audio_data:
            return None, "Could not extract audio data from API response"

        # Decode base64 audio data
        try:
            audio_bytes = base64.b64decode(audio_data)
        except Exception as e:
            return None, f"Failed to decode audio data: {str(e)}"

        # Create WAV file
        wav_data = wave_file(audio_bytes)

        # Determine output path
        if output_path is None:
            from datetime import datetime
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_path = f"voiceover_{voice_name}_{timestamp}.wav"

        # Ensure output directory exists
        output_dir = os.path.dirname(output_path)
        if output_dir:
            os.makedirs(output_dir, exist_ok=True)

        # Save WAV file
        with open(output_path, 'wb') as f:
            f.write(wav_data)

        print(f"✅ Voiceover generated successfully: {output_path}")

        return output_path, "Success"

    except Exception as e:
        error_message = str(e)
        error_trace = traceback.format_exc()

        print(f"❌ Error generating voiceover: {error_message}")
        print(f"Traceback: {error_trace}")

        # Check if we should rotate API key
        if use_rotation and should_rotate_key(error_message):
            print("🔄 Rotating to next API key...")
            get_next_api_key()
            status = f"API error (key rotated): {error_message}"
        else:
            status = f"Generation failed: {error_message}"

        return None, status


def generate_voiceover_batch(texts, voice_name=DEFAULT_VOICE, output_dir="voiceovers"):
    """
    Generate multiple voiceovers from a list of texts

    Args:
        texts (list): List of text strings to convert to speech
        voice_name (str): Voice to use for all voiceovers
        output_dir (str): Directory to save voiceover files

    Returns:
        list: List of tuples (audio_path, status_message) for each text
    """
    os.makedirs(output_dir, exist_ok=True)

    results = []
    for i, text in enumerate(texts, 1):
        output_path = os.path.join(output_dir, f"voiceover_{i:03d}.wav")
        print(f"\n📢 Generating voiceover {i}/{len(texts)}...")

        audio_path, status = generate_tts_audio(
            text,
            voice_name=voice_name,
            output_path=output_path,
            use_rotation=True
        )

        results.append((audio_path, status))

        if not audio_path:
            print(f"⚠️ Failed to generate voiceover {i}: {status}")
        else:
            print(f"✅ Voiceover {i} completed")

    return results


def get_audio_duration(audio_path):
    """
    Get duration of an audio file in seconds

    Args:
        audio_path (str): Path to audio file

    Returns:
        float: Duration in seconds, or 0 if error
    """
    try:
        with wave.open(audio_path, 'rb') as wav_file:
            frames = wav_file.getnframes()
            rate = wav_file.getframerate()
            duration = frames / float(rate)
            return duration
    except Exception as e:
        print(f"Error getting audio duration: {e}")
        return 0


def test_voice(voice_name=DEFAULT_VOICE, test_text="Hello, this is a test of the text to speech system."):
    """
    Test voiceover generation with a sample text

    Args:
        voice_name (str): Voice to test
        test_text (str): Text to use for testing

    Returns:
        bool: True if test successful, False otherwise
    """
    print(f"\n🧪 Testing voice: {voice_name}")
    print(f"📝 Test text: {test_text}")

    audio_path, status = generate_tts_audio(test_text, voice_name)

    if audio_path:
        duration = get_audio_duration(audio_path)
        print(f"✅ Test successful!")
        print(f"📊 Audio duration: {duration:.2f} seconds")
        print(f"📁 File saved: {audio_path}")
        return True
    else:
        print(f"❌ Test failed: {status}")
        return False


# ============================================================================
# STANDALONE EXECUTION
# ============================================================================
if __name__ == "__main__":
    import sys

    print("=" * 70)
    print("🎙️  VOICEOVER GENERATOR")
    print("=" * 70)

    # Check command line arguments
    if len(sys.argv) > 1:
        # Command line mode
        text = " ".join(sys.argv[1:])
        voice = DEFAULT_VOICE

        # Check if first arg is a valid voice name
        if sys.argv[1] in AVAILABLE_VOICES:
            voice = sys.argv[1]
            text = " ".join(sys.argv[2:])

        if not text:
            print("❌ No text provided!")
            sys.exit(1)

        print(f"\n📝 Text: {text}")
        print(f"🎤 Voice: {voice}")
        print(f"\n⏳ Generating voiceover...\n")

        audio_path, status = generate_tts_audio(text, voice)

        if audio_path:
            duration = get_audio_duration(audio_path)
            print(f"\n✅ SUCCESS!")
            print(f"📁 Saved to: {audio_path}")
            print(f"📊 Duration: {duration:.2f} seconds")
        else:
            print(f"\n❌ FAILED: {status}")
            sys.exit(1)

    else:
        # Interactive mode
        print("\n🎤 Available voices:")
        for i, (voice, description) in enumerate(AVAILABLE_VOICES.items(), 1):
            print(f"  {i}. {voice} - {description}")

        print("\n📋 Usage:")
        print(f"  python voiceover_generator.py [voice] <text>")
        print(f"\nExample:")
        print(f"  python voiceover_generator.py Puck Hello world!")
        print(f"  python voiceover_generator.py Hello world!  (uses {DEFAULT_VOICE})")

        print("\n🧪 Running test...")
        test_voice()
