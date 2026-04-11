---
title: "PR #115: docs: Add conversation auto-creation design documentation"
type: source
tags: []
date: 2025-10-01
source_file: raw/prs-/pr-115.md
sources: []
last_updated: 2025-10-01
---

## Summary
Add comprehensive documentation for ChatGPT-like conversation auto-creation feature across 3 documents:

### 1. Technical Design (`conversation-auto-creation-design.md`)
- **Architecture**: Backend + Conversation MCP Server
- **Key Innovation**: Atomic `getOrCreate()` RPC eliminating race conditions
- **Message Ordering**: Firestore transactions with dual timestamp + sequence number approach
- **Anonymous Users**: `anon_{uuid}` strategy with migration path
- **Error Handling**: Comprehensive sta

## Metadata
- **PR**: #115
- **Merged**: 2025-10-01
- **Author**: jleechan2015
- **Stats**: +4039/-0 in 3 files
- **Labels**: none

## Connections
