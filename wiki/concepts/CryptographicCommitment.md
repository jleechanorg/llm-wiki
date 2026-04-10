---
title: "Cryptographic Commitment"
type: concept
tags: [cryptography, hash, commitment, verification]
sources: [provably-fair-dice-roll-primitives]
last_updated: 2026-04-08
---

A cryptographic primitive that allows a party to commit to a value while keeping it hidden, then reveal it later. The commitment phase binds the committer to a specific value without revealing it, while the reveal phase allows anyone to verify the commitment was valid.

## Properties
- **Binding**: Cannot change the committed value after commitment
- **Hiding**: Cannot determine the original value from the commitment

## Use in WorldArchitect.AI
- Server computes `sha256(seed)` as the commitment
- Commitment is stored/published before LLM generates the outcome
- Post-generation, server reveals the original seed
- Verification: `sha256(revealed_seed) == stored_commitment`

## Related Concepts
- [[Provably Fair Gaming]] — applies commitment to game outcomes
- SHA-256 — used as the hash function (collision-resistant)
