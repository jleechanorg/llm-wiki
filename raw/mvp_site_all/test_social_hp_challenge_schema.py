import importlib

from mvp_site import game_state, narrative_response_schema
from mvp_site.narrative_response_schema import NarrativeResponse
from mvp_site.schemas import validation as schema_validation


def _base_social_hp() -> dict:
    return {
        "npc_name": "Empress Sariel",
        "objective": "Demand her surrender",
        "social_hp": 42,
        "social_hp_max": 45,
        "successes": 3,
        "successes_needed": 5,
        "status": "WAVERING",
        "skill_used": "Intimidation",
        "roll_result": 28,
        "roll_dc": 25,
        "social_hp_damage": 2,
    }


def test_social_hp_challenge_normalizes_request_severity_and_resistance():
    payload = _base_social_hp()
    payload["request_severity"] = "Submission"
    payload["resistance_shown"] = "Her jaw tightens as she steps back."

    response = NarrativeResponse(narrative="n", social_hp_challenge=payload)

    assert response.social_hp_challenge["request_severity"] == "submission"
    assert (
        response.social_hp_challenge["resistance_shown"]
        == "Her jaw tightens as she steps back."
    )


def test_social_hp_challenge_invalid_request_severity_defaults_to_information():
    payload = _base_social_hp()
    payload["request_severity"] = "extortion"

    response = NarrativeResponse(narrative="n", social_hp_challenge=payload)

    assert response.social_hp_challenge["request_severity"] == "information"


def test_game_state_social_hp_enums_are_schema_derived(monkeypatch):
    monkeypatch.setattr(
        schema_validation, "get_social_hp_request_severity_values", lambda: {"favor"}
    )
    monkeypatch.setattr(
        schema_validation, "get_social_hp_skill_values", lambda: {"Insight"}
    )

    reloaded_game_state = importlib.reload(game_state)
    try:
        assert {"favor"} == reloaded_game_state._VALID_SOCIAL_REQUEST_SEVERITY
        assert {"Insight"} == reloaded_game_state._VALID_SOCIAL_SKILLS
    finally:
        importlib.reload(game_state)


def test_narrative_response_social_hp_enums_are_schema_derived(monkeypatch):
    monkeypatch.setattr(
        schema_validation, "get_social_hp_request_severity_values", lambda: {"favor"}
    )
    monkeypatch.setattr(
        schema_validation, "get_social_hp_skill_values", lambda: {"Insight"}
    )

    reloaded_schema = importlib.reload(narrative_response_schema)
    try:
        assert {"favor"} == reloaded_schema.VALID_SOCIAL_HP_REQUEST_SEVERITY
        assert {"Insight"} == reloaded_schema.VALID_SOCIAL_SKILLS
    finally:
        importlib.reload(narrative_response_schema)
