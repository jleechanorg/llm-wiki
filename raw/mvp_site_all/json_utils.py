"""
JSON parsing utilities for robust extraction and validation.

This module provides tools for extracting valid JSON from text that may contain
artifacts like code execution output, logs, or markdown formatting.
"""

import json
from collections.abc import Callable
from typing import Any

from mvp_site import logging_util


def find_matching_brace(
    text: str, start: int, open_char: str = "{", close_char: str = "}"
) -> int:
    """
    Find the index of the closing brace/bracket that matches the opening one at start.

    Args:
        text: The text to search in
        start: Index of the opening brace/bracket
        open_char: Opening character (default: "{")
        close_char: Closing character (default: "}")

    Returns:
        Index of the matching closing character, or -1 if not found.
    """
    if start >= len(text) or text[start] != open_char:
        return -1

    depth = 0
    in_string = False
    escape_next = False

    for i in range(start, len(text)):
        char = text[i]

        if escape_next:
            escape_next = False
            continue

        if char == "\\":
            escape_next = True
        elif char == '"':
            in_string = not in_string
        elif not in_string:
            if char == open_char:
                depth += 1
            elif char == close_char:
                depth -= 1
                if depth == 0:
                    return i

    # No matching brace found
    return -1


def extract_best_json(
    text: str,
    scoring_func: Callable[[Any], float] | None = None,
    log_selection: bool = True,
) -> Any | None:
    """
    Scan text for all valid JSON objects/arrays and return the best candidate.

    This function is useful for parsing LLM responses that may contain:
    - Code execution artifacts
    - Markdown code blocks
    - Logging output
    - Multiple JSON fragments

    Args:
        text: The text to search for JSON
        scoring_func: Optional custom scoring function. Takes parsed JSON object,
                     returns score (higher is better). If None, uses default scoring:
                     - Objects with "narrative" key: +500 points
                     - Objects with "god_mode_response" key: +500 points
                     - Size: +1 point per 100 chars
        log_selection: Whether to log the selected candidate (default: True)

    Returns:
        The best JSON candidate (dict, list, or other JSON type), or None if no valid JSON found.

    Examples:
        >>> extract_best_json('{"a": 1}')
        {'a': 1}

        >>> extract_best_json('[1, 2, 3]')
        [1, 2, 3]

        >>> text = 'Debug log\\n{"narrative": "story", "value": 42}\\n{"value": 123}'
        >>> extract_best_json(text)
        {'narrative': 'story', 'value': 42}  # Prioritizes object with "narrative"

        >>> # Custom scoring
        >>> def score_by_size(obj): return len(json.dumps(obj))
        >>> extract_best_json(text, scoring_func=score_by_size)
        {'narrative': 'story', 'value': 42}  # Largest object
    """
    candidates = []
    i = 0
    text_len = len(text)

    # Phase 1: Extract all valid JSON objects/arrays
    while i < text_len:
        char = text[i]
        if char == "{" or char == "[":
            open_char = char
            close_char = "}" if char == "{" else "]"
            end_pos = find_matching_brace(text, i, open_char, close_char)

            if end_pos != -1:
                chunk = text[i : end_pos + 1]
                try:
                    obj = json.loads(chunk)
                    candidates.append(obj)
                    # Skip to end of this object to avoid parsing nested objects as top-level candidates
                    i = end_pos
                except json.JSONDecodeError:
                    # If parsing fails (e.g. invalid content inside), continue scanning
                    pass
        i += 1

    if not candidates:
        return None

    # Phase 2: Score candidates
    if scoring_func is None:
        # Default scoring for narrative response objects
        def default_scoring(obj: Any) -> float:
            score = 0.0
            # Unwrap list for inspection
            inspect_obj = obj[0] if isinstance(obj, list) and len(obj) > 0 else obj

            # Signal 1: 'narrative' key (strong signal for story responses)
            if isinstance(inspect_obj, dict) and "narrative" in inspect_obj:
                score += 500

            # Signal 2: 'god_mode_response' key (admin responses)
            if isinstance(inspect_obj, dict) and "god_mode_response" in inspect_obj:
                score += 500

            # Signal 3: Size (1 point per 100 chars of string repr)
            score += len(json.dumps(obj)) / 100

            return score

        scoring_func = default_scoring

    best_candidate = None
    best_score = -1.0

    for obj in candidates:
        score = scoring_func(obj)
        if score > best_score:
            best_score = score
            best_candidate = obj

    if best_candidate is not None and log_selection:
        # Debug log for selected candidate
        preview = str(best_candidate)[:200]
        logging_util.info(
            f"Selected best JSON candidate (score={best_score:.1f}): {preview}..."
        )

    return best_candidate
