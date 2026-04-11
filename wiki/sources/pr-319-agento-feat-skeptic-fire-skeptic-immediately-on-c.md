---
title: "PR #319: [agento] feat(skeptic): fire skeptic immediately on CR approval (no 30-min wait)"
type: source
tags: []
date: 2026-03-31
source_file: raw/prs-worldai_claw/pr-319.md
sources: []
last_updated: 2026-03-31
---

## Summary
When CodeRabbit approves a PR on the same commit (no new push), the skeptic dispatch
block in `lifecycle-manager.ts` fires only on SHA changes. With no SHA change, skeptic
waits up to 30 min for the `skeptic-cron` interval.

## Metadata
- **PR**: #319
- **Merged**: 2026-03-31
- **Author**: jleechan2015
- **Stats**: +199/-0 in 2 files
- **Labels**: none

## Connections
