---
title: "PR #5754: chore: add shared classifier preflight and startup gating"
type: source
tags: []
date: 2026-03-04
source_file: raw/prs-worldarchitect-ai/pr-5754.md
sources: []
last_updated: 2026-03-04
---

## Summary
- Add shared preflight script for classifier model cache repair + warmup.
- Hook run_local_server.sh to preflight-check classifier before launching Flask.
- Replace Dockerfile inline model bootstrap with shared preflight_model.py.
- Add server startup gate in main.py so startup fails fast if semantic classifier is enabled and fails to initialize.

## Metadata
- **PR**: #5754
- **Merged**: 2026-03-04
- **Author**: jleechan2015
- **Stats**: +306/-10 in 8 files
- **Labels**: none

## Connections
