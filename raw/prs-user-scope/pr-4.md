# PR #4: backup: show per-file dry-run changes

**Repo:** jleechanorg/user_scope
**Merged:** 2026-03-09
**Author:** jleechan2015
**Stats:** +404/-432 in 15 files

## Summary
(none)

## Raw Body
Show per-file file-level changes during backup-home dry-run using rsync --dry-run output.

<!-- CURSOR_SUMMARY -->
---

> [!NOTE]
> **Medium Risk**
> Modifies backup logic and what gets captured/synced (including filtered OpenClaw data) and changes automation entrypoints, so misconfiguration could leak data to git or break backups despite added exclusion tests.
> 
> **Overview**
> Updates the scheduled backup workflow to use `scripts/backup-home.sh` (removing `backup_conversations.sh`) and renames related cron/launchd docs, env files, logs, and metadata to “home backup”.
> 
> Enhances `backup-home.sh` dry-run behavior to run `rsync --dry-run` with per-item `--itemize-changes` output and accurate counting, adds safeguards to prevent recursive self-copy when a destination is inside the source tree, and expands what’s backed up (adds Claude sessions plus broader OpenClaw backups split by target: **filtered** to git via explicit exclude patterns, **full** to Dropbox).
> 
> Hardens privacy hygiene by expanding `.gitignore` for OpenClaw secrets/runtime artifacts and adds/updates tests to assert dry-run creates no dirs, routing of private vs config data, OpenClaw secret exclusion from git, and removal of the legacy script.
> 
> <sup>Written by [Cursor Bugbot](https://cursor.com/dashboard?tab=bugbot) for commit 14ea222c5a9c00b4f758538f7dfcc5b405d4e318. This will update automatically on new commits. Configure [here](https://cursor.com/dashboard?tab=bugbot).</sup>
<!-- /CURSOR_SUMMARY -->

<!-- This is an auto-generated comment: release notes by coderabbit.ai -->
## Summary by CodeRabbit

* **New Features**
  * Adds a “home backup” workflow and configurable OpenClaw home-data backup with exclude patterns.

* **Chores**
  * Replaces legacy conversation-backup entrypoints with home-backup launch/cron configs and renamed metadata/log paths.
  * Expanded .gitignore to exclude OpenClaw/private artifacts.

* **Bug Fixes / Improvements**
  * Better dry-run and real-run rsync reporti
