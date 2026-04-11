---
title: "PR #491: fix(harness): add protected openclaw.json keys — heartbeat.every must stay 5m"
type: source
tags: []
date: 2026-04-04
source_file: raw/prs-worldai_claw/pr-491.md
sources: []
last_updated: 2026-04-04
---

## Summary
On 2026-04-04, an agent changed agents.defaults.heartbeat.every from 5m to 30m in ~/.openclaw/openclaw.json. This caused doctor.sh to FAIL on every monitor run and the monitor-agent to report STATUS=PROBLEM. The constraint existed only in doctor.sh — no agent instruction stated the value was protected.

Root cause (from /harness analysis): agents mutate openclaw.json without knowing which keys doctor.sh validates. The constraint knowledge was absent from any file agents read before writing.

Rel

## Metadata
- **PR**: #491
- **Merged**: 2026-04-04
- **Author**: jleechan2015
- **Stats**: +12/-0 in 1 files
- **Labels**: none

## Connections
