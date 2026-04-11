---
title: "PR #205: fix(evidence-gate): fail instead of skip when no Evidence section"
type: source
tags: []
date: 2026-03-26
source_file: raw/prs-worldai_claw/pr-205.md
sources: []
last_updated: 2026-03-26
---

## Summary
AO workers can bypass the evidence gate by omitting the `## Evidence` section from the PR body. The workflow previously set `found=false` and silently passed when no `## Evidence` section was found. Combined with `gh pr merge --auto` (which only waits for CI status) and branch protection with no required checks, this allowed PRs to merge without CodeRabbit approval or any evidence review.

## Metadata
- **PR**: #205
- **Merged**: 2026-03-26
- **Author**: jleechan2015
- **Stats**: +15/-3 in 1 files
- **Labels**: none

## Connections
