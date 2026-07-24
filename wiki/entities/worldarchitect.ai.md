---
title: "WorldArchitect.AI"
type: entity
tags: [project, game, dnd, ai-gm]
sources: [llm-service-ai-integration-response-processing]
last_updated: 2026-04-08
---

AI-powered tabletop RPG game master platform that uses Gemini for story generation. The llm_service module provides comprehensive AI integration handling story generation, prompt construction, entity tracking, and response processing.

## Key Components
- [[LLM Service - AI Integration and Response Processing]] — core AI service module
- [[Game State Management Protocol]] — state handling
- [[Faction & Army Management System]] — faction minigame
- [[Living World Protocol]] — living world events

## Connections
- [Doc-stated safety policy must be code-enforced (2026-07-17)](../sources/feedback-2026-07-17-doc-stated-policy-must-be-code-enforced.md) — repo's `.claude/skills/ezgha-watchdog/` skill's stated "fail-closed" policy wasn't code-enforced until PR #8393; entity [[EzGhaDaemon]]
