"""Tests for provably fair dice roll system.

TDD: Written before implementation - tests the full cryptographic chain.

Integration tests for gemini_provider/gemini_code_execution require the
google-generativeai SDK (available in CI). Pure function tests run anywhere.
"""

import hashlib
import importlib.util
import pathlib
import re
import sys
from unittest.mock import MagicMock

from mvp_site import dice_provably_fair

# Mock google SDK before importing modules that depend on it.
# sys.modules.setdefault only sets if not already present, so real SDK wins in CI.
sys.modules.setdefault("google", MagicMock())
sys.modules.setdefault("google.genai", MagicMock())
sys.modules.setdefault("google.genai.types", MagicMock())
sys.modules.setdefault("google.api_core", MagicMock())
sys.modules.setdefault("google.api_core.exceptions", MagicMock())

# Import gemini_code_execution directly (not via llm_providers/__init__ which
# imports all providers and triggers google.genai dependency chain).
_gce_path = pathlib.Path(__file__).parent.parent / "llm_providers" / "gemini_code_execution.py"
_gce_spec = importlib.util.spec_from_file_location("mvp_site.llm_providers.gemini_code_execution", _gce_path)
_gce_mod = importlib.util.module_from_spec(_gce_spec)
_gce_spec.loader.exec_module(_gce_mod)  # type: ignore[union-attr]
extract_code_execution_evidence = _gce_mod.extract_code_execution_evidence

from mvp_site.llm_providers.gemini_provider import apply_code_execution_system_instruction  # noqa: E402

# Gemini 3 is required to trigger code_execution strategy
_GEMINI3_MODEL = "gemini-3-flash"


# ===================================================================
# Pure function tests (no external dependencies)
# ===================================================================


def test_generate_server_seed_is_64_hex_chars():
    seed = dice_provably_fair.generate_server_seed()
    assert len(seed) == 64
    int(seed, 16)  # ValueError if not valid hex


def test_generate_server_seed_is_unique():
    seeds = {dice_provably_fair.generate_server_seed() for _ in range(10)}
    assert len(seeds) == 10


def test_compute_commitment_is_sha256():
    seed = "abc123"
    expected = hashlib.sha256(b"abc123").hexdigest()
    assert dice_provably_fair.compute_commitment(seed) == expected


def test_compute_commitment_is_deterministic():
    seed = dice_provably_fair.generate_server_seed()
    assert dice_provably_fair.compute_commitment(seed) == dice_provably_fair.compute_commitment(seed)


def test_verify_commitment_valid():
    seed = dice_provably_fair.generate_server_seed()
    commitment = dice_provably_fair.compute_commitment(seed)
    assert dice_provably_fair.verify_commitment(seed, commitment)


def test_verify_commitment_rejects_wrong_seed():
    seed = dice_provably_fair.generate_server_seed()
    commitment = dice_provably_fair.compute_commitment(seed)
    assert not dice_provably_fair.verify_commitment("wrong_seed", commitment)


def test_verify_commitment_rejects_tampered_commitment():
    seed = dice_provably_fair.generate_server_seed()
    assert not dice_provably_fair.verify_commitment(seed, "0" * 64)


def test_inject_seed_replaces_time_ns():
    server_seed = "a" * 64
    prompt = "import random, time\nrandom.seed(time.time_ns())\nresult = random.randint(1, 20)"
    result = dice_provably_fair.inject_seed_into_prompt(prompt, server_seed)
    assert "time.time_ns()" not in result
    assert f"random.seed('{server_seed}')" in result


def test_inject_seed_replaces_all_occurrences_with_unique_seeds():
    """Each occurrence gets a different seed so multiple rolls in one turn differ."""
    server_seed = "b" * 64
    prompt = "random.seed(time.time_ns())\n...\nrandom.seed(time.time_ns())"
    result = dice_provably_fair.inject_seed_into_prompt(prompt, server_seed)
    assert result.count("time.time_ns()") == 0
    # Extract both seeds from result - they must differ
    seeds = re.findall(r"random\.seed\('([a-fA-F0-9]{64})'\)", result)
    assert len(seeds) == 2
    assert seeds[0] != seeds[1]
    assert dice_provably_fair.is_valid_injected_seed(seeds[0], server_seed)
    assert dice_provably_fair.is_valid_injected_seed(seeds[1], server_seed)


