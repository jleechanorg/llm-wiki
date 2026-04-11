---
title: "PR #5: feat(claim-pr): send initial task message to agent after claiming PR"
type: source
tags: []
date: 2026-03-16
source_file: raw/prs-worldai_claw/pr-5.md
sources: []
last_updated: 2026-03-16
---

## Summary
- Agents spawned with `--claim-pr` had no initial instructions — they woke up in the worktree not knowing they should fix a PR
- This caused agents to idle, exit early, or post `@coderabbitai all good?` without reading/fixing review comments
- Root cause: `claimPR()` checked out the branch and updated metadata but sent zero message to the agent

## Metadata
- **PR**: #5
- **Merged**: 2026-03-16
- **Author**: jleechan2015
- **Stats**: +304/-10 in 7 files
- **Labels**: none

## Connections
