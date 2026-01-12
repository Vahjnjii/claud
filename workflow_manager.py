#!/usr/bin/env python3
"""
Workflow Manager
Controls the pipeline flow and decides whether to send results to Telegram or continue processing
"""

import os
from enum import Enum


class WorkflowMode(Enum):
    """Workflow execution modes"""
    STANDALONE = "standalone"  # Send results immediately to Telegram
    PIPELINE = "pipeline"      # Continue to next step
    AUTO = "auto"             # Automatically determine based on command


class WorkflowStep(Enum):
    """Available workflow steps"""
    VOICEOVER = "voiceover"
    SUBTITLE = "subtitle"
    VIDEO = "video"


class WorkflowManager:
    """
    Manages workflow execution and determines whether to send results or continue
    """

    def __init__(self, mode=WorkflowMode.AUTO):
        """
        Initialize workflow manager

        Args:
            mode (WorkflowMode): Execution mode
        """
        self.mode = mode
        self.current_step = None
        self.results = {}
        self.chat_id = None

    def set_chat_id(self, chat_id):
        """Set Telegram chat ID for sending results"""
        self.chat_id = chat_id

    def should_send_to_telegram(self, step):
        """
        Determine if results should be sent to Telegram at this step

        Args:
            step (WorkflowStep): Current workflow step

        Returns:
            bool: True if should send to Telegram, False if continue pipeline
        """
        if self.mode == WorkflowMode.STANDALONE:
            # Always send immediately
            return True

        elif self.mode == WorkflowMode.PIPELINE:
            # Only send at the end (video step)
            return step == WorkflowStep.VIDEO

        else:  # AUTO mode
            # Send at each step completion
            return True

    def save_step_result(self, step, result):
        """
        Save result from a workflow step

        Args:
            step (WorkflowStep): Workflow step
            result (dict): Step result data
        """
        self.results[step.value] = result
        self.current_step = step

    def get_step_result(self, step):
        """
        Get saved result from a workflow step

        Args:
            step (WorkflowStep): Workflow step

        Returns:
            dict: Step result data or None
        """
        return self.results.get(step.value)

    def should_continue_to_next_step(self, current_step):
        """
        Determine if should continue to next step

        Args:
            current_step (WorkflowStep): Current step

        Returns:
            tuple: (should_continue: bool, next_step: WorkflowStep or None)
        """
        if self.mode == WorkflowMode.STANDALONE:
            # Don't continue, send results
            return (False, None)

        # Pipeline mode - determine next step
        if current_step == WorkflowStep.VOICEOVER:
            return (True, WorkflowStep.SUBTITLE)

        elif current_step == WorkflowStep.SUBTITLE:
            return (True, WorkflowStep.VIDEO)

        elif current_step == WorkflowStep.VIDEO:
            # End of pipeline
            return (False, None)

        return (False, None)

    def get_pipeline_description(self):
        """Get description of current pipeline mode"""
        if self.mode == WorkflowMode.STANDALONE:
            return "Standalone mode - results sent immediately"

        elif self.mode == WorkflowMode.PIPELINE:
            return "Pipeline mode - processing all steps, sending final result only"

        else:
            return "Auto mode - sending results at each step"


# ============================================================================
# WORKFLOW EXECUTION FUNCTIONS
# ============================================================================

def execute_voiceover_workflow(text, chat_id, voice="Puck", mode=WorkflowMode.AUTO):
    """
    Execute voiceover generation workflow

    Args:
        text (str): Text to convert to speech
        chat_id (int): Telegram chat ID
        voice (str): Voice to use
        mode (WorkflowMode): Execution mode

    Returns:
        dict: Workflow result with paths and status
    """
    from voiceover_generator import generate_tts_audio
    from telegram_bot import send_audio, send_message

    manager = WorkflowManager(mode)
    manager.set_chat_id(chat_id)

    # Generate voiceover
    audio_path, status = generate_tts_audio(text, voice_name=voice, use_rotation=True)

    if not audio_path:
        return {'success': False, 'message': status}

    # Save result
    result = {'audio_path': audio_path, 'status': status, 'text': text}
    manager.save_step_result(WorkflowStep.VOICEOVER, result)

    # Check if should send to Telegram
    if manager.should_send_to_telegram(WorkflowStep.VOICEOVER):
        send_audio(chat_id, audio_path, f"🎤 Voiceover: {voice}")

    # Check if should continue
    should_continue, next_step = manager.should_continue_to_next_step(WorkflowStep.VOICEOVER)

    if should_continue and next_step == WorkflowStep.SUBTITLE:
        # Continue to subtitle generation
        return execute_subtitle_workflow(audio_path, chat_id, mode)

    return {'success': True, 'audio_path': audio_path, 'mode': mode.value}


