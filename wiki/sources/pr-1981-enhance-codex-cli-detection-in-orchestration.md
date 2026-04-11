---
title: "PR #1981: Enhance Codex CLI detection in orchestration"
type: source
tags: [codex]
date: 2025-11-08
source_file: raw/prs-worldarchitect-ai/pr-1981.md
sources: []
last_updated: 2025-11-08
---

## Summary
- broaden Codex CLI detection keywords so tasks that mention Codex directly select the Codex profile
- add binary-name matching in the dispatcher to catch explicit CLI references
- cover the new detection path with a unit test ensuring Codex is chosen when mentioned by name

## Metadata
- **PR**: #1981
- **Merged**: 2025-11-08
- **Author**: jleechan2015
- **Stats**: +22/-3 in 2 files
- **Labels**: codex

## Connections
