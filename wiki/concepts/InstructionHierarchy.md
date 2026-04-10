---
title: "Instruction Hierarchy"
type: concept
tags: [prompt-engineering, system-instructions, ai-behavior]
sources: [prompts-directory]
last_updated: 2026-04-08
---

## Definition
The layered authority structure governing how AI system instructions are prioritized and loaded in WorldArchitect.AI. Higher authority instructions take precedence when conflicts arise.

## Levels
1. **Master Directive** (highest) — Core AI personality, instruction conflict resolution
2. **Game State Instructions** — Data structures, JSON format, state management
3. **Feature-Specific Instructions** — Narrative, mechanics, dice systems
4. **System Reference** (lowest) — D&D SRD for rule lookup only

## Application
When generating responses, the AI follows instructions from highest to lowest authority. Lower-level instructions cannot override higher-level ones.
