---
title: "Hermes Slack credential rotation requires three token classes and full scope baseline"
type: source
tags: [slack, hermes, credentials, rotation, oauth, socket-mode, launchd, bashrc]
sources:
  - raw/feedback_2026-07-12_hermes_slack_rotation_complete_permissions.md
last_updated: 2026-07-12
---

## Summary
Reinstalling the Slack app rotates bot and user OAuth tokens but does NOT rotate the Socket Mode `xapp` app-level token, so a "successful" reinstall can still leave Hermes runtime-broken. Fix: before any install/reinstall, establish the full Hermes Slack baseline from the workspace-scoped app manifest (13 bot OAuth scopes, Socket Mode, interactivity, six event subscriptions, plus an app-level `connections:write` token), and rotate all three token classes (`xoxb`, `xoxp` where enabled, and `xapp`). Verify from a clean shell that sources `~/.bashrc`, which is the same shell discipline `~/.hermes/scripts/launchd-env-wrapper.sh` uses to re-extract Slack vars.

## Key Claims
- Hermes Slack runtime depends on THREE token classes, not two: bot (`xoxb`), user/MCP (`xoxp`, where enabled), and Socket Mode (`xapp`). Skipping any class yields a runtime-broken state even when direct file-value tests pass for the other two.
- App reinstall rotates bot and user OAuth tokens automatically. It does NOT replace an app-level token — the `xapp` token must be re-provisioned manually on every rotation.
- Provision the full Hermes Slack baseline BEFORE install/reinstall from the workspace-scoped app manifest: 13 bot OAuth scopes (`app_mentions:read`, `assistant:write`, `channels:history`, `channels:read`, `chat:write`, `commands`, `files:read`, `files:write`, `groups:history`, `groups:read`, `im:history`, `im:read`, `im:write`, `users:read`), Socket Mode enabled, interactivity enabled, six event subscriptions (`app_mention`, `message.channels`, `message.groups`, `message.im`, `assistant_thread_started`, `assistant_thread_context_changed`), and an app-level `connections:write` token.
- Verification must run from a clean shell that sources `~/.bashrc` — the canonical Hermes production env. Require `auth.test` to return `ok:true` for bot and user tokens, and `apps.connections.open` to return `ok:true` for the `xapp` token. Inspect `x-oauth-scopes` response headers to prove granted scopes line up with the manifest.
- Classify restart/registration errors separately from token validity — a failed launchd registration is NOT evidence about token health. Run Hermes doctor, health, and LaunchAgent checks AFTER token verification.
- The fix is documented in `~/.claude/skills/hermes-slack-rotation/SKILL.md` (created 2026-07-12), with the permission baseline, secure dotfile update map, and exact verification path.

## Key Quotes
> "Reinstalling rotates OAuth credentials but not the Socket Mode app token; provision permissions first and test from the sourced runtime shell."

> "Rotate all three token classes: bot (`xoxb`), user/MCP (`xoxp`, where enabled), and Socket Mode (`xapp`). App reinstall rotates bot/user OAuth tokens but does not replace an app-level token automatically."

> "Use a clean shell that sources `~/.bashrc`; require `auth.test` to return `ok:true` for bot and user tokens, and `apps.connections.open` to return `ok:true` for the `xapp` token."

## Connections
- [[HermesSlackCredentialRotation]] — the durable operational rule extracted from this source
- [[SlackBashrcLaunchdEnvContract]] — the sourcing discipline (`~/.bashrc` + `launchd-env-wrapper.sh`) the verification path depends on
- [[ManualCmuxRestoreApprovalGate]] — sibling operational authorization rule on jeffrey-owned operator actions
- [[CommitmentIntegrity]] — don't claim rotation complete based on direct file-value tests alone; verify behavior from the sourced runtime shell
- [Hermes Slack credential rotation skill](https://github.com/jleechanorg/.github/blob/main/.claude/skills/hermes-slack-rotation/SKILL.md) — the fix landing site (cross-reference only)
