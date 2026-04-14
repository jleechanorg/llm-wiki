---
title: "Dropbox"
type: entity
tags: [storage, cloud, backup, p2p, sync]
sources: [system-design-primer]
last_updated: 2026-04-14
---

Dropbox is a cloud storage service used as the backup destination for the Claude and Codex conversation backups. The backup script stores data in `~/Library/CloudStorage/Dropbox/` with separate folders for each AI tool.

## Backup Usage
- **Base Directory**: `~/Library/CloudStorage/Dropbox/`
- **Claude Folder**: `claude_conversations/` (~8,252 files)
- **Codex Folder**: `codex_conversations/` (~6,726 files)

## System Design Case Study
File synchronization service using distributed hash tables (DHT) for peer-to-peer file sync. File chunks stored globally with CRDT-based conflict resolution.

### Key Characteristics
- DHT for peer discovery and file chunk routing
- SQLite for local metadata
- CRDTs for conflict-free concurrent edits

## Connections
- [[DistributedHashTable]] — core DHT technology
