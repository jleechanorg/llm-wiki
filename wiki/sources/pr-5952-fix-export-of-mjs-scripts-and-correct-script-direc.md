---
title: "PR #5952: Fix export of .mjs scripts and correct script directory paths"
type: source
tags: []
date: 2026-03-14
source_file: raw/prs-worldarchitect-ai/pr-5952.md
sources: []
last_updated: 2026-03-14
---

## Summary
Fixes a critical bug where `.mjs` scripts (auth-cli.mjs, auth-aiuniverse.mjs) were being silently omitted from exports, and corrects the directory paths for secondo command scripts that were incorrectly referenced from the wrong location.

## Metadata
- **PR**: #5952
- **Merged**: 2026-03-14
- **Author**: jleechan2015
- **Stats**: +98/-3 in 2 files
- **Labels**: none

## Connections
