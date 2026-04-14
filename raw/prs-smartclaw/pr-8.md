# PR #8: [P2] feat: sync general-purpose content from jleechanclaw

**Repo:** jleechanorg/smartclaw
**Merged:** 2026-04-02
**Author:** jleechan2015
**Stats:** +50124/-1759 in 306 files

## Summary
Syncs general-purpose, non-personal content from jleechanorg/jleechanclaw to this repo.

## Raw Body
## Summary
Syncs general-purpose, non-personal content from jleechanorg/jleechanclaw to this repo.

## What was synced
- **Docs**: HARNESS_ENGINEERING, ZERO_TOUCH
- **Workflows**: skeptic-cron.yml, coderabbit-ping-on-push.yml
- **Launchd plist templates**: lifecycle-manager, health-check, monitor-agent, scheduler, agento-manager
- **Skills**: er (evidence review), dispatch-task, cmux, antigravity-computer-use, claude-code-computer-use

## Sanitization applied
| Pattern | Replacement |
|---------|-------------|
| `jleechanorg` | `$GITHUB_ORG` |
| `jleechanclaw` | `$GITHUB_REPO` |
| `jleechanorg/jleechanclaw` | `$GITHUB_ORG/$GITHUB_REPO` |
| `jleechan` | `$GITHUB_USER` |
| `C0AKALZ4CKW`, `C09GRLXF9GR`, etc. | `$SLACK_CHANNEL_ID` |
| `~/.openclaw` | `~/.smartclaw` |
| `/Users/jleechan/` or `/Users/jleechan` | `$HOME/` or `$HOME` |
| `OPENCLAW_SLACK_BOT_TOKEN` | `SLACK_BOT_TOKEN` |

## Testing
Manual review only — no automated tests on this seed PR.

## ⚠️ DO NOT AUTO-MERGE
This PR requires HUMAN REVIEW before merge.

<!-- CURSOR_SUMMARY -->
---

> [!NOTE]
> **High Risk**
> Updates automation that can block or merge PRs (GitHub Actions `skeptic-*` workflows) and adds enforcement in `.claude/metadata-updater.sh` that can deny `gh pr create/merge`, so misconfiguration could interrupt delivery or merging across the repo.
> 
> **Overview**
> Adds a large set of new `.claude/commands/*` and `.claude/skills/*` to support orchestration workflows (notably `/claw` for dispatching coding work to parallel `ao spawn` sessions, plus reporting/history/research/learn/checkpoint utilities and an `agento` PR status report that also posts to Slack).
> 
> Tightens agent guardrails in `.claude/metadata-updater.sh` by normalizing prefixed shell commands, enforcing `[agento]` PR titles at `PreToolUse`, and denying agent-driven `gh pr merge` unless explicitly overridden, while keeping PostToolUse metadata updates for PR/branch tracking.
> 
> Expands CI/merge automation by updating `skeptic-cr
