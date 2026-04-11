---
title: "PR #1: Add disk alerts, conversation backups, and machine-setup tooling"
type: source
tags: []
date: 2026-03-07
source_file: raw/prs-/pr-1.md
sources: []
last_updated: 2026-03-07
---

## Summary
This PR expands `user_scope` from a small policy/backup repo into a more complete user-level operations and machine-restore toolkit.

It adds two operational automations:
- a disk-usage alert workflow with email + Slack notification paths, silence controls, smoke tests, and a macOS LaunchAgent installer
- a repo-local/additive conversation-backup workflow for Codex, Claude, and OpenClaw artifacts, plus a LaunchAgent installer and regression coverage

It also adds a substantial set of restore/set

## Metadata
- **PR**: #1
- **Merged**: 2026-03-07
- **Author**: jleechan2015
- **Stats**: +2579/-2 in 32 files
- **Labels**: none

## Connections
