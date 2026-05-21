---
title: WorldArchitect.AI
type: entity
tags: [project, dnd, ai-gm, game-engine]
date: 2026-05-16
---

## Summary
Production D&D 5e AI Game Master platform. Flask + MCP backend, Gemini AI engine with 14 specialized agents, FastEmbed semantic routing, deterministic token budget, dice anti-fabrication, and living world factions. Deployed on Google Cloud Run.

## Key Metrics
- 14 specialized agents ([agents.py](https://github.com/jleechanorg/worldarchitect.ai/blob/main/mvp_site/agents.py))
- 30 prompt files, 17,369 lines ([prompts/](https://github.com/jleechanorg/worldarchitect.ai/blob/main/mvp_site/prompts/))
- 12 living world factions ([faction/](https://github.com/jleechanorg/worldarchitect.ai/blob/main/mvp_site/faction/))
- 370 test files
- 684 tracked files in mvp_site/

## Architecture
See [[WorldArchitect System Architecture v3.0]] for full deep-dive.

## Connections
- [[GeminiAPI]] — primary LLM
- [[FastEmbed]] — semantic routing
- [[DiceIntegrity]] — anti-fabrication
- [[TokenBudget]] — token allocation
- [[FactionSystem]] — living world
