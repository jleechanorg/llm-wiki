---
title: "PR #452: [agento] fix(scripts): anchor spawn success grep to ✓ to prevent false positives"
type: source
tags: []
date: 2026-03-30
source_file: raw/prs-worldai_claw/pr-452.md
sources: []
last_updated: 2026-03-30
---

## Summary
When `ao spawn --claim-pr` fails during `git checkout` (e.g., branch locked by another worktree), the error message printed is: `"Session X was created, but failed to claim PR Y: ..."`. This message contains the substring "Session X was created, but failed to claim PR" which matched the unanchored grep pattern `"Session .* created and claimed PR"` in `github-intake.sh`, causing the poller to log SUCCESS even though checkout failed.

## Metadata
- **PR**: #452
- **Merged**: 2026-03-30
- **Author**: jleechan2015
- **Stats**: +923/-50 in 12 files
- **Labels**: none

## Connections
