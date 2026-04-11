---
title: "PR #5761: CI: disable non-core self-hosted jobs and pin MVP shards to mac"
type: source
tags: []
date: 2026-02-24
source_file: raw/prs-worldarchitect-ai/pr-5761.md
sources: []
last_updated: 2026-02-24
---

## Summary
- disable non-core self-hosted usage by moving migrated heavy workflows back to `ubuntu-latest`
- keep new self-hosted code in the MVP shard workflow, but disable harness autonomy jobs for now (`if: false`)
- restrict active self-hosted MVP shard jobs to mac runners via labels: `[self-hosted, claude, macOS, ARM64]`

## Metadata
- **PR**: #5761
- **Merged**: 2026-02-24
- **Author**: jleechan2015
- **Stats**: +39/-14 in 7 files
- **Labels**: none

## Connections
