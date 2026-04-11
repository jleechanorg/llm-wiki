---
title: "PR #5542: Add Codex Web setup/maintenance scripts for git remote bootstrap"
type: source
tags: []
date: 2026-02-15
source_file: raw/prs-worldarchitect-ai/pr-5542.md
sources: []
last_updated: 2026-02-15
---

## Summary
- add `scripts/codex_web_setup.sh` to bootstrap git wiring in Codex Web containers
- add `scripts/codex_web_maintenance.sh` to re-apply the same wiring on cached container resume
- handle missing `origin` remote, branch/upstream detection, and print git diagnostics

## Metadata
- **PR**: #5542
- **Merged**: 2026-02-15
- **Author**: jleechan2015
- **Stats**: +132/-0 in 2 files
- **Labels**: none

## Connections
