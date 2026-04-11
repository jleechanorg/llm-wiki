---
title: "PR #532: [P2] feat: jleechanclaw custom eloop skill path (orch-eei)"
type: source
tags: []
date: 2026-04-07
source_file: raw/prs-worldai_claw/pr-532.md
sources: []
last_updated: 2026-04-07
---

## Summary
AO `orchestratorRules` and operators expect the dropped-thread eloop at `~/.openclaw/skills/jleechanclaw-eloop.md`, but bootstrap never created that path. This PR wires the canonical repo file (`skills/jleechanclaw-eloop.md`) via symlink and adds a Claude Code skill entry for discovery.

## Metadata
- **PR**: #532
- **Merged**: 2026-04-07
- **Author**: jleechan2015
- **Stats**: +72/-3 in 7 files
- **Labels**: none

## Connections
