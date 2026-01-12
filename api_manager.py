"""
API Key Management Module
Handles Google Gemini API key rotation and persistence
"""

import os
import json
import random
from config import GOOGLE_GEMINI_API_KEYS, API_KEY_FILE

# Global state for API key rotation
current_api_key_index = None
api_keys = GOOGLE_GEMINI_API_KEYS.copy()


def initialize_api_keys():
    """Initialize API key rotation with random starting position"""
    global current_api_key_index
    if current_api_key_index is None:
        current_api_key_index = random.randint(0, len(api_keys) - 1)


def load_api_key():
    """
    Load the last used API key from file or return a random key

    Returns:
        str: Google Gemini API key
    """
    global current_api_key_index

    initialize_api_keys()

    # Try to load last used key index from file
    if os.path.exists(API_KEY_FILE):
        try:
            with open(API_KEY_FILE, 'r') as f:
                data = json.load(f)
                saved_index = data.get('index', current_api_key_index)
                if 0 <= saved_index < len(api_keys):
                    current_api_key_index = saved_index
        except:
            pass

    return api_keys[current_api_key_index]


def get_next_api_key():
    """
    Rotate to the next API key in the list

    Returns:
        str: Next Google Gemini API key
    """
    global current_api_key_index

    initialize_api_keys()

    # Move to next key
    current_api_key_index = (current_api_key_index + 1) % len(api_keys)

    # Save the new index
    save_api_key()

    return api_keys[current_api_key_index]


def get_current_api_key():
    """
    Get the current API key without rotation

    Returns:
        str: Current Google Gemini API key
    """
    initialize_api_keys()
    return api_keys[current_api_key_index]


def get_api_rotation_status():
    """
    Get current API key rotation status

    Returns:
        dict: Status information with masked key
    """
    initialize_api_keys()

    current_key = api_keys[current_api_key_index]
    masked_key = current_key[:10] + "..." + current_key[-4:]

    return {
        "index": current_api_key_index + 1,
        "total": len(api_keys),
        "masked_key": masked_key
    }


def reset_api_key_rotation():
    """Reset API key rotation to a random position"""
    global current_api_key_index
    current_api_key_index = random.randint(0, len(api_keys) - 1)
    save_api_key()
    return get_api_rotation_status()


def save_api_key():
    """Save current API key index to file for persistence"""
    try:
        with open(API_KEY_FILE, 'w') as f:
            json.dump({'index': current_api_key_index}, f)
    except Exception as e:
        print(f"Warning: Could not save API key index: {e}")


def is_quota_error(error_message):
    """
    Check if error message indicates quota or rate limit issue

    Args:
        error_message (str): Error message to check

    Returns:
        bool: True if quota/rate limit error
    """
    if not error_message:
        return False

    error_lower = str(error_message).lower()
    quota_indicators = [
        "quota",
        "429",
        "resource_exhausted",
        "rate_limit",
        "too many requests"
    ]

    return any(indicator in error_lower for indicator in quota_indicators)


def is_auth_error(error_message):
    """
    Check if error message indicates authentication issue

    Args:
        error_message (str): Error message to check

    Returns:
        bool: True if authentication error
    """
    if not error_message:
        return False

    error_lower = str(error_message).lower()
    auth_indicators = [
        "api key",
        "authentication",
        "unauthorized",
        "invalid key",
        "permission denied"
    ]

    return any(indicator in error_lower for indicator in auth_indicators)


def should_rotate_key(error_message):
    """
    Determine if API key should be rotated based on error

    Args:
        error_message (str): Error message to analyze

    Returns:
        bool: True if key should be rotated
    """
    return is_quota_error(error_message) or is_auth_error(error_message)


# Initialize on module import
initialize_api_keys()
