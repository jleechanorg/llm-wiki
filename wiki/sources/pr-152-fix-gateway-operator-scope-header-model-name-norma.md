---
title: "PR #152: fix(gateway): operator scope header + model name normalization + agent routing (wc-4sn, wc-6ol, wc-on8)"
type: source
tags: []
date: 2026-03-30
source_file: raw/prs-worldai_claw/pr-152.md
sources: []
last_updated: 2026-03-30
---

## Summary
Three related gateway issues were causing turn pipeline failures and lifecycle test failures:
- **wc-4sn**: Turn pipeline 502 — SSE tests skipped due to OPENCLAW_UNAVAILABLE
- **wc-6ol**: OpenClaw model contract mismatch — backend stripping model prefix causing HTTP 400
- **wc-on8**: Lifecycle acceptance video test needed to prove end-to-end turn flow works

Root cause: backend used campaign UUID as gateway agent routing key. The local OpenClaw gateway waits 120s for a session registered to that

## Metadata
- **PR**: #152
- **Merged**: 2026-03-30
- **Author**: jleechan2015
- **Stats**: +330/-33 in 14 files
- **Labels**: none

## Connections
