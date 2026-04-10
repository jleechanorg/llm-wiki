---
title: "Provably Fair Dice"
type: concept
tags: [dice, cryptography, provably-fair, security]
sources: [provably-fair-dice-roll-tests]
last_updated: 2026-04-08
---

A cryptographic dice rolling system where the server generates a seed, computes a commitment (SHA256 hash), and the client provides a client seed. The combination determines the dice outcome, allowing players to verify the roll was not manipulated after the fact.

## Components

1. **Server Seed**: 64-character hex string generated via `generate_server_seed()`
2. **Commitment**: SHA256 hash of the server seed via `compute_commitment(seed)`
3. **Seed Injection**: Replacing `time.time_ns()` with deterministic `random.seed(server_seed)` in prompts
4. **Verification**: Checking that executed code actually used the injected seed

## Verification Flow
1. Server generates seed and publishes commitment (hash) before roll
2. Client provides client seed
3. Combined seeds determine outcome via `random.randint(1, 20)`
4. After roll, server reveals seed — player verifies commitment matches and code used seed

## Related
- [[CodeExecutionEvidenceExtraction]] — extracting proof of dice execution
- [[DiceIntegrityModule]] — ensuring dice fields are present and valid
