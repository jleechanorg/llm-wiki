---
title: "PR #2103: Address service DI and validation feedback"
type: source
tags: [codex]
date: 2025-11-24
source_file: raw/prs-worldarchitect-ai/pr-2103.md
sources: []
last_updated: 2025-11-24
---

## Summary
- use injected modules across services, add thread-safe/resettable singletons, and guard async runners against pydantic validation errors
- align user settings validation with world_logic schema and translate ai_model/debug_mode to expected payloads
- expand tests for injected world_logic usage, singleton reset, and updated async helper docs/imports

## Metadata
- **PR**: #2103
- **Merged**: 2025-11-24
- **Author**: jleechan2015
- **Stats**: +208/-90 in 6 files
- **Labels**: codex

## Connections
