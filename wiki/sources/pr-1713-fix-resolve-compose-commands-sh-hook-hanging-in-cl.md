---
title: "PR #1713: fix: Resolve compose-commands.sh hook hanging in claude -p mode"
type: source
tags: []
date: 2025-09-22
source_file: raw/prs-worldarchitect-ai/pr-1713.md
sources: []
last_updated: 2025-09-22
---

## Summary
- Fixed UserPromptSubmit hook hanging that blocked `claude -p` execution
- Replaced blocking `cat` with timeout-based `dd` approach in compose-commands.sh
- Added comprehensive red-green TDD test suite with 8 test scenarios
- Preserved all existing functionality for normal interactive mode

## Metadata
- **PR**: #1713
- **Merged**: 2025-09-22
- **Author**: jleechan2015
- **Stats**: +252/-4 in 3 files
- **Labels**: none

## Connections
