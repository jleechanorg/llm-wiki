---
title: "PR #100: ci: add manual convo deploy workflow"
type: source
tags: []
date: 2025-11-13
source_file: raw/prs-/pr-100.md
sources: []
last_updated: 2025-11-13
---

## Summary
- add a workflow_dispatch wrapper that forwards to deploy-dev.yml so we can manually trigger convo dev deploys without waiting on GitHub to refresh the reusable workflow metadata
- the wrapper exposes the same reason input and inherits secrets so behavior matches the auto-deploy path

## Metadata
- **PR**: #100
- **Merged**: 2025-11-13
- **Author**: jleechan2015
- **Stats**: +21/-0 in 1 files
- **Labels**: none

## Connections
