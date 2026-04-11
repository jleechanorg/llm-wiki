---
title: "PR #5596: fix: Prevent doubled $PROJECT_ROOT in export path transformation"
type: source
tags: []
date: 2026-02-17
source_file: raw/prs-worldarchitect-ai/pr-5596.md
sources: []
last_updated: 2026-02-17
---

## Summary
- Fix critical bug in export filter where `mvp_site/` was being replaced with `$PROJECT_ROOT/` even when `$PROJECT_ROOT/` was already present
- This caused invalid paths like `$PROJECT_ROOT/$PROJECT_ROOT/mcp_api.py` in exported scripts

## Metadata
- **PR**: #5596
- **Merged**: 2026-02-17
- **Author**: jleechan2015
- **Stats**: +4/-1 in 1 files
- **Labels**: none

## Connections
