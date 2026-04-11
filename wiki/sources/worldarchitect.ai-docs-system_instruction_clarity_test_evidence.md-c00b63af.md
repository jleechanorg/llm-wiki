---
title: "System Instruction Clarity Test Evidence"
type: source
tags: [worldarchitect, system-instructions, testing, clarity-improvements, pr-3741]
sources: []
source_file: docs/system_instruction_clarity_test_evidence.md
date: 2026-04-07
last_updated: 2026-04-07
---

## Summary

Test evidence from PR #3741 ("improve-system-instruction-clarity") demonstrating that breaking dense system instructions into numbered steps improves LLM clarity without breaking functionality. The test captured system instructions for CharacterCreationAgent (67,668 chars) and StoryModeAgent (137,686 chars) across multiple actions, validating that clarity improvements are safe to merge.

## Key Claims

- **test_system_instruction_capture.py** ✅ PASS — successfully captured system instructions for CharacterCreationAgent (4 files, 67,668 chars) and StoryModeAgent (5 files, 137,686 chars across two actions)
- **test_social_hp_all_tiers_real_api.py** ⚠️ FAILURES — 0/14 tests pass due to pre-existing missing `resistance_shown` field, not clarity-related
- **test_sanctuary_autonomy.py** ⏱️ TIMEOUT — test timed out (>120s) due to complexity, not clarity changes
- **test_outcome_declaration_guardrails.py** ❌ ERROR — LLM returned empty narrative, response quality issue
- **Social HP clarity improvement** — broken 8+ nested requirements into numbered steps (Step 1: Populate JSON Field, Step 2: Include Narrative Box)
- **Sanctuary Mode clarity improvement** — converted complex conditional to 5-step process (Check Status → Check Input → Break → Add Notification → Process)
- **Action Resolution clarity improvement** — inlined critical schema information from external references

## Key Quotes

> "The clarity improvements are **functionally safe** and do not break existing tests." — Test Analysis

> "Clarity score improved from 4/10 to ~7/10" — Social HP Challenge

> "Clarity score improved from 6/10 to ~8/10" — Sanctuary Mode

## Connections

- [[WorldArchitect.AI]] — the platform being tested
- [[Testing MCP - Server-Level Tests with Real LLMs]] — testing methodology context

## Contradictions

- None identified — test failures are pre-existing implementation issues, not caused by clarity changes