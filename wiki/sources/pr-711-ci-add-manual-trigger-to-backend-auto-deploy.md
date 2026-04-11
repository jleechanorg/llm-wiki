---
title: "PR #711: ci: add manual trigger to backend auto deploy"
type: source
tags: []
date: 2025-11-13
source_file: raw/prs-/pr-711.md
sources: []
last_updated: 2025-11-13
---

## Summary
- add workflow_dispatch with optional reason input to auto-deploy
- forward reason/ref_name to deploy-dev as in frontend PR #240
- remove redundant deploy-dev-manual wrapper (auto workflow now exposes Run button)

## Metadata
- **PR**: #711
- **Merged**: 2025-11-13
- **Author**: jleechan2015
- **Stats**: +7/-22 in 2 files
- **Labels**: none

## Connections
