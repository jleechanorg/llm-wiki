---
title: "PR #4334: dice: strategy-aware prompts, cache tools, and expanded test suite"
type: source
tags: []
date: 2026-02-01
source_file: raw/prs-worldarchitect-ai/pr-4334.md
sources: []
last_updated: 2026-02-01
---

## Summary
- Split dice instructions into strategy-specific prompt files and wire prompt assembly to load them per dice strategy
- Ensure Gemini explicit cache includes required tools for code_execution and track/cache rebuild conditions
- Reorganize dice tests and expand evidence capture/validation coverage
- Update DC ordering checks: only enforce when a DC appears in code execution output; add per-roll ordering signal
- Fix null value handling in social_hp_challenge validation

**Key themes:**
- Strateg

## Metadata
- **PR**: #4334
- **Merged**: 2026-02-01
- **Author**: jleechan2015
- **Stats**: +2470/-1452 in 43 files
- **Labels**: none

## Connections
