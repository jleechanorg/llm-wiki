---
title: "worldarchitect skeptic lifecycle churn root cause"
type: source
date: 2026-05-04
tags: [agent-orchestrator, worldarchitect.ai, skeptic-gate, lifecycle-worker, launchd, watchdog]
---

# worldarchitect skeptic lifecycle churn root cause

`worldarchitect.ai` skeptic automation looked broken for more than one reason.

The initial fix, adding `scm: { plugin: github }` to the `worldarchitect` AO project config, was necessary because `runLocalSkepticCron()` silently returns `0` when it cannot resolve an SCM plugin with `listOpenPRs`.

But the worker still failed to behave reliably because lifecycle infrastructure was resetting it:

- `lw-watchdog.sh` used shell `case` matching as if `[[:space:]]+` were regex, so exact worker detection failed.
- `ai.agento.lifecycle-all` runs every 5 minutes through launchd.
- `start-all.sh` killed existing lifecycle workers by default on each run.
- Local skeptic cron is throttled to 10 minutes, so a 5-minute restart loop can erase in-memory throttle/dedup state before the cron completes reliably.

Fix:

- Use `grep -E` for exact lifecycle-worker detection in `lw-watchdog.sh`.
- Make `start-all.sh` skip already-running workers by default.
- Require `AO_START_RESTART_EXISTING=1` for deliberate restarts.

Verification:

- Manual `scripts/start-all.sh worldarchitect` preserved the existing `worldarchitect` worker PID.
- Watchdog logged repeated `HEALTHY_DORMANT` after the fix.
- Direct `ao skeptic verify --repo jleechanorg/worldarchitect.ai -n 6801 --dry-run` produced a real `VERDICT: FAIL`, separating infrastructure recovery from legitimate PR-gate failures.

## Reusable Lesson

Before debugging a cron feature inside a daemon, confirm daemon uptime exceeds the cron cadence and that health automation is not resetting the process on a shorter interval.

