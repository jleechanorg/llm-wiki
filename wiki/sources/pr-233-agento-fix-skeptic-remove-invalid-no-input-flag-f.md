---
title: "PR #233: [agento] fix(skeptic): remove invalid --no-input flag from Claude CLI invocation"
type: source
tags: []
date: 2026-03-27
source_file: raw/prs-worldai_claw/pr-233.md
sources: []
last_updated: 2026-03-27
---

## Summary
`ao skeptic` shells out to `claude --print --no-input` to run LLM evaluation. The `--no-input` flag does not exist in Claude CLI v2.1.x, causing the command to fail silently (stderr suppressed by `2>/dev/null`). The catch block then returns a generic \"CLI not available\" message, making it appear Claude CLI isn't installed.

Discovered when running `ao skeptic --pr 5879 --repo jleechanorg/worldarchitect.ai` from within a Claude Code CLI session — the very tool it was looking for.

## Metadata
- **PR**: #233
- **Merged**: 2026-03-27
- **Author**: jleechan2015
- **Stats**: +174/-15 in 2 files
- **Labels**: none

## Connections
