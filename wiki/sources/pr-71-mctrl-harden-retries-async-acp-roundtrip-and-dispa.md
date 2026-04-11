---
title: "PR #71: mctrl: harden retries, async ACP roundtrip, and dispatch env isolation"
type: source
tags: []
date: 2026-03-10
source_file: raw/prs-worldai_claw/pr-71.md
sources: []
last_updated: 2026-03-10
---

## Summary
- harden notifier delivery with transient retry/backoff and shared outbox defaults
- align reconciliation/supervisor wait windows with notifier runtime budget
- make `test_mcp_dispatch_roundtrip` async and validate full real ACP roundtrip behavior
- fix dispatch subprocess environment so `ai_orch` works under `PYTHONPATH=src`

## Metadata
- **PR**: #71
- **Merged**: 2026-03-10
- **Author**: jleechan2015
- **Stats**: +346/-227 in 6 files
- **Labels**: none

## Connections
