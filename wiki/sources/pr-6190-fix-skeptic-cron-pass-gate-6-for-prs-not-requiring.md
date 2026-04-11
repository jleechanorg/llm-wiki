---
title: "PR #6190: fix(skeptic-cron): pass Gate 6 for PRs not requiring evidence-gate check"
type: source
tags: []
date: 2026-04-11
source_file: raw/prs-worldarchitect-ai/pr-6190.md
sources: []
last_updated: 2026-04-11
---

## Summary
- Gate 6 (evidence review) permanently fails for PRs that don't touch `testing_mcp/**` or `testing_ui/**`
- `evidence-gate.yml` only triggers on those paths — so no evidence check-run exists for other PRs
- `evidence-review-bot` is not a real GitHub user — approval path is also unavailable
- Result: PRs like #6179 (touching only `mvp_site/`) are permanently blocked at Gate 6

## Metadata
- **PR**: #6190
- **Merged**: 2026-04-11
- **Author**: jleechan2015
- **Stats**: +23/-1 in 2 files
- **Labels**: none

## Connections
