---
title: "PR #91: feat: add evidence-fidelity contract validation to system_instruction.ts"
type: source
tags: []
date: 2026-03-26
source_file: raw/prs-worldai_claw/pr-91.md
sources: []
last_updated: 2026-03-26
---

## Summary
LLM-generated `scene_text` in WorldArchitect responses can claim permanent outcomes (combat rewards, NPC deaths, XP gains, level-ups) without corresponding `state_delta` or `mechanic_requests`. This violates the Evidence Fidelity Contract documented in Layer 5 of the system prompt (already present in `system_instruction.md` lines 154-158) but had no programmatic enforcement.

## Metadata
- **PR**: #91
- **Merged**: 2026-03-26
- **Author**: jleechan2015
- **Stats**: +201/-0 in 2 files
- **Labels**: none

## Connections
