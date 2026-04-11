---
title: "PR #576: feat: harden conversation MCP, rate limits, and citation guarantees"
type: source
tags: []
date: 2025-11-08
source_file: raw/prs-/pr-576.md
sources: []
last_updated: 2025-11-08
---

## Summary
- Rebuilt the conversation MCP stack so `conversation.send-message`, `conversation.add-message`, `conversation.get-history`, and `conversation.list` all preserve conversation ids, assistant replies, and metadata even under Firestore eventual consistency. Added convo delete wiring, streaming persistence fixes, and noserver-parity harnesses under `testing_integration/convo/` with evidence capture scripts.
- Hardened rate limiting by moving `RateLimitTool` into `shared-libs`, adding Secret Manager

## Metadata
- **PR**: #576
- **Merged**: 2025-11-08
- **Author**: jleechan2015
- **Stats**: +102/-11 in 3 files
- **Labels**: none

## Connections
