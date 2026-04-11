---
title: "PR #121: feat: simplify mctrl orchestration — remove cross-repo dispatch, outbox retry/dead-letter, proof payload"
type: source
tags: []
date: 2026-03-13
source_file: raw/prs-worldai_claw/pr-121.md
sources: []
last_updated: 2026-03-13
---

## Summary
This PR trims the mctrl orchestration stack back to its essential responsibilities: spawn an agent, watch it, notify on completion. Everything added "for future use" or that duplicated higher-level system concerns (retry queues, proof payloads, multi-registry fan-out, terminal archival) is removed.

- **−1357 / +132 lines** across 8 files
- No new functionality — only removal and hardening of the core path

---

## Metadata
- **PR**: #121
- **Merged**: 2026-03-13
- **Author**: jleechan2015
- **Stats**: +219/-1357 in 8 files
- **Labels**: none

## Connections
