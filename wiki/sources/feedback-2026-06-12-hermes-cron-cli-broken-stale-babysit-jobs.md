---
title: "Hermes cron CLI broken + stale babysit jobs accumulate (2026-06-12)"
type: source
tags: [hermes, cron, cli-broken, jobs.json, babysit-jobs, slack-spam, channel-deleted, prod-gateway]
date: 2026-06-12
source_file: raw/feedback_2026-06-12_hermes_cron_cli_broken_stale_babysit_jobs.md
---

## Summary
Two related Hermes cron findings (2026-06-12, prod `~/.hermes_prod`): (1) `hermes cron list`/`pause` CLI crashes because at least one job in `cron/jobs.json` has `schedule` as a plain string instead of a dict — fall back to editing `cron/jobs.json` directly (CLAUDE.md documented exception); (2) per-session AO "babysit/progress-tick" jobs accumulate and go stale, spamming `gateway.error.log` with `channel_not_found` errors when the target Slack channel is deleted/renamed or the bot is removed.

## Key Claims
- `hermes cron list` crashes with `AttributeError: 'str' object has no attribute 'get'` at `hermes_cli/cron.py:61`
- Workaround: edit `cron/jobs.json` directly — target the **prod** copy `~/.hermes_prod/cron/jobs.json` for the running `ai.hermes.prod` gateway
- To disable a job: set `enabled: false` + add `paused_at` (ISO) + `paused_reason`; back up first with `cp cron/jobs.json cron/jobs.json.bak-$(date +%s)`
- Stale per-session AO babysit jobs (e.g. `babysit-wa-2248-…`, `wa-2302-progress-tick`) post every 5 min even after the session ends
- Leave jobs whose session file under `~/.agent-orchestrator/*/sessions/<wa-id>` was touched recently — only disable ones whose session is stale AND that error every tick
- Scheduler runs in-gateway (`cron.scheduler`), not the Python CLI — verify a JSON edit takes effect live by watching `gateway.error.log` for the next 5-min fire

## Key Quotes
> "Fall back to editing `cron/jobs.json` directly (this is a CLAUDE.md *permitted exception*: 'cron/jobs.json — live job management, documented exception')."

> "On 2026-06-12, 4 of 6 such jobs were already `enabled:false`; `d3d8c509414f` (wa-2302, session idle ~10h, channel `C0AH3RY3DK6` gone) was still firing — disabled it via direct JSON edit."

## Connections
- [[HermesCron]] — broken CLI + jobs.json direct-edit fallback
- [[AOBabysitJobs]] — per-session progress-tick accumulation
- [[SlackChannelDeleted]] — channel_not_found root cause
- [[CoderrabbitStall]] — related admin-override pattern
- [[ProdGateway]] — ~/.hermes_prod is the live target
