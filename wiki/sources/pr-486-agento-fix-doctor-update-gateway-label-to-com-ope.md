---
title: "PR #486: [agento] fix(doctor): update GATEWAY_LABEL to com.openclaw.gateway"
type: source
tags: []
date: 2026-04-04
source_file: raw/prs-worldai_claw/pr-486.md
sources: []
last_updated: 2026-04-04
---

## Summary
PR #485 renamed the production gateway launchd label from `ai.openclaw.gateway` to `com.openclaw.gateway`, but `scripts/doctor.sh` line 9 still had the old label. This caused monitor-agent to report `STATUS=PROBLEM` with 4 FAIL checks despite the gateway being healthy.

## Metadata
- **PR**: #486
- **Merged**: 2026-04-04
- **Author**: jleechan2015
- **Stats**: +255/-132 in 2 files
- **Labels**: none

## Connections
