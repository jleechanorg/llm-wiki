---
title: "Intent Matching Guardrail"
type: concept
tags: [prompt-engineering, validation, game-state, hallucination]
sources: [manual-beads-creation-guide]
last_updated: 2026-04-07
---

## Definition
A validation mechanism that ensures AI responses reference the correct entity or target that the player explicitly named, preventing responses about unrelated entities from previous scenes.

## Problem
Player asks to attack "Golden Dawn" but AI responds about "Blood Ravens" from previous scene — a form of context hallucination where the model drifts to previously-discussed entities.

## Solution
Add intent/entity matching guardrail in prompts that:
1. Extracts the explicit target from player input
2. Validates AI response targets match the extracted intent
3. Re-prompts or blocks if mismatched

## Related Concepts
- [[ContextManagement]] — preventing context drift
- [[PromptEngineering]] — structuring prompts to reduce hallucinations
