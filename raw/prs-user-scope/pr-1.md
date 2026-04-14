# PR #1: Add disk alerts, conversation backups, and machine-setup tooling

**Repo:** jleechanorg/user_scope
**Merged:** 2026-03-07
**Author:** jleechan2015
**Stats:** +2579/-2 in 32 files

## Summary
This PR expands `user_scope` from a small policy/backup repo into a more complete user-level operations and machine-restore toolkit.

It adds two operational automations:
- a disk-usage alert workflow with email + Slack notification paths, silence controls, smoke tests, and a macOS LaunchAgent installer
- a repo-local/additive conversation-backup workflow for Codex, Claude, and OpenClaw artifacts, plus a LaunchAgent installer and regression coverage

It also adds a substantial set of restore/set

## Raw Body
## Summary
This PR expands `user_scope` from a small policy/backup repo into a more complete user-level operations and machine-restore toolkit.

It adds two operational automations:
- a disk-usage alert workflow with email + Slack notification paths, silence controls, smoke tests, and a macOS LaunchAgent installer
- a repo-local/additive conversation-backup workflow for Codex, Claude, and OpenClaw artifacts, plus a LaunchAgent installer and regression coverage

It also adds a substantial set of restore/setup assets:
- new-machine setup documentation for macOS and Ubuntu
- OOM guard documentation and a launchd plist
- `dotfiles/` templates and helper scripts for shell, Git, Codex, Claude MCP config, search safety, tmux/cmux visibility, repo bootstrap, and memory watchdog setup
- a secret-scrubbing helper for generating safe config templates from real local config files

## Main Changes
### 1. Disk usage alert automation
Adds:
- `scripts/disk_usage_alert.sh`
- `scripts/install_disk_usage_alert_launchd.sh`
- expanded regression coverage inside `scripts/test_disk_usage_alert.sh`

Behavior:
- checks disk usage for a configurable path
- defaults threshold to `800G`
- supports `--status`, `--silence`, `--unsilence`, and `--dry-run`
- attempts email delivery first, then Slack MCP delivery
- treats Slack MCP `result.isError=true` responses as delivery failures
- exits non-zero when all delivery methods fail

Launchd installer behavior:
- installs scripts under `~/Library/Application Support/user-scope/bin`
- writes a per-job env file under `~/Library/Application Support/user-scope/config`
- installs an hourly LaunchAgent under `~/Library/LaunchAgents`

### 2. Conversation backup workflow
Adds:
- `scripts/backup_conversations.sh`
- `scripts/install_conversation_backup_launchd.sh`
- config example updates in `config/crontab.example`
- spec/update docs in `roadmap/repo-local-conversation-backup-spec.md`

Behavior:
- backs up Codex, Claude, and OpenClaw conversation artifacts in
