---
title: "PR #134: fix: correct PATCH endpoint for skeptic gate trigger comments"
type: source
tags: []
date: 2026-03-28
source_file: raw/prs-worldai_claw/pr-134.md
sources: []
last_updated: 2026-03-28
---

## Summary
- Fix HTTP 404 error when Skeptic Gate workflow tries to update existing trigger comments
- Root cause: `issues/{pr_num}/comments/{id}` is not a valid GET/PATCH endpoint; correct endpoint is `issues/comments/{id}`
- This caused all Skeptic Gate runs to fail immediately whenever a concurrent cancelled run had already posted a trigger comment

## Metadata
- **PR**: #134
- **Merged**: 2026-03-28
- **Author**: jleechan2015
- **Stats**: +1/-1 in 1 files
- **Labels**: none

## Connections
