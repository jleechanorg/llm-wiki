---
title: "GOD MODE"
type: entity
tags: [feature, admin, state-modification]
sources: ["god-mode-end-to-end-integration-tests"]
last_updated: 2026-04-08
---

## Description
Admin functionality for correcting mistakes and modifying campaign state. Uses a separate, focused prompt stack without narrative generation prompts.

## Used In
- test_god_mode_end2end.py
- main.py (app endpoints)
- agent_prompts.py (PromptBuilder)
- narrative_response_schema.py

## Connections
- [[PromptBuilder]] — builds god mode prompts
- [[validate_god_mode_response]] — validates responses
- [[FakeFirestoreClient]] — stores state changes
