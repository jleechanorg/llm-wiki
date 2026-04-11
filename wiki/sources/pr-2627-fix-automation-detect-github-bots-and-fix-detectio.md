---
title: "PR #2627: fix(automation): Detect GitHub bots and fix detection order"
type: source
tags: []
date: 2025-12-26
source_file: raw/prs-worldarchitect-ai/pr-2627.md
sources: []
last_updated: 2025-12-26
---

## Summary
- Add `KNOWN_GITHUB_BOTS` set to detect bots without `[bot]` suffix (coderabbitai, github-actions, copilot-swe-agent)
- Fix detection order - check `KNOWN_GITHUB_BOTS` FIRST before codex pattern exclusion (P1 bug)
- Check for new bot comments before skipping already-processed PRs in `_is_pr_actionable()`

## Metadata
- **PR**: #2627
- **Merged**: 2025-12-26
- **Author**: jleechan2015
- **Stats**: +89/-20 in 3 files
- **Labels**: none

## Connections
