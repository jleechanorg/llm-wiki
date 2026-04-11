---
title: "PR #168: fix(webhook): handle check_suite.completed events without PR association"
type: source
tags: []
date: 2026-03-16
source_file: raw/prs-worldai_claw/pr-168.md
sources: []
last_updated: 2026-03-16
---

## Summary
- Handle check_suite.completed and check_run.completed webhook events that are not associated with a PR (e.g., CI runs on main branch commits)
- Previously these events were silently dropped at the webhook bridge level

## Metadata
- **PR**: #168
- **Merged**: 2026-03-16
- **Author**: jleechan2015
- **Stats**: +148/-22 in 5 files
- **Labels**: none

## Connections
