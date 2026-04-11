---
title: "PR #32: feat(orchestration): thread ack watcher + in-process MC poller runtime"
type: source
tags: []
date: 2026-03-04
source_file: raw/prs-worldai_claw/pr-32.md
sources: []
last_updated: 2026-03-04
---

## Summary
- add deterministic Slack thread mention ack watcher + session tail helper and related launch wiring
- run Mission Control task polling in-process with backend service lifecycle (single supervised service)
- harden task dispatch for null task text fields (`title`/`description`) to prevent poller crashes
- update runtime/startup wiring so backend service includes required MC env for poller

## Metadata
- **PR**: #32
- **Merged**: 2026-03-04
- **Author**: jleechan2015
- **Stats**: +2579/-26 in 20 files
- **Labels**: none

## Connections
