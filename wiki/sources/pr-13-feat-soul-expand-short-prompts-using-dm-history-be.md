---
title: "PR #13: feat(soul): expand short prompts using DM history before MC dispatch (ORCH-7wk)"
type: source
tags: []
date: 2026-03-02
source_file: raw/prs-worldai_claw/pr-13.md
sources: []
last_updated: 2026-03-02
---

## Summary
- Adds context expansion instruction to SOUL.md
- When jleechanclaw sees a message referencing prior conversation ("we discussed", "from earlier", etc.), it now reads the last 20 DM messages and extracts the full spec before creating a Mission Control task
- The coding agent receives an expanded description — never a raw stub like "build the discord bot we discussed"

## Metadata
- **PR**: #13
- **Merged**: 2026-03-02
- **Author**: jleechan2015
- **Stats**: +92/-11 in 3 files
- **Labels**: none

## Connections
