---
title: "Planning Loop Detection"
type: concept
tags: [bug, social-encounter, loop, planning-block]
sources: [planning-loop-detection-social-encounters-red-tests.md]
last_updated: 2026-04-08
---

## Summary
A bug pattern where the LLM presents the same or similar planning block choices repeatedly without executing the action or rolling dice, causing the narrative to never progress.

## Bug Pattern
1. User selects a social action (e.g., "Press the Logical Argument")
2. LLM describes the situation but doesn't roll dice
3. LLM presents same/similar options again
4. Loop repeats indefinitely — narrative never progresses

## Detection Mechanism
- Track conversation history for similar action keywords
- Count occurrences of similar user actions (e.g., "press", "maintain", "logical", "argument", "pressure", "mathematical")
- After 2+ similar actions, trigger Anti-Loop Rule enforcement

## Bug Example
User selected variants of "Press Logical Argument" 6+ times (Scenes 257-264) without resolution.

## Connections
- [[AntiLoopRule]] — solution to break the loop
- [[SocialEncounter]] — where this bug manifests
- [[ActionExecutionRule]] — rule that should prevent this behavior
- [[DiceRoll]] — missing component that would break the loop
