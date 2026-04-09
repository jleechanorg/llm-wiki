"""Campaign upgrade planning block helpers."""

from __future__ import annotations

import json
from typing import Any

from mvp_site import campaign_divine, constants, logging_util


def normalize_planning_block_choices(  # noqa: PLR0912
    planning_block: dict[str, Any] | str | None,
    *,
    log_prefix: str | None = None,
) -> dict[str, Any]:
    """Normalize planning_block into a dict with list-format choices."""
    max_choice_id_collision_retries = 1000
    if isinstance(planning_block, str):
        try:
            planning_block = (
                json.loads(planning_block) if planning_block.strip() else {}
            )
        except (json.JSONDecodeError, TypeError):
            planning_block = {}
    elif planning_block is None:
        planning_block = {}

    if not isinstance(planning_block, dict):
        planning_block = {}

    existing_choices = planning_block.get("choices")
    converted_choices: list[dict[str, Any]] = []
    seen_ids: set[str] = set()

    source_choices: list[tuple[str | None, dict[str, Any]]] = []
    if isinstance(existing_choices, dict):
        for key, choice in existing_choices.items():
            if isinstance(choice, dict):
                source_choices.append((str(key), dict(choice)))
            elif isinstance(choice, str) and choice.strip():
                # Handle string-valued choices (e.g., {"attack": "Strike the enemy"})
                # Convert to dict format with text and description fields
                normalized_choice = {"text": choice.strip(), "description": choice.strip()}
                source_choices.append((str(key), normalized_choice))
    elif isinstance(existing_choices, list):
        for choice in existing_choices:
            if isinstance(choice, dict):
                source_choices.append((None, dict(choice)))

    for idx, (fallback_key, choice) in enumerate(source_choices):
        choice_id = choice.get("id", "")
        if not isinstance(choice_id, str):
            choice_id = "" if choice_id is None else str(choice_id)
        choice_id = choice_id.strip()
        if not choice_id and fallback_key:
            choice_id = fallback_key.strip()
        if not choice_id:
            text = choice.get("text", "")
            if not isinstance(text, str):
                text = "" if text is None else str(text)
            choice_id = text.lower().replace(" ", "_")[:30] if text else f"choice_{idx}"

        if choice_id in seen_ids:
            original_id = choice_id
            suffix = 1
            while choice_id in seen_ids and suffix < max_choice_id_collision_retries:
                choice_id = f"{original_id}_{suffix}"
                suffix += 1
            if choice_id in seen_ids:
                raise ValueError(
                    f"Choice ID collision limit exceeded for '{original_id}'"
                )
            logging_util.warning(
                f"Choice ID collision detected: '{original_id}' -> '{choice_id}' (index {idx})"
            )

        seen_ids.add(choice_id)
        choice["id"] = choice_id
        converted_choices.append(choice)

    planning_block["choices"] = converted_choices
    if log_prefix and isinstance(existing_choices, dict):
        logging_util.info(
            f"{log_prefix}: Converted {len(existing_choices)} dict-format choices to list format"
        )

    return planning_block


def inject_campaign_upgrade_choice_if_needed(
    planning_block: dict[str, Any] | str | None,
    game_state_dict: dict[str, Any],
    agent_mode: str | None,
) -> dict[str, Any] | str | None:
    """
    Server-side enforcement of campaign upgrade choice in planning_block.

    When CampaignUpgradeAgent is selected, the LLM should present a choice to
    begin the ascension ceremony. If missing, inject a minimal choice so the
    player can proceed.
    """
    if agent_mode != constants.MODE_CAMPAIGN_UPGRADE:
        return planning_block

    custom_state_raw = game_state_dict.get("custom_campaign_state")
    custom_state = custom_state_raw if isinstance(custom_state_raw, dict) else {}
    player_data_raw = game_state_dict.get("player_character_data")
    player_data = player_data_raw if isinstance(player_data_raw, dict) else {}
    upgrade_type = campaign_divine.get_pending_upgrade_type(custom_state, player_data)

    if upgrade_type == "multiverse":
        choice_text = "Begin Sovereign Ascension"
        choice_description = "Initiate the sovereign/multiverse ascension ceremony."
    elif upgrade_type == "divine":
        choice_text = "Begin Divine Ascension"
        choice_description = "Initiate the divine ascension ceremony."
    else:
        # No upgrade actually available (semantic routing can still select this agent)
        return planning_block

    planning_block = normalize_planning_block_choices(planning_block)

    choices = planning_block["choices"]

    def _find_choice_index_by_id(target_id: str) -> int | None:
        for idx, existing in enumerate(choices):
            if isinstance(existing, dict) and existing.get("id") == target_id:
                return idx
        return None

    # Avoid duplicate injection if a matching choice already exists by text
    matching_index = None
    for idx, existing_choice in enumerate(choices):
        if isinstance(existing_choice, dict):
            existing_text = existing_choice.get("text")
            if not isinstance(existing_text, str):
                existing_text = "" if existing_text is None else str(existing_text)
            existing_text = existing_text.strip().lower()
            if existing_text == choice_text.lower():
                matching_index = idx
                break

    if matching_index is not None:
        upgraded_choice = choices[matching_index]
        if isinstance(upgraded_choice, dict):
            # Remove any existing choice with id "upgrade_campaign" to prevent duplicates
            existing_upgrade_idx = _find_choice_index_by_id("upgrade_campaign")
            if existing_upgrade_idx is not None and existing_upgrade_idx != matching_index:
                choices.pop(existing_upgrade_idx)
            upgraded_choice["id"] = "upgrade_campaign"
        return planning_block

    if _find_choice_index_by_id("upgrade_campaign") is None:
        logging_util.info(
            "⬆️ SERVER_CAMPAIGN_UPGRADE_INJECTION: Injecting upgrade_campaign choice"
        )
        choices.append({
            "id": "upgrade_campaign",
            "text": choice_text,
            "description": choice_description,
            "risk_level": "safe",
        })

    if "thinking" not in planning_block:
        planning_block["thinking"] = (
            "A campaign ascension is available. "
            "The player can begin the upgrade ceremony."
        )

    return normalize_choices_to_array(planning_block)


def normalize_choices_to_array(
    planning_block: dict[str, Any],
) -> dict[str, Any]:
    """Convert dict-format choices to array-of-objects with 'id' field."""
    choices = planning_block.get("choices")
    if isinstance(choices, dict):
        planning_block["choices"] = [
            {**value, "id": key}
            for key, value in choices.items()
            if isinstance(value, dict)
        ]
    elif choices is None:
        pass
    return planning_block
