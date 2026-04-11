---
title: "PR #343: [agento] fix(scm-github): fail-closed CI status when no checks reported (bd-jp7q)"
type: source
tags: []
date: 2026-04-02
source_file: raw/prs-worldai_claw/pr-343.md
sources: []
last_updated: 2026-04-02
---

## Summary
- **Bug**: `getCISummary` returned `"none"` when no CI checks were reported, passing the merge gate despite CI not actually passing
- **Root cause**: `checks.length === 0` → `"none"` → Gate 1 passed, but CI was not confirmed green
- **Impact**: PR #254 merged with Test+Lint failing

## Metadata
- **PR**: #343
- **Merged**: 2026-04-02
- **Author**: jleechan2015
- **Stats**: +103/-30 in 3 files
- **Labels**: none

## Connections
