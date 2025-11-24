"""
Dataset Management Module
Handles video and music dataset scanning and file selection
"""

import os
import glob
import random
from config import KAGGLE_INPUT_DIR


def scan_available_folders(base_path=KAGGLE_INPUT_DIR):
    """
    Scan for available video and music datasets

    Args:
        base_path (str): Base path to scan (default: /kaggle/input)

    Returns:
        dict: Dictionary with 'videos' and 'music' folder lists
    """
    video_folders = []
    music_folders = []

    if not os.path.exists(base_path):
        print(f"⚠️ Input directory not found: {base_path}")
        return {'videos': [], 'music': []}

    try:
        # Scan all subdirectories
        for entry in os.listdir(base_path):
            folder_path = os.path.join(base_path, entry)

            if not os.path.isdir(folder_path):
                continue

            # Check for video files
            video_extensions = ['*.mp4', '*.avi', '*.mov', '*.mkv', '*.webm']
            has_videos = False

            for ext in video_extensions:
                pattern = os.path.join(folder_path, '**', ext)
                if glob.glob(pattern, recursive=True):
                    has_videos = True
                    break

            # Check for music files
            music_extensions = ['*.mp3', '*.wav', '*.m4a', '*.ogg', '*.flac']
            has_music = False

            for ext in music_extensions:
                pattern = os.path.join(folder_path, '**', ext)
                if glob.glob(pattern, recursive=True):
                    has_music = True
                    break

            # Categorize folder
            if has_videos:
                video_folders.append({
                    'name': entry,
                    'path': folder_path
                })

            if has_music:
                music_folders.append({
                    'name': entry,
                    'path': folder_path
                })

    except Exception as e:
        print(f"❌ Error scanning folders: {e}")

    print(f"📁 Found {len(video_folders)} video datasets")
    print(f"🎵 Found {len(music_folders)} music datasets")

    return {
        'videos': video_folders,
        'music': music_folders
    }


def get_dataset_by_name(dataset_name, base_path=KAGGLE_INPUT_DIR):
    """
    Get dataset path by name

    Args:
        dataset_name (str): Name of the dataset
        base_path (str): Base path to scan

    Returns:
        str: Full path to dataset, or None if not found
    """
    dataset_path = os.path.join(base_path, dataset_name)

    if os.path.exists(dataset_path):
        return dataset_path

    return None


def get_video_files(folder_path, recursive=True):
    """
    Get all video files from a folder

    Args:
        folder_path (str): Path to folder
        recursive (bool): Whether to search recursively

    Returns:
        list: List of video file paths
    """
    if not os.path.exists(folder_path):
        return []

    video_extensions = ['*.mp4', '*.avi', '*.mov', '*.mkv', '*.webm']
    video_files = []

    for ext in video_extensions:
        pattern = os.path.join(folder_path, '**', ext) if recursive else os.path.join(folder_path, ext)
        video_files.extend(glob.glob(pattern, recursive=recursive))

    return video_files


def get_music_files(folder_path, recursive=True):
    """
    Get all music files from a folder

    Args:
        folder_path (str): Path to folder
        recursive (bool): Whether to search recursively

    Returns:
        list: List of music file paths
    """
    if not os.path.exists(folder_path):
        return []

    music_extensions = ['*.mp3', '*.wav', '*.m4a', '*.ogg', '*.flac']
    music_files = []

    for ext in music_extensions:
        pattern = os.path.join(folder_path, '**', ext) if recursive else os.path.join(folder_path, ext)
        music_files.extend(glob.glob(pattern, recursive=recursive))

    return music_files


def get_random_video_file(folder_path):
    """
    Get a random video file from folder

    Args:
        folder_path (str): Path to video folder

    Returns:
        str: Path to random video file, or None if no videos found
    """
    video_files = get_video_files(folder_path)

    if not video_files:
        print(f"⚠️ No video files found in: {folder_path}")
        return None

    selected = random.choice(video_files)
    print(f"🎬 Selected video: {os.path.basename(selected)}")

    return selected


def get_random_music_file(folder_path):
    """
    Get a random music file from folder

    Args:
        folder_path (str): Path to music folder

    Returns:
        str: Path to random music file, or None if no music found
    """
    music_files = get_music_files(folder_path)

    if not music_files:
        print(f"⚠️ No music files found in: {folder_path}")
        return None

    selected = random.choice(music_files)
    print(f"🎵 Selected music: {os.path.basename(selected)}")

    return selected