def execute_subtitle_workflow(audio_path, chat_id, mode=WorkflowMode.AUTO):
    """
    Execute subtitle generation workflow

    Args:
        audio_path (str): Path to audio file
        chat_id (int): Telegram chat ID
        mode (WorkflowMode): Execution mode

    Returns:
        dict: Workflow result with paths and status
    """
    from subtitle_processor import process_voiceover_to_subtitles, split_text_into_lines, generate_srt_file
    from telegram_bot import send_document, send_message

    manager = WorkflowManager(mode)
    manager.set_chat_id(chat_id)

    # Generate subtitles
    word_data = process_voiceover_to_subtitles(audio_path)
    subtitles = split_text_into_lines(word_data)

    # Save SRT
    from datetime import datetime
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    srt_path = f"exports/subtitles_{timestamp}.srt"
    generate_srt_file(subtitles, srt_path)

    # Save result
    result = {'srt_path': srt_path, 'subtitles': subtitles, 'audio_path': audio_path}
    manager.save_step_result(WorkflowStep.SUBTITLE, result)

    # Check if should send to Telegram
    if manager.should_send_to_telegram(WorkflowStep.SUBTITLE):
        send_document(chat_id, srt_path, f"📝 Subtitles: {len(subtitles)} lines")

    # Check if should continue
    should_continue, next_step = manager.should_continue_to_next_step(WorkflowStep.SUBTITLE)

    if should_continue and next_step == WorkflowStep.VIDEO:
        # Continue to video generation
        # Would need to extract original text - for now return result
        pass

    return {'success': True, 'srt_path': srt_path, 'subtitle_count': len(subtitles), 'mode': mode.value}


def execute_video_workflow(text, chat_id, voice="Puck", aspect="9:16", quality="High Quality", mode=WorkflowMode.AUTO):
    """
    Execute complete video generation workflow

    Args:
        text (str): Script text
        chat_id (int): Telegram chat ID
        voice (str): Voice to use
        aspect (str): Aspect ratio
        quality (str): Video quality
        mode (WorkflowMode): Execution mode

    Returns:
        dict: Workflow result with paths and status
    """
    from generate_video import generate_complete_video
    from telegram_bot import send_video, send_message

    manager = WorkflowManager(mode)
    manager.set_chat_id(chat_id)

    # Generate complete video
    result = generate_complete_video(
        script_text=text,
        voice_name=voice,
        aspect_ratio=aspect,
        quality=quality
    )

    if not result['success']:
        return result

    # Save result
    manager.save_step_result(WorkflowStep.VIDEO, result)

    # Always send final video to Telegram
    caption = (
        f"🎬 Video Complete\n"
        f"⏱️ Duration: {result['duration']:.2f}s\n"
        f"📝 Subtitles: {result['subtitle_count']} lines"
    )
    send_video(chat_id, result['video_path'], caption)

    return result


# ============================================================================
# BATCH WORKFLOW FUNCTIONS
# ============================================================================

def execute_batch_voiceover_workflow(scripts, chat_id, voice="Puck", mode=WorkflowMode.AUTO):
    """
    Execute batch voiceover generation workflow

    Args:
        scripts (list): List of text scripts
        chat_id (int): Telegram chat ID
        voice (str): Voice to use
        mode (WorkflowMode): Execution mode

    Returns:
        list: List of results for each script
    """
    from telegram_bot import send_message

    send_message(chat_id, f"🎤 **Batch Voiceover**\n\nGenerating {len(scripts)} voiceovers...")

    results = []
    for i, script in enumerate(scripts, 1):
        send_message(chat_id, f"⏳ Processing {i}/{len(scripts)}...")

        result = execute_voiceover_workflow(script, chat_id, voice, mode)
        results.append(result)

    # Summary
    successful = sum(1 for r in results if r.get('success'))
    send_message(chat_id, f"✅ **Batch Complete!**\n\nSuccessful: {successful}/{len(scripts)}")

    return results


def execute_batch_video_workflow(scripts, chat_id, voice="Puck", aspect="9:16", quality="High Quality", mode=WorkflowMode.AUTO):
    """
    Execute batch video generation workflow

    Args:
        scripts (list): List of text scripts
        chat_id (int): Telegram chat ID
        voice (str): Voice to use
        aspect (str): Aspect ratio
        quality (str): Video quality
        mode (WorkflowMode): Execution mode

    Returns:
        list: List of results for each script
    """
    from telegram_bot import send_message

    send_message(chat_id, f"🎬 **Batch Video Generation**\n\nGenerating {len(scripts)} videos...")

    results = []
    for i, script in enumerate(scripts, 1):
        send_message(chat_id, f"⏳ Processing video {i}/{len(scripts)}...")

        result = execute_video_workflow(script, chat_id, voice, aspect, quality, mode)
        results.append(result)

    # Summary
    successful = sum(1 for r in results if r.get('success'))
    send_message(chat_id, f"✅ **Batch Complete!**\n\nSuccessful: {successful}/{len(scripts)}")

    return results


# ============================================================================
# MAIN EXECUTION
# ============================================================================

if __name__ == "__main__":
    print("=" * 70)
    print("📋 WORKFLOW MANAGER")
    print("=" * 70)
    print("\nWorkflow modes:")
    print("  1. STANDALONE - Send results immediately")
    print("  2. PIPELINE - Process all steps, send final result")
    print("  3. AUTO - Send at each step completion")
    print("\nThis module is used by telegram_bot.py")
    print("=" * 70)
