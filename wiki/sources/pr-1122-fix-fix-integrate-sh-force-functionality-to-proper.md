---
title: "PR #1122: fix: Fix integrate.sh --force functionality to properly stash uncommitted changes"
type: source
tags: []
date: 2025-08-02
source_file: raw/prs-worldarchitect-ai/pr-1122.md
sources: []
last_updated: 2025-08-02
---

## Summary
Fixes the integrate.sh script's --force functionality to properly handle uncommitted changes. Previously, the script would detect uncommitted changes, claim to proceed anyway, but then fail when `git checkout` refused to switch branches.

## Metadata
- **PR**: #1122
- **Merged**: 2025-08-02
- **Author**: jleechan2015
- **Stats**: +8/-1 in 1 files
- **Labels**: none

## Connections
