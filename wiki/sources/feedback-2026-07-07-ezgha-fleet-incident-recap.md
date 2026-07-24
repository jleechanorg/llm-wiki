---
title: "ezgha fleet incident recap (2026-07-07)"
type: source
tags: [ez-gh-actions, ezgha, watchdog, github-actions, fleet]
date: 2026-07-07
bead: ez-gh-actions-2ik
---

Raw ingest of Codex memory `feedback_2026-07-07_ezgha_fleet_incident_recap_2026_07_07.md`.

See [[EzGhaDaemon]] for entity context.

## Key claims

1. systemd `WatchdogSec` SIGABRT ≠ external `ezgha-watchdog.timer` fleet script.
2. Long `gh api` + batch `ensure_count` exceeded watchdog window until pings + 300s ([045cd66](https://github.com/jleechanorg/ez-gh-actions/commit/045cd66)).
3. Hard reset (docker rm all + slot wipe) wedges on GitHub `offline+busy` runners; DELETE returns 422 until job cancelled.
4. Mac Colima requires `minimum_isolation=container` in config ([1f3948f](https://github.com/jleechanorg/ez-gh-actions/commit/1f3948f)).
5. Queue tail saturation had zero completed-job runner failures across 20 PRs — capacity not crash.
6. Soft reset only: `systemctl --user restart ezgha.service` / `launchctl kickstart -k`.

**Jeffrey oracle:** NO

[[../../raw/feedback_2026-07-07_ezgha_fleet_incident_recap.md|Full source]]
