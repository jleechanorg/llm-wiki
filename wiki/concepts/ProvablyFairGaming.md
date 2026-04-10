---
title: "Provably Fair Gaming"
type: concept
tags: [cryptography, gaming, verification, fairness]
sources: [provably-fair-dice-roll-primitives]
last_updated: 2026-04-08
---

A gaming paradigm where players can verify that game outcomes (dice rolls, card shuffles, random events) were not manipulated by the server. The server commits to a random value before the outcome is determined, then reveals it afterward for verification.

## How It Works
1. Server generates a random seed
2. Server publishes a cryptographic hash of the seed (commitment)
3. Game uses the seed to determine the outcome
4. Server reveals the seed post-outcome
5. Players verify the hash matches and re-run the random process

## Implementation in WorldArchitect.AI
- [[Provably Fair Dice Roll Primitives]] provide the core functions
- Seed is injected into LLM code_execution prompts
- Executed code is stored in Firestore for later verification
- SHA-256 commitment ensures pre-image resistance

## Related Concepts
- [[Cryptographic Commitment]] — hash-based commitment schemes
- [[Seed Injection]] — injecting deterministic seeds into prompts
