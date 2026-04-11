---
title: "PR #6078: fix(skeptic-cron): handle gh api --paginate exit code failures"
type: source
tags: []
date: 2026-04-02
source_file: raw/prs-worldarchitect-ai/pr-6078.md
sources: []
last_updated: 2026-04-02
---

## Summary
- Fix skeptic-cron List open PRs step: gh api --paginate exits non-zero when ANY page fails mid-stream, causing the entire step to fail and skipping all PR processing
- Add || true guard + JSON validation + single-page fallback retry so transient page errors dont kill the cron run

## Metadata
- **PR**: #6078
- **Merged**: 2026-04-02
- **Author**: jleechan2015
- **Stats**: +13/-1 in 1 files
- **Labels**: none

## Connections
