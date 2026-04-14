---
title: "LLM Verdict Trust"
type: concept
tags: [pairv2, bug-pattern, automation]
sources: []
last_updated: 2026-04-13
---

## Description

The LLM verdict trust pattern ensures the system never overrides LLM judgment with timing heuristics. If the verifier says FAIL, trust it — never downgrade based on how long the verifier was active.

## Why It Matters

`_read_verification_outcome` was downgrading verifier FAIL to NEEDS_HUMAN if verifier was active for less than 60 seconds. This overrides LLM judgment with a timing heuristic that has no bearing on whether the code is correct.

## Key Technical Details

- **Pattern**: Never override LLM verdict with timing heuristics
- **Scope**: `.claude/pair/pair_execute_v2.py` — `_read_verification_outcome`
- **Key insight**: Trust the verifier's judgment, not the timing

## Related Beads

- BD-pairv2-liveliness-override
