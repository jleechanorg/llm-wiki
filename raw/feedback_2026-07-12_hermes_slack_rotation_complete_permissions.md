---
name: Hermes Slack credential rotation requires three token classes and full scope baseline
description: Reinstalling rotates OAuth credentials but not the Socket Mode app token; provision permissions first and test from the sourced runtime shell.
type: feedback
bead: jleechan-j1qt
---

## Classification
Mandatory

## Context
During Hermes Slack credential rotation on 2026-07-12, bot and user OAuth tokens were replaced after app reinstall, but `SLACK_APP_TOKEN` remained invalid. Initial direct file-value tests passed for `xoxb` and `xoxp`, while Hermes later exposed that the Socket Mode `xapp` token was still stale. The relevant production environment is loaded from `~/.bashrc`, with `~/.hermes/scripts/launchd-env-wrapper.sh` re-extracting key Slack variables from that file.

## Durable rule
Before install/reinstall, use the workspace-scoped app manifest to establish the full Hermes Slack baseline: bot OAuth scopes `app_mentions:read`, `assistant:write`, `channels:history`, `channels:read`, `chat:write`, `commands`, `files:read`, `files:write`, `groups:history`, `groups:read`, `im:history`, `im:read`, `im:write`, and `users:read`; Socket Mode; interactivity; events `app_mention`, `message.channels`, `message.groups`, `message.im`, `assistant_thread_started`, and `assistant_thread_context_changed`; and an app-level `connections:write` token.

Rotate all three token classes: bot (`xoxb`), user/MCP (`xoxp`, where enabled), and Socket Mode (`xapp`). App reinstall rotates bot/user OAuth tokens but does not replace an app-level token automatically.

## Fix
FIX: Created `~/.claude/skills/hermes-slack-rotation/SKILL.md` on 2026-07-12. It documents the permission baseline, secure dotfile update map, and exact verification path.

## Verification
Use a clean shell that sources `~/.bashrc`; require `auth.test` to return `ok:true` for bot and user tokens, and `apps.connections.open` to return `ok:true` for the `xapp` token. Inspect `x-oauth-scopes` response headers to prove granted scopes. Run Hermes doctor, health, and LaunchAgent checks afterwards, and classify any restart/registration error separately from token validity.

## References
- `~/.claude/skills/hermes-slack-rotation/SKILL.md`
- `~/.hermes/scripts/launchd-env-wrapper.sh`
- `~/.claude/projects/-Users-jleechan-.hermes/memory/feedback_2026-07-12_hermes_slack_rotation_complete_permissions.md`
