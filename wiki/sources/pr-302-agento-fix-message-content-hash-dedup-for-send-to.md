---
title: "PR #302: [agento] fix: message-content hash dedup for send-to-agent reaction (bd-n039)"
type: source
tags: []
date: 2026-03-30
source_file: raw/prs-worldai_claw/pr-302.md
sources: []
last_updated: 2026-03-30
---

## Summary
The `send-to-agent` reaction fires every poll cycle for unchanged PR state, sending identical CR feedback to workers 5-9x and burning context window tokens. The reaction system lacked message-content deduplication to skip sends when the rendered message (with `{{context}}` resolved) is unchanged.

## Metadata
- **PR**: #302
- **Merged**: 2026-03-30
- **Author**: jleechan2015
- **Stats**: +1327/-1408 in 32 files
- **Labels**: none

## Connections
