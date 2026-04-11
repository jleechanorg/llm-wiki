---
title: "PR #320: [agento] feat(skeptic-cron): SHA-based dedup — skip re-evaluation when HEAD SHA unchanged"
type: source
tags: []
date: 2026-03-31
source_file: raw/prs-worldai_claw/pr-320.md
sources: []
last_updated: 2026-03-31
---

## Summary
`runLocalSkepticCron` evaluates every open PR on every 10-min cycle even if VERDICT was already posted for the current HEAD SHA. This wastes LLM calls and creates duplicate comments.

## Metadata
- **PR**: #320
- **Merged**: 2026-03-31
- **Author**: jleechan2015
- **Stats**: +324/-3 in 2 files
- **Labels**: none

## Connections
