---
title: "Slack bashrc + launchd env contract"
type: concept
tags: [slack, hermes, bashrc, launchd, env-wrapper, operational-rule, verification]
last_updated: 2026-07-12
---

# Slack bashrc + launchd env contract

Hermes Slack verification only works when run from a shell that has sourced `~/.bashrc` — and Hermes's own launchd-managed subprocesses only honor Slack env vars when they have been re-extracted from that file via `~/.hermes/scripts/launchd-env-wrapper.sh`. Treating either of these as decorative produces silent failures where the right tokens are on disk and the right launchd plist is loaded, but Slack API calls still return `invalid_auth` or Socket Mode sockets fail to open.

## The two halves

**1. The interactive shell.** `~/.bashrc` is the canonical source of Hermes's Slack env at a real terminal. `SLACK_BOT_TOKEN`, `SLACK_USER_TOKEN`, `SLACK_APP_TOKEN`, and any related vars (`*_SLACK_*`, `HERMES_SLACK_*`) live there. Any verification step — `auth.test`, `apps.connections.open`, scope header grep — must run from a shell that has loaded this file. A clean subshell without `source ~/.bashrc` (or `. ~/.bashrc`) can read different values, or no values at all.

**2. The launchd wrapper.** `~/.hermes/scripts/launchd-env-wrapper.sh` re-extracts a defined list of Slack-relevant vars from `~/.bashrc` and exports them into the launchd environment for the managed subprocess. The list of vars it extracts is the authoritative answer to "which env does Hermes see at runtime" — anything NOT in the list is invisible to the daemon even if it exists in `~/.bashrc`. If a new Slack-related var is added to a launchd plist but is NOT in the wrapper's extraction list, the plist will launch with the var unset.

## Why this matters during credential rotation

A common anti-pattern during Slack credential rotation is to update `~/.bashrc`, run `auth.test` from the interactive shell, see `ok:true`, and declare the rotation done. The launchd-managed Hermes subprocess is launched in a separate env and is NOT influenced by the interactive shell's state. If the wrapper's extraction list is missing a var, or the wrapper itself has been edited with `unset` / overwritten by `.profile` ordering, the daemon runs with stale or missing tokens regardless of what `~/.bashrc` says right now.

The rotation rule therefore requires TWO verification steps, run from a clean sourced shell:

1. `auth.test` and `apps.connections.open` against `~/.bashrc`-sourced vars → prove the credentials are valid.
2. Inspect the launchd subprocess's resolved env (`launchctl print gui/<uid>/<label> | grep -i slack`) → prove the wrapper actually delivered those vars into the daemon.

If step 1 passes but step 2 fails, the rotation is incomplete — the verifier and the runtime are looking at different envs.

## Operational rules

- Before any Slack credential rotation, run `bash -lc 'echo "$SLACK_BOT_TOKEN"'` and confirm a non-empty value comes back. A bare `echo $SLACK_BOT_TOKEN` from a non-login shell often returns empty.
- Add NEW Slack env vars to BOTH `~/.bashrc` AND the wrapper's extraction list in the SAME commit. A var that's in the plist but not the wrapper is invisible; a var that's in the wrapper but not `~/.bashrc` is empty.
- After wrapper edits, re-run `launchctl kickstart -k gui/$(id -u)/<label>` to re-launch the daemon and pick up the new extraction list. A live daemon doesn't re-read the wrapper mid-flight.
- Don't trust `hermes gateway status` (CLI) for slack-readiness — verify with `curl :8642/health` and the gateway's resolved env. CLI status lies at the boundary between wrapper state and what the gateway actually saw.

## Covered env vars (canonical, as of 2026-07-12)

- `SLACK_BOT_TOKEN` — `xoxb-...`
- `SLACK_USER_TOKEN` — `xoxp-...` (where MCP user token is enabled)
- `SLACK_APP_TOKEN` — `xapp-...` (Socket Mode; required for Socket Mode transport)
- Any additional `*_SLACK_*` or `HERMES_SLACK_*` vars set in `~/.bashrc`

## Sources
- [Hermes Slack credential rotation requires three token classes and full scope baseline](../sources/feedback-2026-07-12-hermes-slack-rotation-complete-permissions.md) — establishes this contract as a precondition for verification

## See also
- [[HermesSlackCredentialRotation]] — the rotation operation this contract supports
- [[CommitmentIntegrity]] — verify behavior from the right env, not the easiest env
