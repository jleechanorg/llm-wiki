---
title: "PR #373: [agento] fix(harness): add churn-guard PreToolUse hook to block duplicate-file PRs"
type: source
tags: []
date: 2026-04-04
source_file: raw/prs-worldai_claw/pr-373.md
sources: []
last_updated: 2026-04-04
---

## Summary
On 2026-04-04, **8 PRs** (363, 366-372) were created for the same file (`.claude/metadata-updater.sh`) in under 1 hour. 7 were wasted duplicates — all CONFLICTING after PR #367 merged first. Root cause: AO workers had no file-level coordination gate at PR creation time.

Per harness severity table: "repeated manual fix" requires a **hook**, not just instructions.

## Metadata
- **PR**: #373
- **Merged**: 2026-04-04
- **Author**: jleechan2015
- **Stats**: +527/-2 in 5 files
- **Labels**: none

## Connections
