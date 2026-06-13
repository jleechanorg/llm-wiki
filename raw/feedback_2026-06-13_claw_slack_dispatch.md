---
name: feedback-2026-06-13-claw-slack-dispatch
description: /claw now posts to Slack
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 33b6218a-1fc0-42b9-b4f8-1814474904eb
---

# /claw now dispatches via Slack (not nohup hermes chat)

**Date:** 2026-06-13
**Context:** User said "lets use change /claw to use slack. It can use the #claw-dispatch channel and tag @hermes to do work" + "post as me" — replacing the broken `nohup hermes chat` path.
**Lesson:** Two gotchas caught at planning that would have silently broken the dispatcher.

## What /claw does now (patched 2026-06-13)

`/claw <task>` → posts to **#claw-dispatch** (channel id `C0B9W8D609M`) on `jleechanai.slack.com` as the user **jleechan** (U09GH5BR3QU), with `<@U0AEZC7RX1Q>` @hermes mentioned. Hermes (already connected to Slack via Socket Mode, `require_mention: false` global) sees it, reacts ✅, and replies in thread. /claw prints the thread URL and waits up to 30s for an ack (reaction OR first thread reply).

Implementation: `~/.claude/skills/claw-dispatch/SKILL.md` — replaces the `nohup hermes chat -q ...` spawn (was lines 240-256) with a `curl POST chat.postMessage` to Slack Web API.

## GOTCHA #1 — `hermes gateway status` CLI lies

The skill body's pre-flight check (was lines 88-98) used to hard-fail on `grep -q 'Gateway is running'` against the CLI output. The CLI reports "not running" / "draining for shutdown" with phantom PID 3168 while the actual gateway is healthy on port 8642 (`curl :8642/health` returns `{"status":"ok"}`, `gateway_state.json` says `running`).

**Fix:** replaced the CLI check with `curl -sS -m 3 http://127.0.0.1:8642/health | grep -q '"status": "ok"'`. Trust the live health endpoint, not the CLI.

## GOTCHA #2 — HERMES_SLACK_BOT_TOKEN cannot post to Hermes

