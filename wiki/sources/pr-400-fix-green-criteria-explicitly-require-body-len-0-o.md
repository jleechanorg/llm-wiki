---
title: "PR #400: fix(green-criteria): explicitly require body_len > 0 or confirming comment for CR APPROVED condition 3 (orch-jp8u)"
type: source
tags: []
date: 2026-03-25
source_file: raw/prs-worldai_claw/pr-400.md
sources: []
last_updated: 2026-03-25
---

## Summary
Bug orch-jp8u: workers performing their own 6-point green check via `/agento_report` read condition 4 which previously said `state == APPROVED AND body length > 0`. This single-condition check always fails because CodeRabbit consistently posts APPROVED reviews with `body=0` (body_len is always 0 on the APPROVED review itself — the walkthrough appears in a preceding COMMENTED review). As a result, `/agento_report` would always flag `NO_CR` even for genuine approvals.

The correct two-path detecti

## Metadata
- **PR**: #400
- **Merged**: 2026-03-25
- **Author**: jleechan2015
- **Stats**: +6/-2 in 1 files
- **Labels**: none

## Connections
