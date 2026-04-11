---
title: "PR #5227: Restore living world + narrative_lite for DialogAgent"
type: source
tags: []
date: 2026-02-10
source_file: raw/prs-worldarchitect-ai/pr-5227.md
sources: []
last_updated: 2026-02-10
---

## Summary
Restores living world functionality to DialogAgent (broken in PR #5150) while preserving significant token savings through a new narrative_lite prompt.

**Key changes:**
- Created narrative_lite_system_instruction.md for core mechanics (~2,500 tokens)
- Restored LIVING_WORLD prompt to DialogAgent
- Updated constants and PATH_MAP for new prompt type
- Net savings: ~12,200 tokens vs pre-PR-5150 baseline

## Metadata
- **PR**: #5227
- **Merged**: 2026-02-10
- **Author**: jleechan2015
- **Stats**: +349/-17 in 9 files
- **Labels**: none

## Connections
