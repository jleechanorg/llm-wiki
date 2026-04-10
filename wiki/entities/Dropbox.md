---
title: "Dropbox"
type: entity
tags: [storage, cloud, backup]
sources: []
last_updated: 2026-04-07
---

Dropbox is a cloud storage service used as the backup destination for the Claude and Codex conversation backups. The backup script stores data in `~/Library/CloudStorage/Dropbox/` with separate folders for each AI tool.

## Backup Structure
- **Base Directory**: `~/Library/CloudStorage/Dropbox/`
- **Claude Folder**: `claude_conversations/` (~8,252 files)
- **Codex Folder**: `codex_conversations/` (~6,726 files)

## Usage in This Wiki
- [[Backup Script Enhancement: Added Codex Conversations Support]] — Backup destination
