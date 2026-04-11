---
title: "PR #713: Consolidate CI workflows to reduce runner usage"
type: source
tags: [codex]
date: 2025-11-17
source_file: raw/prs-/pr-713.md
sources: []
last_updated: 2025-11-17
---

## Summary
- fold the standalone integration and type-check workflows into the primary CI pipeline so every push/PR runs only one job
- run the real-server integration tests directly inside `ci.yml` after the regular `./scripts/run_tests.sh` step and drop the Node 22 matrix entry
- update the cost optimization note to reflect the new workflow layout and savings

## Metadata
- **PR**: #713
- **Merged**: 2025-11-17
- **Author**: jleechan2015
- **Stats**: +484/-239 in 5 files
- **Labels**: codex

## Connections
