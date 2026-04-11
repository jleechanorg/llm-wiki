---
title: "PR #2564: feat(god-mode): LLM-based directive extraction with persistent rules"
type: source
tags: []
date: 2025-12-30
source_file: raw/prs-worldarchitect-ai/pr-2564.md
sources: []
last_updated: 2025-12-30
---

## Summary
This PR fixes god mode directive persistence so users can say things like "stop forgetting to apply Foresight advantage" and have those rules actually persist and be followed.

### Key Changes

**God Mode Directive System (Core Fix)**
- LLM-based directive extraction from natural language ("stop forgetting", "remember to", "from now on")
- Directives persist in `custom_campaign_state.god_mode_directives[]` with timestamps
- Wired `directives` field through extraction pipeline: `structured_fields

## Metadata
- **PR**: #2564
- **Merged**: 2025-12-30
- **Author**: jleechan2015
- **Stats**: +2081/-275 in 29 files
- **Labels**: none

## Connections
