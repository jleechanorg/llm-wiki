---
title: "PR #395: feat(claw): add learning-loop gate (Step A5.5) to /claw Path A"
type: source
tags: []
date: 2026-03-24
source_file: raw/prs-worldai_claw/pr-395.md
sources: []
last_updated: 2026-03-24
---

## Summary
`/integrate` auto-triggers `/learn`, but `/claw` tasks that directly create PRs bypass `/integrate`, silently breaking the learning loop. Caught 2026-03-24. Resolves orch-xlu.

Note: claw.md also contains the full Path A (ao spawn routing) implementation from a prior change — this PR is scoped only to Step A5.5 (learning-loop gate).

## Metadata
- **PR**: #395
- **Merged**: 2026-03-24
- **Author**: jleechan2015
- **Stats**: +372/-18 in 2 files
- **Labels**: none

## Connections
