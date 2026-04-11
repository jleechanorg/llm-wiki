---
title: "PR #439: [P2] fix(openclaw): remove bundled mem0 plugin, update ops skill"
type: source
tags: []
date: 2026-03-29
source_file: raw/prs-worldai_claw/pr-439.md
sources: []
last_updated: 2026-03-29
---

## Summary
- Removes the bundled `extensions/openclaw-mem0/` from the jleechanclaw repo — the globally installed npm package (`@mem0/openclaw-mem0`) is already configured in `openclaw.json` and takes precedence, making the bundled copy redundant and causing duplicate plugin warnings
- Patches `mem0ai` to pass `checkCompatibility=false` to the Qdrant client, eliminating the persistent version warning on every mem0 command
- Updates `mem0-memory-operations.md` skill with full install/runbook, verification st

## Metadata
- **PR**: #439
- **Merged**: 2026-03-29
- **Author**: jleechan2015
- **Stats**: +50/-2093 in 7 files
- **Labels**: none

## Connections
