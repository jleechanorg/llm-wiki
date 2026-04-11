---
title: "PR #5953: feat(codex): add Codex hooks and exportcommands support"
type: source
tags: []
date: 2026-03-14
source_file: raw/prs-worldarchitect-ai/pr-5953.md
sources: []
last_updated: 2026-03-14
---

## Summary
- Add `.codex/hooks/` with three hooks: `git-header.sh` (statusline), `pre-exec-hook.sh` (safety validator), `stop-git-header-json.sh` (session summary)
- Add `.codex/hooks.json` wiring pre-exec and stop hooks
- Update `/exportcommands` and `/localexportcommands` to include `.codex/hooks` and `.codex/skills` in exported bundles

## Metadata
- **PR**: #5953
- **Merged**: 2026-03-14
- **Author**: jleechan2015
- **Stats**: +662/-1 in 7 files
- **Labels**: none

## Connections
