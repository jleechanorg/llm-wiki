---
title: "PR #5154: Fix: Prevent duplicate PR comments for same SHA"
type: source
tags: []
date: 2026-02-10
source_file: raw/prs-worldarchitect-ai/pr-5154.md
sources: []
last_updated: 2026-02-10
---

## Summary
Fixes infinite loop where automation posted duplicate "Codex support" comments for the same HEAD SHA every hour.

**Key themes:**
- Remove force_process logic that bypassed duplicate detection
- Remove bot comment detection from is_pr_actionable (complete Option A)
- Simplify to "one comment per SHA max" (Option A)
- Add test coverage for duplicate prevention

## Metadata
- **PR**: #5154
- **Merged**: 2026-02-10
- **Author**: jleechan2015
- **Stats**: +253/-315 in 4 files
- **Labels**: none

## Connections
