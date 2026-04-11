---
title: "PR #5346: Add Genesis simulation/prediction mode and /simulate command"
type: source
tags: []
date: 2026-02-12
source_file: raw/prs-worldarchitect-ai/pr-5346.md
sources: []
last_updated: 2026-02-12
---

## Summary
- Add standalone prediction mode to Genesis (--simulation/--sim) that runs the jleechan simulation prompt to predict the next user message
- New /simulate and /sim slash commands for quick in-session predictions
- Benchmarked against real conversation data (PR #2541 streaming session)
- Applied P0-P6 fixes based on 4-agent research (brainstorm, history scan, academic research, multi-model second opinion)
- **P6 (NEW): Workflow state injection** — simulation now gathers git/PR/CI state to prevent

## Metadata
- **PR**: #5346
- **Merged**: 2026-02-12
- **Author**: jleechan2015
- **Stats**: +2124/-77 in 14 files
- **Labels**: none

## Connections
