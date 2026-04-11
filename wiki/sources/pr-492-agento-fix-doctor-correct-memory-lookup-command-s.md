---
title: "PR #492: [agento] fix(doctor): correct memory lookup command + skip when mem0 disabled"
type: source
tags: []
date: 2026-04-04
source_file: raw/prs-worldai_claw/pr-492.md
sources: []
last_updated: 2026-04-04
---

## Summary
doctor.sh fails with `[FAIL] Memory lookup command failed (rc=1)` on every run, causing monitor STATUS=PROBLEM. Two bugs:
1. Wrong command: `openclaw mem0 search` does not exist — correct is `openclaw memory search`
2. Missing disabled-plugin skip: when mem0 is intentionally disabled, output says plugin-disabled but rc=1. monitor-agent.sh handles this at line 671; doctor.sh was missing it.

## Metadata
- **PR**: #492
- **Merged**: 2026-04-04
- **Author**: jleechan2015
- **Stats**: +6/-1 in 2 files
- **Labels**: none

## Connections
