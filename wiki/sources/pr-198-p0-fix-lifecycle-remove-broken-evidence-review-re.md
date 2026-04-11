---
title: "PR #198: [P0] fix(lifecycle): remove broken evidence-review requiredCheck from auto-merge"
type: source
tags: []
date: 2026-03-26
source_file: raw/prs-worldai_claw/pr-198.md
sources: []
last_updated: 2026-03-26
---

## Summary
Fixes orch-xrpl — P0 bug where auto-merge permanently blocks on "Evidence review pass" because it looks for a GitHub review from `evidence-reviewer[bot]`, but the evidence-reviewer subagent posts its verdict as a **PR comment**, not a GitHub review.

## Metadata
- **PR**: #198
- **Merged**: 2026-03-26
- **Author**: jleechan2015
- **Stats**: +5/-1 in 1 files
- **Labels**: none

## Connections
