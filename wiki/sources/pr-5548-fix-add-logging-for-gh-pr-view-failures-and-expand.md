---
title: "PR #5548: fix: add logging for gh pr view failures and expand wrap_prompt docstring"
type: source
tags: []
date: 2026-02-16
source_file: raw/prs-worldarchitect-ai/pr-5548.md
sources: []
last_updated: 2026-02-16
---

## Summary
Addresses two follow-up chores from PR #5546:

### REV-xpge0: Add logging for silent `gh pr view` subprocess failures
- Replaced silent `except Exception: pass` with `logger.debug("gh_pr_view_failed", ...)` including PR number and `exc_info=True`
- Added `logger.debug("gh_pr_view_nonzero_exit", ...)` for non-zero exit codes with returncode and stderr context

### REV-6kk7k: Expand `wrap_prompt` docstring
- Expanded docstring for the `wrap_prompt` parameter in `analyze_task_and_create_agents` to

## Metadata
- **PR**: #5548
- **Merged**: 2026-02-16
- **Author**: jleechan2015
- **Stats**: +85/-3 in 2 files
- **Labels**: none

## Connections
