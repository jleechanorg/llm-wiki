---
title: "PR #89: fix: ensure Render build installs dev dependencies"
type: source
tags: [codex]
date: 2025-10-30
source_file: raw/prs-/pr-89.md
sources: []
last_updated: 2025-10-30
---

## Summary
- update the Render deployment build command to force-install dev dependencies so Vite and other tooling are present during production builds
- add a regression test that asserts render.yaml keeps the `--include=dev` flag in the build command

## Metadata
- **PR**: #89
- **Merged**: 2025-10-30
- **Author**: jleechan2015
- **Stats**: +30/-5 in 5 files
- **Labels**: codex

## Connections
