---
title: "PR #4540: feat: Add living world dual-trigger system (turns + time)"
type: source
tags: []
date: 2026-02-03
source_file: raw/prs-worldarchitect-ai/pr-4540.md
sources: []
last_updated: 2026-02-03
---

## Summary
- Move living world tracking updates to post-response state handling to avoid advancing on failed LLM calls.
- Keep living world prompts out of combat mode and prevent stateless turn 0 triggers.
- Add focused tests for tracking updates and stateless/combat behavior.

## Metadata
- **PR**: #4540
- **Merged**: 2026-02-03
- **Author**: jleechan2015
- **Stats**: +2072/-1124 in 16 files
- **Labels**: none

## Connections
