---
title: "PR #5976: feat(mem0): add Codex SessionStart+Stop hooks for automatic memory recall/save"
type: source
tags: []
date: 2026-03-15
source_file: raw/prs-worldarchitect-ai/pr-5976.md
sources: []
last_updated: 2026-03-15
---

## Summary
- Adds `.codex/hooks/mem0_recall.py` — SessionStart hook that searches the `openclaw_mem0` qdrant store and injects top-K memories as context before each Codex session
- Adds `.codex/hooks/mem0_save.py` — Stop hook that extracts facts from the last assistant turn and saves to qdrant via mem0 LLM extraction (`infer=True`)
- Updates `.codex/hooks.json` to wire both hooks alongside the existing git-header stop hook

## Metadata
- **PR**: #5976
- **Merged**: 2026-03-15
- **Author**: jleechan2015
- **Stats**: +219/-0 in 3 files
- **Labels**: none

## Connections
