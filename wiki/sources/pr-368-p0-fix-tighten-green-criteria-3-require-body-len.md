---
title: "PR #368: [P0] fix: tighten green criteria #3 — require body_len > 0 for genuine CR APPROVED"
type: source
tags: []
date: 2026-03-23
source_file: raw/prs-worldai_claw/pr-368.md
sources: []
last_updated: 2026-03-23
---

## Summary
Workers checking condition 3 against the criteria list in `agent-orchestrator.yaml` skipped the `body_len > 0` check, since that logic only appeared in trigger messages (lines 369, 375), not in the criteria definition itself.

Evidence: PR #361 (jc-491) saw `state: APPROVED, body_len: 0` and workers declared green without running the genuine-detection jq command.

## Metadata
- **PR**: #368
- **Merged**: 2026-03-23
- **Author**: jleechan2015
- **Stats**: +1/-1 in 1 files
- **Labels**: none

## Connections
