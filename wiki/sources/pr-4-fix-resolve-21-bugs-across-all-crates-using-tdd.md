---
title: "PR #4: fix: resolve 21 bugs across all crates using TDD"
type: source
tags: []
date: 2026-03-15
source_file: raw/prs-/pr-4.md
sources: []
last_updated: 2026-03-15
---

## Summary
- Fixed 21 bugs across 4 crates (cmux-core, cmux-ascii, cmux-gtk, cmux-web)
- Added 18 new regression tests
- All 108 cmux-core tests pass, 9 cmux-web tests pass

### Priority 1 - Critical (5 bugs)
| Bug | Description |
|-----|-------------|
| cmux-dy4 | Implemented pane navigation (navigate_left/right/up/down) |
| cmux-7ay | Implemented split_pane() functionality |
| cmux-45g | Enabled GTK socket fetch at startup |
| cmux-mcu | Wired TerminalManager write/resize to VTE terminals |
| cmux-n50 |

## Metadata
- **PR**: #4
- **Merged**: 2026-03-15
- **Author**: jleechan2015
- **Stats**: +1871/-162 in 17 files
- **Labels**: none

## Connections
