---
title: "mvp_site dice_provably_fair"
type: source
tags: []
date: 2026-04-14
source_file: raw/mvp_site_all/dice_provably_fair.py
---

## Summary
Provably fair dice roll primitives using cryptographic commitment scheme. Server generates seed, publishes SHA-256 commitment pre-roll, then injects seed into Gemini code_execution prompt. Players can verify rolls post-game.

## Key Claims
- generate_server_seed() returns cryptographically secure 32-byte seed as 64-char hex
- compute_commitment() returns SHA-256 hex digest of seed (pre-roll commitment)
- inject_seed_into_prompt() replaces random.seed(time.time_ns()) with derived seeds in prompt
- _derive_seed_for_occurrence() creates unique seeds for each occurrence (multiple rolls in one turn)
- is_valid_injected_seed() verifies extracted seed matches commitment

## Connections
- [[DiceMechanics]] — provably fair dice system
- [[LLMIntegration]] — seed injection into code execution prompts
