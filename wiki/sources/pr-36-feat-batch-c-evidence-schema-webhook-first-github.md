---
title: "PR #36: feat(batch-c): evidence schema + webhook-first GitHub integration"
type: source
tags: []
date: 2026-03-05
source_file: raw/prs-worldai_claw/pr-36.md
sources: []
last_updated: 2026-03-05
---

## Summary
- Defines a generalized EvidencePacket schema (src/orchestration/evidence.py) for auditable execution proof at each pipeline stage.
- Adds webhook parsing helpers to gh_integration.py for normalizing GitHub event payloads.
- Extends webhook_bridge.py with receive_github_event() (trusted-actor gate, HMAC validation) and current_github_event_mode() (auto-detects webhook vs polling).
- Adds .github/workflows/agent-pr-trigger.yml: self-contained GitHub Actions webhook-first trigger; no external serv

## Metadata
- **PR**: #36
- **Merged**: 2026-03-05
- **Author**: jleechan2015
- **Stats**: +2176/-0 in 6 files
- **Labels**: none

## Connections
