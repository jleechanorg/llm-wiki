---
title: "PR #691: ci: share backend dev workflow"
type: source
tags: []
date: 2025-11-13
source_file: raw/prs-/pr-691.md
sources: []
last_updated: 2025-11-13
---

## Summary
- move the dev deployment job into deploy-dev.yml so manual dispatches and auto-deploy reuse the same steps
- capture commit metadata inside the reusable workflow and keep health checks + failure issue logic intact

## Metadata
- **PR**: #691
- **Merged**: 2025-11-13
- **Author**: jleechan2015
- **Stats**: +209/-143 in 2 files
- **Labels**: none

## Connections
