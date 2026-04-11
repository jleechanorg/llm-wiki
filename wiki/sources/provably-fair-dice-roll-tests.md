---
title: "Provably Fair Dice Roll System Tests"
type: source
tags: [python, testing, dice-integrity, provably-fair, cryptography, tdd]
source_file: "raw/test_provably_fair.py"
sources: []
last_updated: 2026-04-08
---

## Summary
TDD tests for the provably fair dice roll system that validate the full cryptographic chain: server seed generation, SHA256 commitment computation, seed injection into prompts, and verification of executed code. Tests are designed to run before implementation and cover both pure function logic and Gemini code execution integration.

## Key Claims
- **Server Seed Generation**: `generate_server_seed()` produces 64-character hex strings that are unique each time
- **Commitment Verification**: `compute_commitment()` uses SHA256 and `verify_commitment()` validates seed/commitment pairs
- **Seed Injection**: `inject_seed_into_prompt()` replaces `time.time_ns()` calls with seeded `random.seed()` using unique seeds per occurrence
- **Code Verification**: `verify_seed_in_executed_code()` confirms seeds were actually used in executed Python code
- **TDD Approach**: Tests written before implementation to define the cryptographic contract

## Key Test Functions
- `test_generate_server_seed_is_64_hex_chars` — validates seed format
- `test_generate_server_seed_is_unique` — ensures entropy
- `test_compute_commitment_is_sha256` — verifies hash algorithm
- `test_inject_seed_replaces_time_ns` — confirms seed injection
- `test_inject_seed_replaces_all_occurrences_with_unique_seeds` — validates unique seeds per roll
- `test_verify_seed_in_executed_code_found` — confirms verification works

## Connections
- [[ProvablyFairDice]] — the cryptographic dice system concept
- [[TestDrivenDevelopment]] — methodology used to write these tests
- [[GeminiCodeExecution]] — integration for running dice roll code
