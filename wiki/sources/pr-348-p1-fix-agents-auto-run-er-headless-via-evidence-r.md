---
title: "PR #348: [P1] fix: agents auto-run /er headless via evidence-reviewer subagent"
type: source
tags: []
date: 2026-03-21
source_file: raw/prs-worldai_claw/pr-348.md
sources: []
last_updated: 2026-03-21
---

## Summary
Agento agents were instructed to run /er to satisfy the evidence review condition in the merge gate. However, /er is a slash command that only works in interactive Claude Code sessions — ao-spawned headless agents cannot invoke it directly. This left the evidence review step as the last manual intervention blocking full autonomy.

## Metadata
- **PR**: #348
- **Merged**: 2026-03-21
- **Author**: jleechan2015
- **Stats**: +24/-19 in 2 files
- **Labels**: none

## Connections
