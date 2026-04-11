---
title: "PR #15: docs: add upstream PR strip list to CLAUDE.md and AGENTS.md"
type: source
tags: []
date: 2026-03-16
source_file: raw/prs-worldai_claw/pr-15.md
sources: []
last_updated: 2026-03-16
---

## Summary
Documents what to exclude when cherry-picking fork work to a `ComposioHQ/agent-orchestrator` upstream PR:

- `docs/design/*.md` — fork-only markdown design docs
- `CLAUDE.md` / `AGENTS.md` — fork-specific tooling instructions
- `roadmap/` — internal roadmap docs
- `.beads/` — local issue tracker
- Commits referencing fork-only infrastructure

Motivated by PR #486 where `agent-gemini-plugin.md` was initially included and had to be manually removed.

🤖 Generated with [Claude Code](https://claude.c

## Metadata
- **PR**: #15
- **Merged**: 2026-03-16
- **Author**: jleechan2015
- **Stats**: +21/-0 in 2 files
- **Labels**: none

## Connections
