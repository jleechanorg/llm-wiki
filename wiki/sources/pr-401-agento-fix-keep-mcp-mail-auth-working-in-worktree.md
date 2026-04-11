---
title: "PR #401: [agento] fix: keep MCP mail auth working in worktree settings.json"
type: source
tags: []
date: 2026-04-11
source_file: raw/prs-worldai_claw/pr-401.md
sources: []
last_updated: 2026-04-11
---

## Summary
A previous follow-up tried to avoid serializing `MCP_AGENT_MAIL_TOKEN` by writing `Bearer ${MCP_AGENT_MAIL_TOKEN}` into worktree `settings.json`.

Claude Code reads MCP server headers from `settings.json` literally, so that placeholder broke MCP mail authentication instead of keeping the secret in env only. This follow-up restores working auth, fixes the shared JSON session activity regression surfaced during review, and updates the dependency graph so the current strict audit job clears again.

## Metadata
- **PR**: #401
- **Merged**: 2026-04-11
- **Author**: jleechan2015
- **Stats**: +286/-109 in 7 files
- **Labels**: none

## Connections
