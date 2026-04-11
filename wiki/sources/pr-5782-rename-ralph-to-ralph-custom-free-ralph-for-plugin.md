---
title: "PR #5782: Rename /ralph to /ralph_custom, free /ralph for plugin"
type: source
tags: []
date: 2026-02-26
source_file: raw/prs-worldarchitect-ai/pr-5782.md
sources: []
last_updated: 2026-02-26
---

## Summary
- Rename `.claude/commands/ralph.md` → `ralph_custom.md` so the project-level command no longer shadows the `ralph-marketplace` plugin
- `/ralph` now resolves to the plugin (`ralph-skills:ralph`) — PRD converter for Ralph autonomous execution
- `/ralph_custom` retains the old orchestrator workflow (Codex CLI, goal files, tmux sessions) using repo at `/Users/$USER/projects_other/ralph-orchestrator`

## Metadata
- **PR**: #5782
- **Merged**: 2026-02-26
- **Author**: jleechan2015
- **Stats**: +6/-6 in 1 files
- **Labels**: none

## Connections
