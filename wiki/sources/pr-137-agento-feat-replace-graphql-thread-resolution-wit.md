---
title: "PR #137: [agento] feat: replace GraphQL thread resolution with PR description documentation (bd-ara.1)"
type: source
tags: []
date: 2026-03-24
source_file: raw/prs-worldai_claw/pr-137.md
sources: []
last_updated: 2026-03-24
---

## Summary
- Replaces expensive GraphQL-based review thread resolution in `defaults.agentRules` with PR description documentation
- Workers no longer call `autoResolveThreads()` (burns GraphQL rate limit); instead they append a `## Resolved Comments| Reviewer | File | Comment | Resolution |
|---|---|---|---|
| Copilot | roadmap/autonomy-blockers-v2.md | Fix Type column encodes status; add Status column | Fixed in d361cea1 — split into Fix Type + Status columns |
| Copilot | roadmap/autonomy-blockers-v2.md

## Metadata
- **PR**: #137
- **Merged**: 2026-03-24
- **Author**: jleechan2015
- **Stats**: +85/-16 in 4 files
- **Labels**: none

## Connections
