---
title: "PR #346: [agento] fix(skeptic-cron): make evidence gate fail-closed (live + template)"
type: source
tags: []
date: 2026-04-03
source_file: raw/prs-worldai_claw/pr-346.md
sources: []
last_updated: 2026-04-03
---

## Summary
The skeptic-cron workflow's 6-green gate 6 (Evidence review) was pass-open: it only checked `evidence-review-bot` approval and silently treated missing evidence as N/A. This let PRs merge without any evidence bundle.

## Metadata
- **PR**: #346
- **Merged**: 2026-04-03
- **Author**: jleechan2015
- **Stats**: +62/-10 in 3 files
- **Labels**: none

## Connections
