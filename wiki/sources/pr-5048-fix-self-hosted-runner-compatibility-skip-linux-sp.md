---
title: "PR #5048: Fix: Self-hosted runner compatibility (skip Linux-specific setup on macOS)"
type: source
tags: []
date: 2026-02-08
source_file: raw/prs-worldarchitect-ai/pr-5048.md
sources: []
last_updated: 2026-02-08
---

## Summary
Fix self-hosted macOS runner compatibility by conditionally skipping Linux-specific setup steps (Python installation and apt-get commands).

**Key themes:**
- OS-aware workflow steps for cross-platform runner support
- Self-hosted runner cost optimization (macOS runners are free, use existing pyenv Python)
- Proper fallback logic when self-hosted unavailable

## Metadata
- **PR**: #5048
- **Merged**: 2026-02-08
- **Author**: jleechan2015
- **Stats**: +13/-8 in 3 files
- **Labels**: none

## Connections
