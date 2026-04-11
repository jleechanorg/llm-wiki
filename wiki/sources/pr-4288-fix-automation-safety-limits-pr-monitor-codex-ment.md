---
title: "PR #4288: fix: automation safety limits + PR monitor + codex mentions"
type: source
tags: []
date: 2026-01-31
source_file: raw/prs-worldarchitect-ai/pr-4288.md
sources: []
last_updated: 2026-01-31
---

## Summary
- Safety limits: rolling-window global/pr counts, retry logic around atomic_update, clearer fail-closed behavior
- PR monitor: anti-loop for bot replies, REST pagination for >100 comments, single-action mode
- Codex automation: sessionStorage persistence + task discovery tuned to GitHub Mention tasks only
- Tests updated/added to cover safety limits, rolling window, pagination, and codex task filtering

## Metadata
- **PR**: #4288
- **Merged**: 2026-01-31
- **Author**: jleechan2015
- **Stats**: +1914/-581 in 24 files
- **Labels**: none

## Connections
