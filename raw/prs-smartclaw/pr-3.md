# PR #3: [P2] feat: sync general-purpose content from jleechanclaw

**Repo:** jleechanorg/smartclaw
**Merged:** 2026-03-29
**Author:** jleechan2015
**Stats:** +1377/-0 in 18 files

## Summary
Syncs general-purpose, non-personal content from jleechanorg/jleechanclaw to this repo.

## Raw Body
## Summary
Syncs general-purpose, non-personal content from jleechanorg/jleechanclaw to this repo.

## What was synced
- **Docs**: HARNESS_ENGINEERING, ORCHESTRATION_DESIGN, ZERO_TOUCH, EVIDENCE_REVIEW_SCHEMA
- **Workflows**: skeptic-cron.yml, coderabbit-ping-on-push.yml
- **Launchd plist templates**: gateway, lifecycle-manager, health-check, monitor-agent, scheduler, webhook, agento-manager
- **Skills**: er (evidence review), dispatch-task, cmux, antigravity-computer-use, claude-code-computer-use

## Sanitization applied
| Pattern | Replacement |
|---------|-------------|
| `jleechanorg` | `$GITHUB_ORG` |
| `C0AKALZ4CKW`, `C09GRLXF9GR`, etc. | `$SLACK_CHANNEL_ID` |
| `~/.openclaw` | `~/.smartclaw` |
| `/Users/jleechan/` | `$HOME/` |
| `OPENCLAW_SLACK_BOT_TOKEN` | `SLACK_BOT_TOKEN` |

## Testing
Manual review only — no automated tests on this seed PR.

## ⚠️ DO NOT AUTO-MERGE
This PR requires HUMAN REVIEW before merge.

<!-- CURSOR_SUMMARY -->
---

> [!NOTE]
> **High Risk**
> Adds new GitHub Actions automation that can automatically comment on and merge open PRs based on bot-driven gates; misconfiguration or edge cases could lead to unintended merges or noisy PR activity.
> 
> **Overview**
> Introduces repo-level automation for PR review/merge. A new `coderabbit-ping-on-push` workflow comments `@coderabbitai all good?` on open PRs for the pushed branch, and a new scheduled `skeptic-cron` workflow evaluates all open non-draft PRs against a **7-green** gate (CI, mergeability, CodeRabbit approval, Bugbot severity comments, unresolved review comments, evidence-review-bot state, and a skeptic verdict) and auto-merges qualifying PRs.
> 
> Adds supporting operational/config artifacts and guidance: new docs defining *Harness Engineering* and *zero-touch* criteria, several macOS `launchd` plist templates for running managers/health checks/scheduler/monitor agents, and new/updated `skills/` content (e.g., `cmux` control docs + a small socket client script, `dispatch-task`, UI
