---
title: "PR #3685: fix: Skip fixpr on clean PRs with no conflicts or failing checks"
type: source
tags: []
date: 2026-01-17
source_file: raw/prs-worldarchitect-ai/pr-3685.md
sources: []
last_updated: 2026-01-17
---

## Summary
- Fixpr automation was processing PRs even when they had no merge conflicts and all CI checks were passing
- This caused unnecessary automation runs that spammed clean PRs like #3682 with queued notices
- Root cause: Skip logic only checked PR status IF commit was already processed, not for new commits

## Metadata
- **PR**: #3685
- **Merged**: 2026-01-17
- **Author**: jleechan2015
- **Stats**: +808/-185 in 9 files
- **Labels**: none

## Connections
