"""Schema strictness and schema-coverage guard tests."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path


def _load_schema() -> dict:
    repo_root = Path(__file__).resolve().parents[2]
    schema_path = repo_root / "mvp_site" / "schemas" / "game_state.schema.json"
    return json.loads(schema_path.read_text())


def test_routing_objects_have_explicit_properties() -> None:
    schema = _load_schema()
    defs = schema["$defs"]

    encounter_props = defs["EncounterState"]["properties"]
    rewards_props = defs["RewardsPending"]["properties"]
    custom_props = defs["CustomCampaignState"]["properties"]
    combat_props = defs["CombatState"]["properties"]

    assert "encounter_completed" in encounter_props
    assert "encounter_summary" in encounter_props
    assert "rewards_processed" in encounter_props

    assert "processed" in rewards_props
    assert "level_up_available" in rewards_props

    assert "level_up_pending" in custom_props
    assert "level_up_in_progress" in custom_props
    assert "character_creation_completed" in custom_props
    assert "success_streak" in custom_props
    assert "core_memories" in custom_props
    assert "world_events" in custom_props
    assert "last_location" in custom_props
    assert "last_story_mode_sequence_id" in custom_props

    assert "rewards_processed" in combat_props
    assert "budget_warnings_shown" in custom_props
    assert "player_character_data_extras" in custom_props


def test_top_level_state_uses_structured_refs() -> None:
    schema = _load_schema()
    props = schema["properties"]

    assert props["encounter_state"]["$ref"] == "#/$defs/EncounterState"
    assert props["rewards_pending"]["$ref"] == "#/$defs/RewardsPending"
    assert props["custom_campaign_state"]["$ref"] == "#/$defs/CustomCampaignState"
    assert props["combat_state"]["$ref"] == "#/$defs/CombatState"


def test_living_world_top_level_fields_are_canonical() -> None:
    schema = _load_schema()
    props = schema["properties"]

    assert "world_events" in props
    assert "faction_updates" in props
    assert "time_events" in props
    assert "rumors" in props
    assert "scene_event" in props
    assert "complications" in props


def test_canonical_equipment_slots_include_prompt_slots() -> None:
    schema = _load_schema()
    equipped_props = schema["$defs"]["Character"]["properties"]["equipped_items"][
        "properties"
    ]

    assert "shoulders" in equipped_props
    assert "chest" in equipped_props
    assert "waist" in equipped_props
    assert "legs" in equipped_props


def test_schema_coverage_script_reports_no_missing_routing_paths() -> None:
    repo_root = Path(__file__).resolve().parents[2]
    script_path = repo_root / "scripts" / "check_schema_coverage.py"

    result = subprocess.run(
        [sys.executable, str(script_path), "--report-json", "--fail-under", "0"],
        cwd=repo_root,
        capture_output=True,
        text=True,
        check=False,
    )

    assert result.returncode == 0, result.stderr or result.stdout
    payload = json.loads(result.stdout)
    missing_paths = set(payload["missing_paths"])
    code_paths = set(payload["code_paths"])

    assert "combat_state.rewards_processed" in code_paths
    assert "encounter_state.encounter_completed" in code_paths
    assert "rewards_pending.level_up_available" in code_paths
    assert "custom_campaign_state.level_up_pending" in code_paths
    assert "custom_campaign_state.last_location" in code_paths
    assert "custom_campaign_state.last_story_mode_sequence_id" in code_paths

    assert "combat_state.rewards_processed" not in missing_paths
    assert "encounter_state.encounter_completed" not in missing_paths
    assert "rewards_pending.level_up_available" not in missing_paths
    assert "custom_campaign_state.level_up_pending" not in missing_paths
    assert "custom_campaign_state.last_location" not in missing_paths
    assert "custom_campaign_state.last_story_mode_sequence_id" not in missing_paths


def test_schema_coverage_script_required_path_mode() -> None:
    repo_root = Path(__file__).resolve().parents[2]
    script_path = repo_root / "scripts" / "check_schema_coverage.py"

    result = subprocess.run(
        [
            sys.executable,
            str(script_path),
            "--report-json",
            "--fail-under",
            "0",
            "--required-path",
            "combat_state.rewards_processed",
            "--required-path",
            "encounter_state.encounter_completed",
            "--required-path",
            "rewards_pending.level_up_available",
            "--required-path",
            "custom_campaign_state.level_up_pending",
            "--required-path",
            "custom_campaign_state.last_location",
            "--required-path",
            "custom_campaign_state.last_story_mode_sequence_id",
        ],
        cwd=repo_root,
        capture_output=True,
        text=True,
        check=False,
    )

    assert result.returncode == 0, result.stderr or result.stdout
    payload = json.loads(result.stdout)
    assert payload["missing_required_paths"] == []


def test_schema_coverage_script_reconciliation_mode_passes_known_discovered() -> None:
    repo_root = Path(__file__).resolve().parents[2]
    script_path = repo_root / "scripts" / "check_schema_coverage.py"

    result = subprocess.run(
        [
            sys.executable,
            str(script_path),
            "--report-json",
            "--fail-under",
            "0",
            "--discovered-path",
            "custom_campaign_state.last_location",
            "--discovered-path",
            "custom_campaign_state.last_story_mode_sequence_id",
        ],
        cwd=repo_root,
        capture_output=True,
        text=True,
        check=False,
    )

    assert result.returncode == 0, result.stderr or result.stdout
    payload = json.loads(result.stdout)
    assert payload["discovered_unreconciled"] == []
    promoted = set(payload["discovered_promoted"])
    assert "custom_campaign_state.last_location" in promoted
    assert "custom_campaign_state.last_story_mode_sequence_id" in promoted


def test_schema_coverage_script_reconciliation_mode_fails_unreconciled_discovered() -> None:
    repo_root = Path(__file__).resolve().parents[2]
    script_path = repo_root / "scripts" / "check_schema_coverage.py"

    result = subprocess.run(
        [
            sys.executable,
            str(script_path),
            "--report-json",
            "--fail-under",
            "0",
            "--discovered-path",
            "custom_campaign_state.__nonexistent_reconciliation_probe",
        ],
        cwd=repo_root,
        capture_output=True,
        text=True,
        check=False,
    )

    assert result.returncode != 0
    payload = json.loads(result.stdout)
    assert payload["discovered_unreconciled"] == [
        "custom_campaign_state.__nonexistent_reconciliation_probe"
    ]
