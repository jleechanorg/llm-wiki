---
title: "PR #154: test(mem0): add cross-session and hard recall test evidence (2026-03-14)"
type: source
tags: []
date: 2026-03-15
source_file: raw/prs-worldai_claw/pr-154.md
sources: []
last_updated: 2026-03-15
---

## Summary
- Adds two `testing_llm/` artifacts for mem0 hooks recall testing
- Cross-session test: verifies past-session facts surface via `mem0_recall.py` UserPromptSubmit hook (PASS)
- Hard recall test: verifies within-session corrective actions recalled (FAIL — single-session facts not yet in qdrant store, expected gap)

## Metadata
- **PR**: #154
- **Merged**: 2026-03-15
- **Author**: jleechan2015
- **Stats**: +274/-0 in 4 files
- **Labels**: none

## Connections
