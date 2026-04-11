---
title: "PR #4831: fix(secondo): hardcode AI Universe Firebase API key for cross-machine usage"
type: source
tags: []
date: 2026-02-04
source_file: raw/prs-worldarchitect-ai/pr-4831.md
sources: []
last_updated: 2026-02-04
---

## Summary
- Fixed /secondo command failing on other machines with `auth/api-key-not-valid` error
- Hardcoded AI Universe Firebase API key with default syntax (`:-`) instead of strict (`?:`)
- Removed Firebase credential scrubbing from exportcommands.py that was preventing exported commands from working

**Key themes:**
- Cross-machine portability for /secondo command
- Correct implementation of PR #4291 (credential scrubbing removal)

## Metadata
- **PR**: #4831
- **Merged**: 2026-02-04
- **Author**: jleechan2015
- **Stats**: +15/-21 in 5 files
- **Labels**: none

## Connections
