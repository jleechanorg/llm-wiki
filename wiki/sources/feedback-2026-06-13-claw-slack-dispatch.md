---
title: "/claw now dispatches via Slack (not nohup hermes chat) — 2026-06-13"
type: source
tags: [claw, slack, hermes, dispatch, feedback, 2026-06-13]
date: 2026-06-13
source_file: raw/feedback_2026-06-13_claw_slack_dispatch.md
---

## Summary
The `/claw` slash command was patched on 2026-06-13 to dispatch tasks by posting to Slack `#claw-dispatch` (channel `C0B9W8D609M`) as user jleechan with `<@U0AEZC7RX1Q>` @hermes mentioned, replacing the broken `nohup hermes chat` spawn path. Two pre-flight gotchas were caught: the `hermes gateway status` CLI lies (use `curl :8642/health` instead), and posting as `HERMES_SLACK_BOT_TOKEN` is silently dropped by Hermes's self-message guard (use `SLACK_MCP_XOXP_TOKEN` xoxp user token).

## Key Claims
- `/claw` now posts to Slack `#claw-dispatch` and waits up to 30s for a Hermes ack (reaction OR first thread reply)
- `hermes gateway status` CLI is unreliable — use `curl -sS -m 3 http://127.0.0.1:8642/health | grep -q '"status": "ok"'` instead
- Posting with `HERMES_SLACK_BOT_TOKEN` silently fails because Hermes's `slack.py:25-28` drops messages where `user == self._bot_user_id`
- `SLACK_MCP_XOXP_TOKEN` (xoxp user token for jleechan `U09GH5BR3QU`) is the correct dispatch token
- Ack detection: 30s polling window, success = reaction on parent OR thread reply; warn + thread URL on no-ack, exit 0
- Slack dispatch is a strict improvement over `nohup hermes chat`: audit trail, multi-user coordination, lane awareness, no tmux death, no CLI lies

## Key Quotes
> "The CLI reports 'not running' / 'draining for shutdown' with phantom PID 3168 while the actual gateway is healthy on port 8642."

> "If you post AS Hermes, the message's `user` field equals Hermes's `self._bot_user_id`. Hermes drops the message before it reaches the agent. You get a successful `chat.postMessage` API response, but Hermes never sees the task and the PR stalls silently with no error."

## Constants
| What | Value |
|---|---|
| Dispatch channel | `C0B9W8D609M` (#claw-dispatch) |
| Hermes bot user_id | `U0AEZC7RX1Q` |
| User (jleechan) | `U09GH5BR3QU` |
| Hermes home channel | `C0AJQ5M0A0Y` (#ai-general) |
| Workspace | jleechanai.slack.com (team T09FXQ4LCQP) |
| Slack `require_mention` | `false` (global) |

## Connections
- [[HermesGateway]] — gateway health endpoint replaces the lying CLI
- [[HermesSlackAdapter]] — slack.py self-message guard at lines 25-28
- [[ClawDispatchSkill]] — patched implementation at `~/.claude/skills/claw-dispatch/SKILL.md`
- [[SlackSocketMode]] — Hermes connected to Slack via Socket Mode
- [[SLACK_MCP_XOXP_TOKEN]] — correct dispatch token
- [[HERMES_SLACK_BOT_TOKEN]] — wrong token; messages silently dropped
- [[feedback-2026-06-12-local-claude-session-can-runaway-push]] — related runaway-prevention work
- [[ColimaMigration]] — same session context (jleechanorg runners)
