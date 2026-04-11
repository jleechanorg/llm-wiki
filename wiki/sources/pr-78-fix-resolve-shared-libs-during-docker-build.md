---
title: "PR #78: fix: resolve shared libs during docker build"
type: source
tags: [codex]
date: 2025-09-28
source_file: raw/prs-/pr-78.md
sources: []
last_updated: 2025-09-28
---

## Summary
- copy the shared libraries into `/shared-libs` before running npm installs so file: dependencies resolve inside the container
- allow both `/shared-libs` and in-repo `shared-libs` paths when re-installing the packages in each stage of the Docker build

## Metadata
- **PR**: #78
- **Merged**: 2025-09-28
- **Author**: jleechan2015
- **Stats**: +85/-30 in 3 files
- **Labels**: codex

## Connections
