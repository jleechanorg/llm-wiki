---
name: worldarchitect skeptic lifecycle churn root cause
description: Skeptic failures can hide multiple layers: SCM config skip, watchdog false missing detection, and start-all 5-minute worker resets versus 10-minute skeptic cron.
type: feedback
bead: bd-5h5s
---

# worldarchitect skeptic lifecycle churn root cause

On 2026-05-04, `worldarchitect.ai` skeptic automation appeared to be always failing or silent after prior work claimed the missing `scm:` project config was fixed.

The complete root cause was layered:

1. `runLocalSkepticCron()` returned `0` when `project.scm` was absent, so adding `scm: { plugin: github }` to the `worldarchitect` project config was necessary.
2. `lw-watchdog.sh` used shell `case` matching as if `[[:space:]]+` were a regex. In shell globs, `+` is literal, so live workers like `node ... ao lifecycle-worker worldarchitect` were not detected.
3. `ai.agento.lifecycle-all` has `StartInterval=300`, and `start-all.sh` killed existing lifecycle workers by default every time it ran. Since local skeptic cron is throttled to 10 minutes, a 5-minute worker reset cadence could prevent reliable evaluation.

The durable fix was to make `lw-watchdog.sh` use `grep -E` for exact lifecycle-worker matching and make `start-all.sh` skip already-running workers by default, with explicit restart only via `AO_START_RESTART_EXISTING=1`.

Verification included:

- Manual `scripts/start-all.sh worldarchitect` preserved the existing worker PID and printed "lifecycle-worker already running".
- `~/.openclaw/logs/lw-watchdog.log` logged repeated `HEALTHY_DORMANT` entries after the fix.
- Direct `ao skeptic verify --repo jleechanorg/worldarchitect.ai -n 6801 --dry-run` completed with real `VERDICT: FAIL`, proving remaining failures were PR-gate failures rather than infrastructure skips.

Reusable rule: before debugging an AO cron feature, verify worker uptime exceeds the feature cadence and that watchdog/start-all paths are not resetting the process.

