"""Agent routing tests that exercise schema-validated state updates."""

from __future__ import annotations

from mvp_site.agents import CharacterCreationAgent, RewardsAgent
from mvp_site.game_state import GameState
from mvp_site.schemas.validation import sanitize_state_updates_overlay


def _base_state_kwargs() -> dict[str, object]:
    return {
        "game_state_version": 2,
        "session_id": "routing-test-session",
        "turn_number": 10,
    }


def test_rewards_agent_matches_after_overlay_sanitization() -> None:
    updates = {
        "combat_state": {
            "combat_phase": "ended",
            "combat_summary": {"xp_awarded": 120},
            "rewards_processed": False,
        }
    }
    sanitized, errors = sanitize_state_updates_overlay(updates)

    assert errors == [], errors

    state = GameState(**_base_state_kwargs(), combat_state=sanitized["combat_state"])
    assert RewardsAgent.matches_game_state(state) is True


def test_rewards_agent_matches_encounter_and_rewards_pending_fields() -> None:
    updates = {
        "encounter_state": {
            "encounter_completed": True,
            "encounter_summary": {"xp_awarded": 50},
            "rewards_processed": False,
        },
        "rewards_pending": {
            "source": "encounter",
            "xp": 50,
            "processed": False,
            "level_up_available": True,
        },
    }
    sanitized, errors = sanitize_state_updates_overlay(updates)

    assert errors == [], errors

    state = GameState(
        **_base_state_kwargs(),
        encounter_state=sanitized["encounter_state"],
        rewards_pending=sanitized["rewards_pending"],
    )
    assert RewardsAgent.matches_game_state(state) is True


def test_character_creation_agent_matches_level_up_flags_after_sanitization() -> None:
    updates = {
        "custom_campaign_state": {
            "character_creation_completed": False,
            "level_up_pending": True,
            "level_up_in_progress": True,
        },
        "rewards_pending": {
            "level_up_available": True,
            "processed": False,
        },
    }
    sanitized, errors = sanitize_state_updates_overlay(updates)

    assert errors == [], errors

    state = GameState(
        **_base_state_kwargs(),
        custom_campaign_state=sanitized["custom_campaign_state"],
        rewards_pending=sanitized["rewards_pending"],
    )
    assert CharacterCreationAgent.matches_game_state(state) is True
