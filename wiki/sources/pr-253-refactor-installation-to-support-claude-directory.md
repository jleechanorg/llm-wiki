---
title: "PR #253: Refactor installation to support ~/.claude directory structure"
type: source
tags: []
date: 2026-02-20
source_file: raw/prs-/pr-253.md
sources: []
last_updated: 2026-02-20
---

## Summary
Refactored the installation script to properly support Claude Code's standard `~/.claude` directory structure with separate subdirectories for agents, commands, scripts, and skills. The installer now copies plugin files from the repository to the appropriate system-level directories instead of installing locally.

## Metadata
- **PR**: #253
- **Merged**: 2026-02-20
- **Author**: jleechan2015
- **Stats**: +172/-102 in 2 files
- **Labels**: none

## Connections
