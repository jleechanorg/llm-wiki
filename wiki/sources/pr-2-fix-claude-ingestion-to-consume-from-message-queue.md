---
title: "PR #2: Fix Claude ingestion to consume from message_queue"
type: source
tags: []
date: 2025-11-29
source_file: raw/prs-/pr-2.md
sources: []
last_updated: 2025-11-29
---

## Summary
- Route Claude fast-path consumer to `telemetry:message_queue` (was `telemetry:events`) so it reads what hooks emit
- HTTP endpoint now enqueues into the same message queue to keep capture consistent
- AGENTS.md documents GH CLI PR workflow and notes CLAUDE.md defers here

## Metadata
- **PR**: #2
- **Merged**: 2025-11-29
- **Author**: jleechan2015
- **Stats**: +83/-73 in 17 files
- **Labels**: none

## Connections
