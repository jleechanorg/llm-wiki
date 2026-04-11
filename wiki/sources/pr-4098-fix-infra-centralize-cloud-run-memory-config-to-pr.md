---
title: "PR #4098: fix(infra): Centralize Cloud Run memory config to prevent drift"
type: source
tags: []
date: 2026-01-27
source_file: raw/prs-worldarchitect-ai/pr-4098.md
sources: []
last_updated: 2026-01-27
---

## Summary
- Centralize Cloud Run resource allocation (memory, CPU) in `scripts/shared_config.sh`
- Update `deploy.sh` and `pr-preview.yml` to use shared config
- Fixes PR preview OOM errors caused by mismatched memory limits

## Metadata
- **PR**: #4098
- **Merged**: 2026-01-27
- **Author**: jleechan2015
- **Stats**: +13/-4 in 3 files
- **Labels**: none

## Connections
