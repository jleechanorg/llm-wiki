---
name: hermes-cron-cli-broken-stale-babysit-jobs
description: hermes cron list/pause crashes on a job whose schedule is a string; disable stale per-session AO babysit tick jobs by editing cron/jobs.json directly (documented exception)
metadata: 
  node_type: memory
  type: feedback
  originSessionId: c594d4f0-a942-4271-85f6-5407a3c1d6e6
---

Two related Hermes cron findings (2026-06-12, prod `~/.hermes_prod`).

## 1. `hermes cron list` / `pause` CLI is broken
`hermes cron list` (and therefore `pause <id>`, which looks up via list) crashes:
```
AttributeError: 'str' object has no attribute 'get'
  hermes_cli/cron.py:61  schedule = job.get("schedule_display", job.get("schedule", {}).get("value", "?"))
```
Root cause: at least one job in `cron/jobs.json` has `schedule` as a **plain string** instead of a dict, so `.get("value")` blows up and takes the whole listing down. Until that's fixed in `hermes_cli/cron.py`, the cron CLI cannot manage jobs — **fall back to editing `cron/jobs.json` directly** (this is a CLAUDE.md *permitted exception*: "cron/jobs.json — live job management, documented exception"). Target the **prod** copy `~/.hermes_prod/cron/jobs.json` for the running `ai.hermes.prod` gateway, not `~/.hermes/cron/jobs.json`.

To disable a job, match the existing disabled-job shape: set `enabled: false` and add `paused_at` (ISO) + `paused_reason`. Back up first (`cp cron/jobs.json cron/jobs.json.bak-$(date +%s)`).

## 2. Per-session AO "babysit/progress-tick" jobs accumulate and go stale
AO dispatch creates per-session recurring cron jobs (`every 5m`) named like `babysit-wa-2248-…`, `wa-2302-progress-tick`, that post progress to a specific Slack channel/thread. When the session finishes they're supposed to be disabled, but some get orphaned and **keep firing every 5 min**, spamming `gateway.error.log`:
```
ERROR cron.scheduler: Job '<id>': delivery error: Slack API error: channel_not_found
```
(the target channel was deleted/renamed or the bot was removed). On 2026-06-12, 4 of 6 such jobs were already `enabled:false`; `d3d8c509414f` (wa-2302, session idle ~10h, channel `C0AH3RY3DK6` gone) was still firing — disabled it via direct JSON edit. **Leave jobs whose session file under `~/.agent-orchestrator/*/sessions/<wa-id>` was touched recently** (e.g. wa-2307 active within the hour) — only disable ones whose session is stale AND that error every tick.

Gateway pickup: the scheduler runs in-gateway (`cron.scheduler`), not the Python CLI — verify a JSON edit takes effect live by watching `gateway.error.log` for the next 5-min fire; if it re-fires, the job is cached and needs a gateway reload/restart.

Related: [[slack-wrong-thread-root-cause]], [[coderabbit-dismissed-stuck-admin-override]].
