---
title: "PR #50: Fix global inbox mention search and tighten tests"
type: source
tags: []
date: 2025-11-16
source_file: raw/prs-/pr-50.md
sources: []
last_updated: 2025-11-16
---

## Summary
- ensure `_find_mentions_in_global_inbox` uses a proper SQLAlchemy join against the `fts_messages` virtual table so mention detection works again (fixes failing global inbox tests and addresses the missing c1 bug fix)
- add a SQLAlchemy `table()` representation and `cast()` to keep queries type-safe, and make `search_mailbox` consistently return `ToolResult`
- harden integration tests (`tests/integration/test_mcp_mail_crud.py`, `tests/test_share_export.py`) with not-None checks and `isinstance`

## Metadata
- **PR**: #50
- **Merged**: 2025-11-16
- **Author**: jleechan2015
- **Stats**: +21/-13 in 3 files
- **Labels**: none

## Connections
