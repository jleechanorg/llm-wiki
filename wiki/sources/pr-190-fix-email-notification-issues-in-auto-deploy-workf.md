---
title: "PR #190: Fix email notification issues in auto-deploy workflow"
type: source
tags: []
date: 2025-11-11
source_file: raw/prs-/pr-190.md
sources: []
last_updated: 2025-11-11
---

## Summary
Fixes issues identified in PR #185 review comments:
- Move permissions to job level (GitHub Actions requirement)
- Improve issue search to include commit SHA for better deduplication
- Safely escape commit message to prevent heredoc breakage
- Include commit SHA in issue title for better tracking

## Metadata
- **PR**: #190
- **Merged**: 2025-11-11
- **Author**: jleechan2015
- **Stats**: +220/-92 in 5 files
- **Labels**: none

## Connections
