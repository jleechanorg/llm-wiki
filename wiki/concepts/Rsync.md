---
title: "Rsync"
type: concept
tags: [backup, sync, tool]
sources: []
last_updated: 2026-04-07
---

Rsync is a fast and versatile file copying tool used for the backup synchronization. It efficiently transfers only differences between source and destination, making it ideal for large conversation histories.

## Usage in Backup Script
The enhanced `claude_backup.sh` uses rsync to synchronize Claude and Codex conversation directories to Dropbox with the following benefits:
- Incremental sync (only changed files)
- Efficient bandwidth usage
- Preserves file permissions and timestamps

## Related Sources
- [[Backup Script Enhancement: Added Codex Conversations Support]] — Uses rsync for backup
