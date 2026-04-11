---
title: "PR #429: [agento] fix(ci): treat cancelled check runs as neutral in CI gate"
type: source
tags: []
date: 2026-03-29
source_file: raw/prs-worldai_claw/pr-429.md
sources: []
last_updated: 2026-03-29
---

## Summary
- skeptic-cron.yml: jq filter now treats `cancelled` as neutral alongside `success`, `skipped`, `neutral`
- Concurrency cancellation creates cancelled check runs on superseded commits — these should not count as CI failures

## Metadata
- **PR**: #429
- **Merged**: 2026-03-29
- **Author**: jleechan2015
- **Stats**: +19/-3 in 2 files
- **Labels**: none

## Connections
