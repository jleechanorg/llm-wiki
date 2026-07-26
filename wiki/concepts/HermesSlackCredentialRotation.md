---
title: "Hermes Slack credential rotation"
type: concept
tags: [slack, hermes, credentials, rotation, oauth, socket-mode, launchd, bashrc, operational-rule]
last_updated: 2026-07-12
---

# Hermes Slack credential rotation

Hermes Slack credential rotation is a three-token-class operation, not a two-token-class one. A full rotation re-provisions bot OAuth (`xoxb`), user/MCP OAuth (`xoxp`, where enabled), AND the Socket Mode app-level `xapp` token, then verifies from a clean shell that sources `~/.bashrc` — the same shell discipline `~/.hermes/scripts/launchd-env-wrapper.sh` uses.

## Why three classes, not two

The Slack web API uses bot/user OAuth tokens; the Socket Mode transport uses an `xapp` app-level token. App reinstall is an OAuth action — it rotates `xoxb` and `xoxp` automatically, but it does NOT replace `xapp`. So a "successful" reinstall that leaves `xapp` stale produces a Hermes runtime state where direct file-value tests for `xoxb` and `xoxp` pass, but Socket Mode sockets still fail to open. The user-visible symptom is Hermes "down" with no apparent credential cause.

## Permission baseline to provision BEFORE rotating

Re-create or verify the workspace-scoped Slack app manifest against the Hermes baseline:

- **Bot OAuth scopes (13):** `app_mentions:read`, `assistant:write`, `channels:history`, `channels:read`, `chat:write`, `commands`, `files:read`, `files:write`, `groups:history`, `groups:read`, `im:history`, `im:read`, `im:write`, `users:read`
- **App settings:** Socket Mode enabled, Interactivity enabled
- **Event subscriptions (6):** `app_mention`, `message.channels`, `message.groups`, `message.im`, `assistant_thread_started`, `assistant_thread_context_changed`
- **App-level token:** `connections:write` scope

Reinstall only AFTER this baseline is correct in the manifest. Rotating against an under-scoped manifest will produce a Hermes runtime that still fails even though every token is fresh.

## Verification path

Run from a clean shell that sources `~/.bashrc` — that is the canonical Hermes production environment:

```bash
# bot token
curl -fsS -X POST "https://slack.com/api/auth.test" \
  -H "Authorization: Bearer $SLACK_BOT_TOKEN" | jq '.ok'

# user token (xoxp), where enabled
curl -fsS -X POST "https://slack.com/api/auth.test" \
  -H "Authorization: Bearer $SLACK_USER_TOKEN" | jq '.ok'

# app-level token (xapp) — proves Socket Mode can open a connection
curl -fsS -X POST "https://slack.com/api/apps.connections.open" \
  -H "Authorization: Bearer $SLACK_APP_TOKEN" | jq '.ok'

# granted-scope proof — header must list the 13 bot scopes
curl -fsSI -X POST "https://slack.com/api/auth.test" \
  -H "Authorization: Bearer $SLACK_BOT_TOKEN" | grep -i '^x-oauth-scopes'
```

Required: all three `auth.test` calls AND `apps.connections.open` return `ok:true`; `x-oauth-scopes` lists the 13 bot scopes. After tokens verify, run the Hermes runtime checks (`hermes doctor`, gateway health probe, LaunchAgent status). A failed launchd registration is NOT evidence about token health — classify it separately.

## What this rule forbids

- Treating any of the three token classes as optional. Skipping `xapp` "because Socket Mode isn't used" fails silently whenever a launchd-managed subprocess needs it.
- Verifying tokens by reading `echo $SLACK_BOT_TOKEN` alone — file-value presence does NOT prove the token works against the Slack API.
- Running `auth.test` from a shell that hasn't sourced `~/.bashrc`. The wrapper contract (`launchd-env-wrapper.sh`) re-extracts from that file; tokens that look fine in an inline shell but were never sourced can be stale.
- Claiming rotation complete before `apps.connections.open` returns `ok:true`.
- Confusing restart/registration errors with token validity — fix each class separately, in its own commit/PR.

## Sources
- [Hermes Slack credential rotation requires three token classes and full scope baseline](../sources/feedback-2026-07-12-hermes-slack-rotation-complete-permissions.md) — primary source
- `~/.claude/skills/hermes-slack-rotation/SKILL.md` — fix landing site (machine-local, not in this wiki)

## See also
- [[SlackBashrcLaunchdEnvContract]] — the sourcing wrapper the verification path depends on
- [[ManualCmuxRestoreApprovalGate]] — sibling operational authorization rule
- [[CommitmentIntegrity]] — verify behavior, don't trust file-value tests
