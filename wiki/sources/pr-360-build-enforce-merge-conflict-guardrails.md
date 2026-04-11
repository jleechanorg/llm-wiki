---
title: "PR #360: build: enforce merge-conflict guardrails"
type: source
tags: [codex]
date: 2025-10-15
source_file: raw/prs-/pr-360.md
sources: []
last_updated: 2025-10-15
---

## Summary
- document the merge-conflict guardrails in AGENTS.md for quick reference
- add repository-managed pre-commit and pre-push hooks that block commits or pushes while MERGE_HEAD is present
- require explicit modes in the conflict resolution helpers, enforce merge commit prefixes, and make run_tests.sh abort on dirty or conflicted trees

## Metadata
- **PR**: #360
- **Merged**: 2025-10-15
- **Author**: jleechan2015
- **Stats**: +281/-23 in 7 files
- **Labels**: codex

## Connections