I almost picked this token (it does exist in env, and `auth.test` confirms it IS Hermes's bot token). It is **the wrong choice**. The Hermes slack adapter at `gateway/platforms/slack.py:25-28` has:

```python
# Always ignore our own messages to prevent echo loops
msg_user = event.get("user", "")
if msg_user and self._bot_user_id and msg_user == self._bot_user_id:
    return
```

If you post AS Hermes, the message's `user` field equals Hermes's `self._bot_user_id` (both are `U0AEZC7RX1Q`). Hermes drops the message before it reaches the agent. You get a successful `chat.postMessage` API response, but Hermes never sees the task and the PR stalls silently with no error.

**Right token:** `SLACK_MCP_XOXP_TOKEN` — xoxp user token for jleechan (U09GH5BR3QU). Posts as the user with @hermes mentioned. Hermes sees a different `user` field and processes it.

**Why not SLACK_WEBHOOK_URL:** webhooks can't mention specific users (only @channel/@here). Hermes wouldn't get a personal notification, may not respond.

## Channel / bot constants (jleechanai.slack.com, team T09FXQ4LCQP)

| What | Value | Source |
|---|---|---|
| Dispatch channel | `C0B9W8D609M` (#claw-dispatch) | user-specified, created 2026-06-13 |
| Hermes bot user_id | `U0AEZC7RX1Q` | `auth.test` on HERMES_SLACK_BOT_TOKEN |
| Hermes bot_id | `B0AEHUEA0JK` | same |
| User (jleechan) | `U09GH5BR3QU` | `auth.test` on SLACK_MCP_XOXP_TOKEN |
| Hermes home channel | `C0AJQ5M0A0Y` (#ai-general) | `slack.home_channel` in `~/.hermes_prod/config.yaml` |
| Workspace | jleechanai.slack.com | `auth.test` |
| Slack `require_mention` | `false` (global) | config — Hermes responds without @mention in any channel it's a member of |

## Slack dispatch message format

```
[via /claw] <@U0AEZC7RX1Q> <task_description>
```

The `[via /claw]` provenance tag makes the dispatch source obvious in the channel log. The mention is stripped by slack.py line 240 before the model sees the text.

## Ack detection (30s window)

Polled every 1s for 30s. Two success conditions:
1. **Reaction on parent message** — Hermes typically adds ✅ ("white_check_mark") or another emoji as visual ack
2. **Reply in thread** — Hermes often posts text like "On it…" or starts the work

If neither lands in 30s, /claw prints a warning + the thread URL, exits 0 (the message is durable in the channel; the user can monitor the thread).

**Caveat:** when Hermes is busy with other work (e.g. multiple AO workers running), the first reaction can land 25-30s after the post. The 30s window is a trade-off between fail-fast visibility and Hermes's queue depth. If you see frequent "no ack" warnings while Hermes is processing, the task is probably fine — check the thread.

## env-var precedence in the dispatcher

```bash
CLAW_CHANNEL="${CLAW_CHANNEL:-C0B9W8D609M}"     # override at runtime
CLAW_BOT_ID="${CLAW_BOT_ID:-U0AEZC7RX1Q}"        # override at runtime
CLAW_TOKEN="${SLACK_MCP_XOXP_TOKEN:-${HERMES_SLACK_USER_TOKEN:-}}"  # required, no usable default
```

## Verification commands (for re-testing after any change)

```bash
# 1. Pre-flight (gateway health)
curl -sS -m 3 http://127.0.0.1:8642/health
# expect: {"status": "ok", "platform": "hermes-agent"}

# 2. Token identity
curl -sS -m 5 -H "Authorization: Bearer $SLACK_MCP_XOXP_TOKEN" \
  https://slack.com/api/auth.test
# expect: user=jleechan, user_id=U09GH5BR3QU

# 3. Channel membership
curl -sS -m 5 -H "Authorization: Bearer $HERMES_SLACK_BOT_TOKEN" \
  "https://slack.com/api/conversations.info?channel=C0B9W8D609M"
# expect: is_member=true, is_archived=false

# 4. End-to-end dispatch (uses the patched SKILL body)
ARGUMENTS="[test] please ack and reply with current UTC time" bash /tmp/claw-test.sh
# expect: ✅ Dispatched to Hermes via Slack + thread URL + ✅ Hermes acked (within 30s)
```

## Why this is better than the old nohup hermes chat path

- **Audit trail** — every dispatch is a Slack message, pinned-able, searchable, linkable
- **Human-in-loop visibility** — anyone watching #claw-dispatch sees the task, the ack, the work, the result
- **Multi-user coordination** — if jleechan2015 and jleechan both /claw, the channel shows who's asking what
- **Liveness** — Slack is the source of truth; no separate tmux session to die
- **Lane awareness** — a /claw dispatch appears in the channel BEFORE the work starts, so conflicts with other open PRs in the same files are visible to all watchers
- **No more "Hermes was actually up but CLI said no"** — health check is curl, not a CLI that lies

## Out of scope (mentioned to user, not done)

- Migrate `/repro`, `/orch`, etc. to the same Slack pattern — separate PR
- Fix the broken `hermes gateway status` CLI — Hermes bug, not /claw
- Move dispatch to Hermes home channel #ai-general — user chose #claw-dispatch

## Source-of-truth order (extends dashboard-lags-tmux, echo-loop avoidance)

1. `gh pr view` (real PR head SHA + mergeable state)
2. `git -C <worktree> log` (real commits)
3. **Slack thread URL** (real-time dispatch + result, single source of truth for /claw)
4. `tmux capture-pane -t <name>` (real conversation for AO workers — only relevant if NOT using /claw)
5. `ao status` (lifecycle state — useful but lagging)
6. AO dashboard (decorative, do not drive decisions off it)
7. **`hermes gateway status` CLI — LIES, do not trust** (use `curl :8642/health` instead)
8. **Posting as HERMES_SLACK_BOT_TOKEN to a channel where Hermes is a member — LIES, message is dropped** (use xoxp user token)
