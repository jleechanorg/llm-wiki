---
title: "PR #707: fix: harden in-memory rate limit retention"
type: source
tags: [codex]
date: 2025-11-13
source_file: raw/prs-/pr-707.md
sources: []
last_updated: 2025-11-13
---

## Summary
- track per-identifier windows so the in-memory limiter keeps the full hourly/daily history and cleanly removes entries when limits reset
- extend the shared rate-limit tests to cover cleanup behaviour, align backend tests with the current dev/test defaults, and drop the unused RATE_LIMIT_FORCE_NON_DISTRIBUTED env hook
- update the public rate-limit response doc to reflect the real authenticated tiers and call out that production loads its values from Secret Manager

## Metadata
- **PR**: #707
- **Merged**: 2025-11-13
- **Author**: jleechan2015
- **Stats**: +74/-53 in 7 files
- **Labels**: codex

## Connections
