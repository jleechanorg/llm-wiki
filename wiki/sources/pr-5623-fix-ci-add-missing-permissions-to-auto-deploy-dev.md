---
title: "PR #5623: fix(ci): add missing permissions to auto-deploy-dev workflow"
type: source
tags: []
date: 2026-02-18
source_file: raw/prs-worldarchitect-ai/pr-5623.md
sources: []
last_updated: 2026-02-18
---

## Summary
- **Fixed startup_failure** on `auto-deploy-dev.yml` that has been broken since at least Feb 16 (20+ consecutive failures)
- **Root cause**: Top-level `permissions` only granted `contents: read`, but the reusable workflow job passed `issues: write` and needed `pull-requests: read` — GitHub Actions rejects permission escalation beyond the workflow-level grant
- **Fix**: Added `issues: write` and `pull-requests: read` to the top-level permissions block

## Metadata
- **PR**: #5623
- **Merged**: 2026-02-18
- **Author**: jleechan2015
- **Stats**: +3/-0 in 1 files
- **Labels**: none

## Connections
