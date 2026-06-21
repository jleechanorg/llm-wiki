---
name: feedback-cron-env-access-token
description: "Scripts invoked from cron must source ~/.bashrc — cron's env has no ACCESS_TOKEN, LABELS, or ORG_NAME"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 1b83ecc8-6dc7-4dc3-9c53-0197133eccce
---

Any script invoked from cron (or launchd with minimal env) that calls docker compose using variable substitution MUST source `~/.bashrc` (with set +u guard) near the top of the script.

**Why:** Discovered 2026-06-21 on jeff-ubuntu: `monitor.sh` zombie recreation called `docker compose` with `ACCESS_TOKEN="${ACCESS_TOKEN:-}"` which expanded to an empty string in cron's minimal environment, causing compose to hard-fail with "required variable ACCESS_TOKEN is missing". The fix (zombie container recreation) silently failed across many 15-minute cron ticks while the log showed "FAILED" with no escalation.

`start.sh` (the companion script) already had `source ~/.bashrc` — this pattern was not carried over to `monitor.sh` when the zombie_check function was added.

**How to apply:**
- Any new shell script dispatched by cron or launchd that uses env vars that come from the user's shell profile (`ACCESS_TOKEN`, `ORG_NAME`, `LABELS`, `HERMES_SLACK_BOT_TOKEN`, etc.) MUST have this near the top:
  ```bash
  if [[ -f "$HOME/.bashrc" ]]; then
    set +u
    source "$HOME/.bashrc" 2>/dev/null || true
    set -u
  fi
  ```
- When reviewing or writing such scripts, check that the sourcing block is present before any use of the env var.
- Test with `env -i HOME=$HOME bash <script>` to verify it works in a minimal cron environment.
- On jeff-ubuntu: this pattern applies to all scripts under `~/projects/worktree_runner/self-hosted-colima/scripts/`
