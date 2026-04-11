---
title: "PR #390: feat(commands): integrate Claude auto-memory read/write into /history /research /debug /learn /checkpoint"
type: source
tags: []
date: 2026-03-24
source_file: raw/prs-worldai_claw/pr-390.md
sources: []
last_updated: 2026-03-24
---

## Summary
Claude Code has a file-based auto-memory system at `~/.claude/projects/PROJECT/memory/*.md` that persists learnings across conversations. Our slash commands were not reading from or writing to it — making the memory system silently underutilized. This PR wires 5 commands into that system.

## Metadata
- **PR**: #390
- **Merged**: 2026-03-24
- **Author**: jleechan2015
- **Stats**: +112/-46 in 7 files
- **Labels**: none

## Connections
