---
title: "PR #345: feat: add pr preview workflow installer"
type: source
tags: [codex]
date: 2025-10-14
source_file: raw/prs-/pr-345.md
sources: []
last_updated: 2025-10-14
---

## Summary
- add `scripts/install-pr-preview-workflow.sh` to copy the PR preview workflow, deploy script, and smoke tests into downstream repositories
- introduce reusable template assets under `docs/workflows/templates/pr-preview/` with placeholder substitution for project, region, and service naming
- document the installer in `docs/workflows/README.md`, updating the quickstart, setup guidance, and reference snippets to match the new templates

## Metadata
- **PR**: #345
- **Merged**: 2025-10-14
- **Author**: jleechan2015
- **Stats**: +830/-4 in 5 files
- **Labels**: codex

## Connections
