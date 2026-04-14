---
title: "mvp_site — Dice Rolling System"
type: source
tags: [worldarchitect-ai, dice, determinism, DICE_SEED, authenticity, llm-fabrication]
date: 2026-04-14
source_file: raw/mvp_site_all/dice.py
---

## Summary

Core dice rolling implementation with deterministic RNG support via `DICE_SEED` environment variable. When `DICE_SEED` is set, rolls are reproducible (critical for test evidence). Includes fabrication detection — checks whether dice rolls appearing in narrative text were actually executed by the dice tool or hallucinated by the LLM.

## Key Claims

### Deterministic Mode
- `DICE_SEED=<value>` environment variable enables deterministic RNG
- `random.Random(_DICE_SEED_VALUE)` used instead of global random
- All dice rolls logged with campaign context when seed is active

### Dice Fabrication Detection
`log_dice_fabrication_check()` tracks:
- `has_dice_in_narrative` — dice notation found in LLM narrative text
- `has_dice_in_structured` — dice in structured response
- `code_execution_used` — did the LLM actually call the dice tool?
- `tool_requests_executed` — were dice tool requests actually executed?

**Fabrication = narrative has dice but code execution wasn't used** — LLM invented a roll rather than executing it.

### Narrative Dice Pattern Detection
Regex patterns detect dice notation in narrative text:
- `\d+d\d+` notation (e.g., "1d20+5")
- "rolls a 15" type phrases (only when context suggests check/attack/save)
- `[dice:...]` tagged dice results

## Connections

- [[DiceAuthenticity]] — the overarching principle that dice must be real rolls
- [[DiceRollDebugRegression]] — frontend gates dice on debugMode (bug)
- [[mvp-site-action-resolution-utils]] — dice roll extraction and audit events
- [[dice_integrity]] — full fabrication detection pipeline
- [[mvp-site-battle-sim]] — battle simulation uses dice.py rolls
