"""Provably fair dice roll primitives.

Provides cryptographic functions to make dice rolls verifiable by players:

  1. Server generates a seed and publishes sha256(seed) as commitment pre-roll.
  2. The seed is injected into Gemini's code_execution prompt so it calls
     random.seed(server_seed) before rolling.
  3. Gemini's executed_code is stored verbatim in Firestore debug_info.
  4. Post-roll, the server reveals the seed. Players verify:
       sha256(revealed_seed) == stored_commitment
       running the same executed_code with the seed produces the same result.

All functions are pure; no I/O or external dependencies.
"""

from __future__ import annotations

import ast
import hashlib
import re
import secrets

# Matches random.seed('<64 hex chars>') produced by inject_seed_into_prompt.
# Case-insensitive to handle any future changes to seed generation format.
_INJECTED_SEED_PATTERN = re.compile(r"random\.seed\('([a-fA-F0-9]{64})'\)")

# Max occurrences of random.seed(time.time_ns()) in CODE_EXECUTION_DICE_OVERRIDE.
# Each gets a unique derived seed so multiple rolls in one turn produce different results.
_MAX_SEED_OCCURRENCES = 4


def generate_server_seed() -> str:
    """Return a cryptographically secure 32-byte seed as a 64-char hex string."""
    return secrets.token_hex(32)


def compute_commitment(server_seed: str) -> str:
    """Return SHA-256 hex digest of server_seed (the pre-roll commitment hash)."""
    return hashlib.sha256(server_seed.encode()).hexdigest()


def _derive_seed_for_occurrence(base_seed: str, occurrence_index: int) -> str:
    """Return a deterministic 64-char hex seed for the i-th occurrence.

    Occurrence 0 uses the base seed; others are derived via SHA-256 so each
    random.seed() call in the same turn gets a different seed, avoiding
    identical roll results across multiple code blocks.
    """
    if occurrence_index == 0:
        return base_seed
    return hashlib.sha256((base_seed + "\n" + str(occurrence_index)).encode()).hexdigest()


def is_valid_injected_seed(extracted: str, base_seed: str) -> bool:
    """Return True if extracted is the base seed or a valid derived seed."""
    for i in range(_MAX_SEED_OCCURRENCES):
        if extracted == _derive_seed_for_occurrence(base_seed, i):
            return True
    return False


def inject_seed_into_prompt(prompt: str, server_seed: str) -> str:
    """Replace every ``random.seed(time.time_ns())`` in prompt with derived seeds.

    Each occurrence gets a unique seed (base for 0, derived for 1..3) so multiple
    rolls in one turn produce different results. The base seed is used for the
    commitment; players verify sha256(base_seed) == stored_commitment.
    """
    result = prompt
    for i in range(_MAX_SEED_OCCURRENCES):
        seed_i = _derive_seed_for_occurrence(server_seed, i)
        # Replace one occurrence at a time so each gets a different seed
        result = result.replace(
            "random.seed(time.time_ns())",
            f"random.seed('{seed_i}')",
            1,
        )
    return result


def verify_seed_in_executed_code(executed_code: list[str], server_seed: str) -> bool:
    """Return True if server_seed appears literally in any of the executed code samples."""
    return any(server_seed in code for code in executed_code)


def _is_valid_64_hex(s: str) -> bool:
    """Return True if s is exactly 64 hexadecimal characters."""
    return len(s) == 64 and all(c in "0123456789abcdefABCDEF" for c in s)


def _extract_seed_via_ast(code: str) -> str | None:
    """Extract seed from random.seed('<hex>') function call via AST. Returns None on parse failure."""
    try:
        tree = ast.parse(code)
        for node in ast.walk(tree):
            if isinstance(node, ast.Call):
                func = node.func
                if isinstance(func, ast.Attribute) and func.attr == "seed":
                    if node.args and isinstance(node.args[0], ast.Constant):
                        arg_val = node.args[0].value
                        if isinstance(arg_val, str) and _is_valid_64_hex(arg_val):
                            return arg_val
    except (SyntaxError, ValueError):
        pass
    return None


def extract_seed_from_executed_code(executed_code: list[str]) -> str | None:
    """Extract the injected server seed from stored executed_code samples.

    Uses AST parsing to avoid false positives from string literals (e.g.,
    example = "random.seed('...')"). Falls back to regex on code without
    comment lines if AST fails.

    Returns the 64-char hex seed string if found, or None if the code used
    time.time_ns() (i.e., no provably-fair seed was injected).
    """
    for code in executed_code:
        # AST-first: only matches actual function calls, not string literals
        extracted = _extract_seed_via_ast(code)
        if extracted is not None:
            return extracted
        # Fallback: regex on code without comments
        code_without_comments = "\n".join(
            line for line in code.splitlines() if not line.lstrip().startswith("#")
        )
        match = _INJECTED_SEED_PATTERN.search(code_without_comments)
        if match:
            return match.group(1)
    return None


def verify_commitment(server_seed: str, commitment: str) -> bool:
    """Return True if sha256(server_seed) matches the stored commitment hash."""
    return compute_commitment(server_seed) == commitment
