---
title: "PR #329: feat: resolve slash commands before /claw dispatch"
type: source
tags: []
date: 2026-03-21
source_file: raw/prs-worldai_claw/pr-329.md
sources: []
last_updated: 2026-03-21
---

## Summary
`/claw run /simplify on this repo` dispatched successfully to the OpenClaw gateway, but the agent didn't execute `/simplify` — it asked "say go ahead" instead. Root cause: OpenClaw has no way to discover slash command definitions, and `/claw` was forwarding raw text without resolving commands.

## Metadata
- **PR**: #329
- **Merged**: 2026-03-21
- **Author**: jleechan2015
- **Stats**: +80/-1 in 1 files
- **Labels**: none

## Connections
