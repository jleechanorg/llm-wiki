---
title: "PR #90: mctrl: add outbox dead-letter, retry bounds, and status telemetry"
type: source
tags: []
date: 2026-03-11
source_file: raw/prs-worldai_claw/pr-90.md
sources: []
last_updated: 2026-03-11
---

## Summary
- add bounded retry + dead-letter handling for mctrl outbox delivery failures
- add supervisor outbox health alerting (backlog/age/dead-letter) with cooldown
- extend `mctrl status` output to include outbox/dead-letter/retry telemetry
- add TDD coverage for notifier, supervisor alert cooldown, and status output

## Metadata
- **PR**: #90
- **Merged**: 2026-03-11
- **Author**: jleechan2015
- **Stats**: +1275/-739 in 14 files
- **Labels**: none

## Connections
