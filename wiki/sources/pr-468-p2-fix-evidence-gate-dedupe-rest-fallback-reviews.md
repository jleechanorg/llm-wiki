---
title: "PR #468: [P2] fix(evidence-gate): dedupe REST fallback reviews init (orch-jqh)"
type: source
tags: []
date: 2026-04-02
source_file: raw/prs-worldai_claw/pr-468.md
sources: []
last_updated: 2026-04-02
---

## Summary
Removes a duplicate `reviews = []` assignment in the GraphQL→REST fallback path in `_get_reviews()`. No behavior change — cleanup after `feat/orch-jqh` / evidence-gate work.

## Metadata
- **PR**: #468
- **Merged**: 2026-04-02
- **Author**: jleechan2015
- **Stats**: +132/-32 in 5 files
- **Labels**: none

## Connections
