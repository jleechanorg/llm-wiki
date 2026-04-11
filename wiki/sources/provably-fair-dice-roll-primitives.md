---
title: "Provably Fair Dice Roll Primitives"
type: source
tags: [cryptography, dice, gaming, verification, security]
source_file: "raw/provably-fair-dice-roll-primitives.md"
sources: []
last_updated: 2026-04-08
---

## Summary
Cryptographic system enabling verifiable dice rolls for WorldArchitect.AI game sessions. Uses a commitment scheme where the server publishes a SHA-256 hash of the seed before the roll, then reveals the seed post-roll for player verification. Ensures the server cannot manipulate outcomes after seeing the prompt.

## Key Claims
- **Commitment Scheme**: Server generates a 64-char hex seed, publishes `sha256(seed)` before roll, reveals seed post-roll for verification
- **Seed Injection**: The seed is injected into Gemini's code_execution prompt so `random.seed(server_seed)` runs before any dice functions
- **Multi-Roll Support**: Derived seeds via SHA-256 ensure multiple rolls in one turn produce different results
- **Verification**: Players compare `sha256(revealed_seed)` against stored commitment and re-run the executed code to confirm results

## Key Functions
- `generate_server_seed()`: Creates cryptographically secure 32-byte seed
- `compute_commitment()`: Returns SHA-256 hex digest for pre-roll publication
- `inject_seed_into_prompt()`: Replaces `random.seed(time.time_ns())` with deterministic seeds
- `verify_seed_in_executed_code()`: Confirms seed appears in stored code
- `extract_seed_from_executed_code()`: Parses executed code via AST to recover seed

## Connections
- [[Combat System Protocol]] — uses these primitives for verifiable combat dice rolls
- [[Deferred Rewards Protocol]] — may use for randomized loot generation
- [[Capture Framework Documentation]] — executed_code stored in Firestore for verification

## Contradictions
- None identified
