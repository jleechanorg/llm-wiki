# PR #2: feat(backup): add git-backed home config backup and scheduler install

**Repo:** jleechanorg/user_scope
**Merged:** 2026-03-07
**Author:** jleechan2015
**Stats:** +16809/-9 in 104 files

## Summary
This PR turns `user_scope` into a git-backed machine config backup repo for Claude/Codex home configuration.

Compared with `origin/main`, it:
- commits the restore-useful backup snapshot under `backup/Mac/`
- adds automated home backup scripting via `scripts/backup-home.sh`
- adds cross-platform scheduler installation via root `install.sh`
- retargets the legacy conversation-backup installer to the new home-backup script
- adds privacy/hygiene guards so large or sensitive runtime artifacts stay

## Raw Body
## Summary

This PR turns `user_scope` into a git-backed machine config backup repo for Claude/Codex home configuration.

Compared with `origin/main`, it:
- commits the restore-useful backup snapshot under `backup/Mac/`
- adds automated home backup scripting via `scripts/backup-home.sh`
- adds cross-platform scheduler installation via root `install.sh`
- retargets the legacy conversation-backup installer to the new home-backup script
- adds privacy/hygiene guards so large or sensitive runtime artifacts stay out of git
- adds regression coverage around backup scope, hook correctness, and installer output

## Main Changes

### 1. Commit tracked backup content for restore
Adds the backed-up config tree under `backup/Mac/`, including:
- `backup/Mac/claude/agents/` — Claude agent definitions
- `backup/Mac/claude/hooks/` — hook scripts, utilities, docs, and tests
- `backup/Mac/codex/AGENTS.md`
- `backup/RESTORE_NOTES.md`

The intent is to keep small, restore-useful machine config in git so a new machine can reconstruct the local Claude/Codex setup from this repo.

### 2. Add automated config backup script
Adds:
- `scripts/backup-home.sh`

Behavior:
- syncs git-safe config content from `~/.claude/agents/`, `~/.claude/hooks/`, and `~/.codex/AGENTS.md` into `backup/<hostname>/`
- sends private or high-churn conversation data (history, sessions, sqlite, Claude projects, OpenClaw sessions) to Dropbox only
- writes backup metadata files
- commits only `backup/` changes when a git backup succeeds
- pushes the snapshot only from `main`, avoiding scheduled commits from feature branches

### 3. Add scheduler installation
Adds:
- `install.sh`

Behavior:
- macOS: writes a `launchd` user agent for `scripts/backup-home.sh`
- Linux: writes a `systemd --user` service + timer for `scripts/backup-home.sh`
- supports `--dry-run` and `--platform darwin|linux` for safe verification

Also updates:
- `scripts/install_conversation_backup_launchd.sh` to install `backup-home.sh` instead of the leg