def get_folder_choices(base_path=KAGGLE_INPUT_DIR):
    """
    Get formatted folder choices for UI dropdowns

    Args:
        base_path (str): Base path to scan

    Returns:
        dict: Dictionary with 'video_choices' and 'music_choices' lists
    """
    folders = scan_available_folders(base_path)

    video_choices = [(f['name'], f['path']) for f in folders['videos']]
    music_choices = [(f['name'], f['path']) for f in folders['music']]

    return {
        'video_choices': video_choices,
        'music_choices': music_choices
    }


def validate_dataset(folder_path, dataset_type='video'):
    """
    Validate that a dataset folder has required files

    Args:
        folder_path (str): Path to dataset folder
        dataset_type (str): Type of dataset ('video' or 'music')

    Returns:
        dict: Validation result with 'valid' bool and 'message' string
    """
    if not os.path.exists(folder_path):
        return {
            'valid': False,
            'message': f"Folder not found: {folder_path}"
        }

    if not os.path.isdir(folder_path):
        return {
            'valid': False,
            'message': f"Not a directory: {folder_path}"
        }

    # Check for files
    if dataset_type == 'video':
        files = get_video_files(folder_path)
        file_type = "video"
    elif dataset_type == 'music':
        files = get_music_files(folder_path)
        file_type = "music"
    else:
        return {
            'valid': False,
            'message': f"Invalid dataset type: {dataset_type}"
        }

    if not files:
        return {
            'valid': False,
            'message': f"No {file_type} files found in folder"
        }

    return {
        'valid': True,
        'message': f"Found {len(files)} {file_type} file(s)"
    }


def create_local_dataset(name, dataset_type='video', source_files=None):
    """
    Create a local dataset folder with files

    Args:
        name (str): Name for the dataset
        dataset_type (str): Type ('video' or 'music')
        source_files (list, optional): List of files to copy

    Returns:
        str: Path to created dataset folder
    """
    import shutil

    # Create local datasets directory
    local_datasets = os.path.join(os.path.dirname(__file__), 'datasets')
    os.makedirs(local_datasets, exist_ok=True)

    # Create dataset folder
    dataset_path = os.path.join(local_datasets, name)
    os.makedirs(dataset_path, exist_ok=True)

    print(f"📁 Created dataset folder: {dataset_path}")

    # Copy source files if provided
    if source_files:
        copied = 0
        for source in source_files:
            if os.path.exists(source):
                dest = os.path.join(dataset_path, os.path.basename(source))
                shutil.copy2(source, dest)
                copied += 1

        print(f"✅ Copied {copied} files to dataset")

    return dataset_path


# ============================================================================
# STANDALONE EXECUTION
# ============================================================================
if __name__ == "__main__":
    import sys

    print("=" * 70)
    print("📦 DATASET MANAGER")
    print("=" * 70)

    # Check if custom path provided
    scan_path = sys.argv[1] if len(sys.argv) > 1 else KAGGLE_INPUT_DIR

    print(f"\n📂 Scanning: {scan_path}\n")

    # Scan for datasets
    folders = scan_available_folders(scan_path)

    # Display results
    print("\n" + "=" * 70)
    print("🎬 VIDEO DATASETS")
    print("=" * 70)

    if folders['videos']:
        for i, folder in enumerate(folders['videos'], 1):
            print(f"\n{i}. {folder['name']}")
            print(f"   Path: {folder['path']}")

            # Count files
            video_files = get_video_files(folder['path'])
            print(f"   Files: {len(video_files)} videos")

            # Show sample
            if video_files:
                sample = video_files[0]
                print(f"   Sample: {os.path.basename(sample)}")
    else:
        print("\n⚠️ No video datasets found")

    print("\n" + "=" * 70)
    print("🎵 MUSIC DATASETS")
    print("=" * 70)

    if folders['music']:
        for i, folder in enumerate(folders['music'], 1):
            print(f"\n{i}. {folder['name']}")
            print(f"   Path: {folder['path']}")

            # Count files
            music_files = get_music_files(folder['path'])
            print(f"   Files: {len(music_files)} tracks")

            # Show sample
            if music_files:
                sample = music_files[0]
                print(f"   Sample: {os.path.basename(sample)}")
    else:
        print("\n⚠️ No music datasets found")

    print("\n" + "=" * 70)
