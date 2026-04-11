---
title: "PR #136: fix(lifecycle): re-send agent-stuck nudge periodically when session stays stuck (bd-sbr)"
type: source
tags: []
date: 2026-03-23
source_file: raw/prs-worldai_claw/pr-136.md
sources: []
last_updated: 2026-03-23
---

## Summary
The `agent-stuck` reaction fires after a session idles beyond a threshold (e.g., 15 min). However, it was only firing **once** — on the `working → stuck` transition — then never again, no matter how long the session stayed stuck.

Root cause: reactions only fire on status **transitions** (`newStatus !== oldStatus`). Once a session enters `"stuck"`, every subsequent poll returns the same status, hitting the `else` (no-transition) branch where no retry logic existed for stuck sessions. The session

## Metadata
- **PR**: #136
- **Merged**: 2026-03-23
- **Author**: jleechan2015
- **Stats**: +69/-3 in 2 files
- **Labels**: none

## Connections
