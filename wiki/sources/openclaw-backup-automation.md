---
title: "OpenClaw ~/.openclaw Backup Automation"
type: source
tags: ["openclaw", "backup", "launchd", "automation", "security"]
date: 2026-04-07
source_file: "raw/openclaw-backup-automation.md"
sources: []
last_updated: 2026-04-07
---

## Summary
This document describes a recurring backup workflow for `~/.openclaw` using launchd (Apple's 24/7 scheduler) instead of system crontab. The backup script creates redacted snapshots of the OpenClaw workspace with secret masking and credential scrubbing.

## Key Claims
- **launchd required**: Guardrail forbids system crontab edits; launchd scheduling is mandatory for repo-managed recurring jobs
- **Redacted backups**: Backup script mirrors ~/.openclaw contents with in-band redaction, masking secret patterns in text files
- **Binary exclusion**: Skips obvious binary, log, database, ipynb, and jsonl artifacts
- **Manifest tracking**: Each snapshot includes a REDACTION_MANIFEST.txt documenting what was redacted

## Key Quotes
> "Forbidden: system crontab edits for OpenClaw jobs." — Guardrail requirement

> "Required: launchd scheduling for repo-managed recurring jobs." — Implementation mandate

## Connections
- [[OpenClaw]] — the project being backed up
- [[Launchd]] — Apple scheduler replacing crontab
- [[BackupAutomation]] — concept of automated backup with redaction

## Contradictions
- []
