---
title: "PR #292: fix(harness): teach agents to detect empty-body CR APPROVED as fake"
type: source
tags: []
date: 2026-03-20
source_file: raw/prs-worldai_claw/pr-292.md
sources: []
last_updated: 2026-03-20
---

## Summary
After merging PR #278 (https://github.com/jleechanorg/jleechanclaw/pull/278) which added empty-body CR APPROVED detection to the merge gate, we ran an E2E test dispatching 9 open PRs to agento via /claw. All 9 PRs reached CI-clean + mergeable, but **0/9 achieved genuine CR approval**. The agents saw `state: APPROVED` and stopped — not realizing `body=0` means it was auto-triggered by thread resolution.

## Metadata
- **PR**: #292
- **Merged**: 2026-03-20
- **Author**: jleechan2015
- **Stats**: +265/-26 in 5 files
- **Labels**: none

## Connections