def test_inject_seed_leaves_other_content_unchanged():
    server_seed = "c" * 64
    prompt = (
        "import json, random, time\n"
        "random.seed(time.time_ns())\n"
        "result = random.randint(1, 20)\n"
        "print(json.dumps({'roll': result}))"
    )
    result = dice_provably_fair.inject_seed_into_prompt(prompt, server_seed)
    assert "import json, random, time" in result
    assert "random.randint(1, 20)" in result


def test_verify_seed_in_executed_code_found():
    server_seed = "a" * 64
    code = [f"import random\nrandom.seed('{server_seed}')\nprint(random.randint(1,20))"]
    assert dice_provably_fair.verify_seed_in_executed_code(code, server_seed)


def test_verify_seed_in_executed_code_multiple_parts():
    server_seed = "d" * 64
    code = ["import random", f"random.seed('{server_seed}')\nresult = random.randint(1,6)"]
    assert dice_provably_fair.verify_seed_in_executed_code(code, server_seed)


def test_verify_seed_in_executed_code_not_found():
    server_seed = "a" * 64
    other_seed = "b" * 64
    code = [f"random.seed('{other_seed}')"]
    assert not dice_provably_fair.verify_seed_in_executed_code(code, server_seed)


def test_verify_seed_in_executed_code_empty():
    assert not dice_provably_fair.verify_seed_in_executed_code([], "a" * 64)


def test_extract_seed_from_executed_code_found():
    server_seed = "a" * 64
    code = [f"import random\nrandom.seed('{server_seed}')\nresult = random.randint(1, 20)"]
    assert dice_provably_fair.extract_seed_from_executed_code(code) == server_seed


def test_extract_seed_from_executed_code_not_found():
    code = ["import random\nrandom.seed(time.time_ns())\nresult = random.randint(1, 20)"]
    assert dice_provably_fair.extract_seed_from_executed_code(code) is None


def test_extract_seed_from_executed_code_empty():
    assert dice_provably_fair.extract_seed_from_executed_code([]) is None


def test_extract_seed_ignores_pattern_in_comment_lines():
    """Seed pattern inside a # comment line must not be extracted as a real seed."""
    seed_in_comment = "b" * 64
    code = [f"# Example: random.seed('{seed_in_comment}')\nrandom.seed(time.time_ns())"]
    assert dice_provably_fair.extract_seed_from_executed_code(code) is None


def test_extract_seed_ignores_pattern_in_string_literal():
    """Seed pattern in a string literal must not be extracted (AST prevents false positive)."""
    server_seed = "a" * 64
    fake_in_string = "b" * 64
    code = [
        f'example = "random.seed(\'{fake_in_string}\')"  # doc string\n'
        f"random.seed('{server_seed}')\n"
        "roll = random.randint(1, 20)"
    ]
    # AST extracts from actual call only, not string literal
    assert dice_provably_fair.extract_seed_from_executed_code(code) == server_seed


def test_is_valid_injected_seed_accepts_base_and_derived():
    """is_valid_injected_seed accepts base seed and derived seeds."""
    base = "c" * 64
    assert dice_provably_fair.is_valid_injected_seed(base, base)
    derived_1 = hashlib.sha256((base + "\n1").encode()).hexdigest()
    assert dice_provably_fair.is_valid_injected_seed(derived_1, base)
    assert not dice_provably_fair.is_valid_injected_seed("x" * 64, base)


def test_full_provably_fair_chain():
    """End-to-end: generate → commit → inject → verify → extract → validate."""
    server_seed = dice_provably_fair.generate_server_seed()
    commitment = dice_provably_fair.compute_commitment(server_seed)

    prompt = "import random, time\nrandom.seed(time.time_ns())\nroll = random.randint(1, 20)"
    injected = dice_provably_fair.inject_seed_into_prompt(prompt, server_seed)

    # Simulate what Gemini executes and stores in debug_info.executed_code
    executed_code = [injected]

    assert dice_provably_fair.verify_seed_in_executed_code(executed_code, server_seed)
    extracted = dice_provably_fair.extract_seed_from_executed_code(executed_code)
    assert extracted == server_seed
    assert dice_provably_fair.verify_commitment(extracted, commitment)

    # Attacker with wrong seed fails commitment check
    assert not dice_provably_fair.verify_commitment("fake" * 16, commitment)


# ===================================================================
# Integration tests: apply_code_execution_system_instruction
# ===================================================================


