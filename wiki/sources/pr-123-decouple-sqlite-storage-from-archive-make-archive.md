---
title: "PR #123: Decouple SQLite storage from archive - make archive optional for core operations"
type: source
tags: []
date: 2025-12-18
source_file: raw/prs-/pr-123.md
sources: []
last_updated: 2025-12-18
---

## Summary
- SQLite storage (messages, agents, projects) now ALWAYS works regardless of archive settings
- Archive storage (`.mcp_mail/` git repo with .md files) is now optional and disabled by default
- Core MCP operations (`register_agent`, `ensure_project`) no longer require archive to be enabled

## Metadata
- **PR**: #123
- **Merged**: 2025-12-18
- **Author**: jleechan2015
- **Stats**: +102/-27 in 3 files
- **Labels**: none

## Connections
