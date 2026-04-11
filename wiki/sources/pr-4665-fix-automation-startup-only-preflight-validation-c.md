---
title: "PR #4665: fix(automation): startup-only preflight + validation cleanup"
type: source
tags: []
date: 2026-02-03
source_file: raw/prs-worldarchitect-ai/pr-4665.md
sources: []
last_updated: 2026-02-03
---

## Summary
- remove per-PR quick preflight gating before queued comments
- keep startup preflight as the only heavy validation at workflow start
- persist startup preflight outputs and log retained output file paths
- increase CLI validation timeouts and align comments with 90s/10s values
- expand default assistant mentions to include @copilot
- simplify queued comment validation tests for new preflight behavior
- align optional-dependency tests with pytest.importorskip and remove redundant aiohttp guard

## Metadata
- **PR**: #4665
- **Merged**: 2026-02-03
- **Author**: jleechan2015
- **Stats**: +97/-377 in 7 files
- **Labels**: none

## Connections
