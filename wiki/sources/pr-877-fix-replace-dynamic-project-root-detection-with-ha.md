---
title: "PR #877: fix: Replace dynamic project root detection with hardcoded path"
type: source
tags: []
date: 2025-07-23
source_file: raw/prs-worldarchitect-ai/pr-877.md
sources: []
last_updated: 2025-07-23
---

## Summary
**EXPANDED SCOPE**: Comprehensive fix for git-header.sh "command not found" errors across all systems - moved from simple hardcoding to complete hooks system overhaul.

Fixes persistent "command not found" errors with git-header.sh by:
1. ✅ Replacing unreliable dynamic project root detection with hardcoded paths
2. ✅ Removing confusing export directory that duplicated functionality  
3. ✅ Simplifying hooks configuration to use clean file paths instead of complex inline bash

## Metadata
- **PR**: #877
- **Merged**: 2025-07-23
- **Author**: jleechan2015
- **Stats**: +17/-43 in 5 files
- **Labels**: none

## Connections
