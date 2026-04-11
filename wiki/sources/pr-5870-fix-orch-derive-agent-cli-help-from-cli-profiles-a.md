---
title: "PR #5870: fix(orch): derive --agent-cli help from CLI_PROFILES (adds minimax)"
type: source
tags: []
date: 2026-03-07
source_file: raw/prs-worldarchitect-ai/pr-5870.md
sources: []
last_updated: 2026-03-07
---

## Summary
- `--agent-cli` help text was hardcoded as `claude, codex, gemini, cursor` — missing `minimax`
- Now derives the list dynamically from `CLI_PROFILES.keys()` so any future additions are automatic

## Metadata
- **PR**: #5870
- **Merged**: 2026-03-07
- **Author**: jleechan2015
- **Stats**: +7/-6 in 6 files
- **Labels**: none

## Connections
