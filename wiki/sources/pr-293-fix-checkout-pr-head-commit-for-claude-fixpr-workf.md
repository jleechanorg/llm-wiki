---
title: "PR #293: fix: checkout PR head commit for claude fixpr workflow"
type: source
tags: [codex]
date: 2025-10-11
source_file: raw/prs-/pr-293.md
sources: []
last_updated: 2025-10-11
---

## Summary
- update the FixPR workflow checkout step to pull the pull request head commit directly
- ensure the workflow still runs when GitHub cannot create the merge ref due to conflicts
- allow manual FixPR runs to honor the requested branch when checking out code

## Metadata
- **PR**: #293
- **Merged**: 2025-10-11
- **Author**: jleechan2015
- **Stats**: +1/-1 in 1 files
- **Labels**: codex

## Connections