def test_apply_seed_to_system_instruction_injects_seed():
    """apply_code_execution_system_instruction with server_seed replaces time.time_ns()."""
    server_seed = "e" * 64
    result = apply_code_execution_system_instruction(
        system_instruction_text=None,
        model_name=_GEMINI3_MODEL,
        server_seed=server_seed,
    )
    assert "time.time_ns()" not in result
    assert f"random.seed('{server_seed}')" in result


def test_apply_seed_to_system_instruction_no_seed_keeps_time_ns():
    """apply_code_execution_system_instruction without server_seed keeps time.time_ns()."""
    result = apply_code_execution_system_instruction(
        system_instruction_text=None,
        model_name=_GEMINI3_MODEL,
        server_seed=None,
    )
    assert "time.time_ns()" in result


# ===================================================================
# Integration tests: extract_code_execution_evidence
# ===================================================================


def _make_mock_response(code: str, stdout: str) -> MagicMock:
    """Build a minimal mock Gemini response with one code + one result part."""
    mock_exec = MagicMock()
    mock_exec.code = code

    mock_result = MagicMock()
    mock_result.output = stdout

    part_exec = MagicMock()
    part_exec.executable_code = mock_exec
    part_exec.code_execution_result = None

    part_result = MagicMock()
    part_result.executable_code = None
    part_result.code_execution_result = mock_result

    mock_content = MagicMock()
    mock_content.parts = [part_exec, part_result]
    mock_candidate = MagicMock()
    mock_candidate.content = mock_content

    mock_response = MagicMock()
    mock_response.candidates = [mock_candidate]
    return mock_response


def test_evidence_includes_seed_fields_when_seed_used():
    """extract_code_execution_evidence verifies seed against pre-roll commitment."""
    server_seed = "f" * 64
    code = (
        f"import random\nrandom.seed('{server_seed}')\n"
        "roll = random.randint(1, 20)\n"
        'print(\'{"rolls": [14], "total": 14}\')'
    )
    response = _make_mock_response(code, '{"rolls": [14], "total": 14}')
    response._pre_roll_server_seed = server_seed

    evidence = extract_code_execution_evidence(response)

    assert evidence.get("dice_server_seed") == server_seed
    assert evidence.get("dice_seed_commitment") == hashlib.sha256(server_seed.encode()).hexdigest()
    assert evidence.get("dice_seed_verified") is True


def test_evidence_seed_verified_true_when_derived_seed_in_code():
    """dice_seed_verified is True when executed code uses a derived seed (not base)."""
    base_seed = "f" * 64
    derived_1 = hashlib.sha256((base_seed + "\n1").encode()).hexdigest()
    code = (
        f"import random\nrandom.seed('{derived_1}')\n"
        "roll = random.randint(1, 20)\n"
        'print(\'{"rolls": [14], "total": 14}\')'
    )
    response = _make_mock_response(code, '{"rolls": [14], "total": 14}')
    response._pre_roll_server_seed = base_seed

    evidence = extract_code_execution_evidence(response)

    assert evidence.get("dice_server_seed") == base_seed
    assert evidence.get("dice_seed_commitment") == hashlib.sha256(base_seed.encode()).hexdigest()
    assert evidence.get("dice_seed_verified") is True


def test_evidence_seed_verified_false_when_gemini_ignores_seed():
    """dice_seed_verified is False when Gemini uses time.time_ns() despite server_seed being injected."""
    server_seed = "a" * 64
    # Gemini ignores the injected seed and falls back to time.time_ns().
    code = (
        "import random, time\nrandom.seed(time.time_ns())\n"
        "roll = random.randint(1, 20)\n"
        'print(\'{"rolls": [14], "total": 14}\')'
    )
    response = _make_mock_response(code, '{"rolls": [14], "total": 14}')
    response._pre_roll_server_seed = server_seed

    evidence = extract_code_execution_evidence(response)

    assert evidence.get("dice_seed_verified") is False


def test_evidence_seed_fields_absent_when_no_seed():
    """extract_code_execution_evidence has no seed fields when time.time_ns() used."""
    code = (
        "import random, time\nrandom.seed(time.time_ns())\n"
        "roll = random.randint(1, 20)\n"
        'print(\'{"rolls": [14], "total": 14}\')'
    )
    response = _make_mock_response(code, '{"rolls": [14], "total": 14}')

    evidence = extract_code_execution_evidence(response)

    assert "dice_server_seed" not in evidence
    assert "dice_seed_commitment" not in evidence
    assert evidence.get("dice_seed_verified") is False
