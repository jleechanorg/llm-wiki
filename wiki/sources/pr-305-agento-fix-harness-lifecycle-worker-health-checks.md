---
title: "PR #305: [agento] fix(harness): lifecycle-worker health checks + start-all.sh pgrep fix (bd-rbgp)"
type: source
tags: []
date: 2026-03-30
source_file: raw/prs-worldai_claw/pr-305.md
sources: []
last_updated: 2026-03-30
---

## Summary
Workers stopped handling CR (CodeRabbit) CHANGES_REQUESTED comments on 4 PRs (#302, #301, #299, #273). Manual `ao review-check` was needed to detect. Root cause: lifecycle-worker death goes undetected, and `start-all.sh` idempotency had a pgrep false-positive.

## Metadata
- **PR**: #305
- **Merged**: 2026-03-30
- **Author**: jleechan2015
- **Stats**: +88/-3 in 3 files
- **Labels**: none

## Connections
