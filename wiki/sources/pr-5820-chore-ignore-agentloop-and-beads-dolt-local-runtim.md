---
title: "PR #5820: chore: ignore .agentloop/ and .beads/.dolt/ local runtime directories"
type: source
tags: []
date: 2026-03-03
source_file: raw/prs-worldarchitect-ai/pr-5820.md
sources: []
last_updated: 2026-03-03
---

## Summary
- Add `.agentloop/` to root `.gitignore` — agent loop runtime state (config.yaml, history.json) is machine-local and should not be tracked
- Add `.dolt/` to `.beads/.gitignore` — existing `dolt/` pattern did not match the dotfile variant `.dolt/` that Dolt actually creates

## Metadata
- **PR**: #5820
- **Merged**: 2026-03-03
- **Author**: jleechan2015
- **Stats**: +4/-0 in 2 files
- **Labels**: none

## Connections
