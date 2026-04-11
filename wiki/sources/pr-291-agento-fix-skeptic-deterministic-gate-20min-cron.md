---
title: "PR #291: [agento] fix(skeptic): deterministic gate + 20min cron with AO-powered LLM merge"
type: source
tags: []
date: 2026-03-29
source_file: raw/prs-worldai_claw/pr-291.md
sources: []
last_updated: 2026-03-29
---

## Summary
Skeptic infrastructure has been unreliable - skeptic-gate.yml polled for 28 minutes waiting for a VERDICT comment from the AO worker, but the lifecycle-worker was frequently down (launchd thrashing). This caused 10+ PRs in 24h of churn testing fixes in isolation.

User directed: make skeptic-gate pure deterministic, leave LLM inference to skeptic-cron only.

## Metadata
- **PR**: #291
- **Merged**: 2026-03-29
- **Author**: jleechan2015
- **Stats**: +277/-242 in 3 files
- **Labels**: none

## Connections
