---
title: "PR #543: [agento] fix(deploy): disable DM e2e in staging+prod monitor; fix upgrade-safe launchd label; fix mem0 log msg"
type: source
tags: []
date: 2026-04-11
source_file: raw/prs-worldai_claw/pr-543.md
sources: []
last_updated: 2026-04-11
---

## Summary
- **deploy.sh**: Add `OPENCLAW_MONITOR_SLACK_E2E_MATRIX_ENABLE=0` for both staging and prod monitor runs — DM e2e tests fail when both gateways share the same socket-mode app token (Slack routes DMs to whichever grabbed the WS connection first)
- **openclaw-upgrade-safe.sh**: Replace `openclaw-staging-start/stop` helper script calls with `launchctl kickstart -k ai.openclaw.staging` directly, satisfying `test_openclaw_upgrade_safe_uses_staging_launchagent_not_deleted_helper`
- **extensions/opencl

## Metadata
- **PR**: #543
- **Merged**: 2026-04-11
- **Author**: jleechan2015
- **Stats**: +9/-43 in 4 files
- **Labels**: none

## Connections
