---
title: "PR #414: [agento] [P1] fix(doctor.sh): 3 health-check improvements (bd-yk9h, bd-23ej, bd-oueo)"
type: source
tags: []
date: 2026-03-27
source_file: raw/prs-worldai_claw/pr-414.md
sources: []
last_updated: 2026-03-27
---

## Summary
Three independent `doctor.sh` / `monitor-agent.sh` health-check fixes bundled in one PR:

- **bd-yk9h**: `detect_ao_dashboard_port()` hardcoded fallback `3011`; actual AO dashboard port is `3020`. Fixed to read `agent-orchestrator.yaml` first, defaulting to `3020`.
- **bd-23ej**: `monitor-agent.sh` token probe reported `FAIL:gateway.auth.token:health_http=000` when the gateway is down (connection refused). Fixed to distinguish `http=000` → `FAIL:gateway.down:connection_refused`.
- **bd-oueo**: R

## Metadata
- **PR**: #414
- **Merged**: 2026-03-27
- **Author**: jleechan2015
- **Stats**: +75/-40 in 2 files
- **Labels**: none

## Connections
