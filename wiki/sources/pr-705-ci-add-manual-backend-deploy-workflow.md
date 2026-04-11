---
title: "PR #705: ci: add manual backend deploy workflow"
type: source
tags: []
date: 2025-11-13
source_file: raw/prs-/pr-705.md
sources: []
last_updated: 2025-11-13
---

## Summary
- add a thin workflow_dispatch wrapper so we can manually trigger backend dev deploys without depending on the reusable workflow metadata cache
- wrapper just forwards inputs to the existing deploy-dev.yml so auto-deploy keeps using the same steps

## Metadata
- **PR**: #705
- **Merged**: 2025-11-13
- **Author**: jleechan2015
- **Stats**: +21/-0 in 1 files
- **Labels**: none

## Connections
