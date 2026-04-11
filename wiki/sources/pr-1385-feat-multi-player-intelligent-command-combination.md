---
title: "PR #1385: feat: Multi-Player Intelligent Command Combination Hook"
type: source
tags: []
date: 2025-08-18
source_file: raw/prs-worldarchitect-ai/pr-1385.md
sources: []
last_updated: 2025-08-18
---

## Summary
Enhanced the compose commands hook to become "multi-player" - intelligently parsing command markdown files for nested slash commands and suggesting optimal combinations.

### 🎯 Multi-Player Intelligence System

The hook now goes beyond simple command detection to parse `.claude/commands/*.md` files and find nested command references:

- **Nested Command Detection**: Automatically discovers commands referenced in other commands
- **Pattern Recognition**: Finds phrases like "combines the functiona

## Metadata
- **PR**: #1385
- **Merged**: 2025-08-18
- **Author**: jleechan2015
- **Stats**: +455/-20 in 3 files
- **Labels**: none

## Connections
