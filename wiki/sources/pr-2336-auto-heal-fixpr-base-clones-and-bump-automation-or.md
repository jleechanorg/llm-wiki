---
title: "PR #2336: Auto-heal fixpr base clones and bump automation/orchestration"
type: source
tags: []
date: 2025-12-10
source_file: raw/prs-worldarchitect-ai/pr-2336.md
sources: []
last_updated: 2025-12-10
---

## Summary
- Auto-reclone base worktrees if git fetch fails (prevents stuck fixpr runs on corrupted packs)
- Add logging when failing-check detection errors during eligibility listing
- Publish and pin latest packages: orchestration 0.1.11, automation 0.2.6 (depends on >=0.1.11)

## Metadata
- **PR**: #2336
- **Merged**: 2025-12-10
- **Author**: jleechan2015
- **Stats**: +61/-5 in 4 files
- **Labels**: none

## Connections
