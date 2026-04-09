"""Input validation utilities for production launch."""

import json
import re
import unicodedata
from typing import Any

# Maximum request sizes
DEFAULT_MAX_REQUEST_SIZE = 1024 * 1024  # 1MB
DEFAULT_MAX_ARRAY_SIZE = 1000


def validate_campaign_id(campaign_id: str) -> bool:
    """Validate campaign ID format.

    Args:
        campaign_id: The campaign ID to validate

    Returns:
        True if valid, False otherwise
    """
    if not campaign_id:
        return False

    # Check for UUID format
    uuid_pattern = r"^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$"
    if re.match(uuid_pattern, campaign_id, re.IGNORECASE):
        return True

    # Alphanumeric with dash/underscore only; max 128 chars to prevent abuse
    return len(campaign_id) <= 128 and bool(re.match(r"^[a-zA-Z0-9_-]+$", campaign_id))


def validate_user_id(user_id: str) -> bool:
    """Validate user ID format.

    Args:
        user_id: The user ID to validate

    Returns:
        True if valid, False otherwise
    """
    if not user_id:
        return False

    # User IDs can be UUIDs or alphanumeric
    uuid_pattern = r"^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$"
    if re.match(uuid_pattern, user_id, re.IGNORECASE):
        return True

    # Alphanumeric with dash/underscore only; max 128 chars to prevent abuse
    return len(user_id) <= 128 and bool(re.match(r"^[a-zA-Z0-9_-]+$", user_id))


def sanitize_string(value: str, max_length: int = 10000) -> str:
    """Sanitize a string value.

    Args:
        value: The string to sanitize
        max_length: Maximum allowed length

    Returns:
        Sanitized string
    """
    if not value:
        return ""

    # Truncate to max length
    result = value[:max_length]

    # Remove null bytes
    result = result.replace("\x00", "")

    # Normalize unicode (NFC normalization)
    return unicodedata.normalize("NFC", result)


def sanitize_user_input(value: str) -> str:
    """Sanitize user input: truncate to 50K chars, strip null bytes, normalize unicode.

    Does not perform HTML escaping or injection-pattern filtering — those are
    handled at the rendering/storage layer as appropriate for each context.

    Args:
        value: The user input to sanitize

    Returns:
        Sanitized string
    """
    if not value:
        return ""

    # Apply basic sanitization (truncate, null bytes, unicode normalization)
    return sanitize_string(value, max_length=50000)


def validate_request_size(data: Any, max_size: int = DEFAULT_MAX_REQUEST_SIZE) -> bool:
    """Validate request data size.

    Args:
        data: The data to check
        max_size: Maximum size in bytes

    Returns:
        True if within limits
    """
    try:
        data_str = json.dumps(data)
        size = len(data_str.encode("utf-8"))
        return size <= max_size
    except (TypeError, ValueError):
        return False


def validate_array_size(arr: list, max_size: int = DEFAULT_MAX_ARRAY_SIZE) -> bool:
    """Validate array size.

    Args:
        arr: The array to check
        max_size: Maximum number of elements

    Returns:
        True if within limits
    """
    return isinstance(arr, list) and len(arr) <= max_size


def validate_export_format(export_format: str) -> bool:
    """Validate export format parameter.

    Args:
        export_format: The export format to validate

    Returns:
        True if valid format
    """
    if not export_format or not isinstance(export_format, str):
        return False
    valid_formats = {"txt", "pdf", "json", "docx"}
    return export_format.lower() in valid_formats
