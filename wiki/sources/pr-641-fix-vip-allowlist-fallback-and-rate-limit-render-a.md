---
title: "PR #641: fix: VIP allowlist fallback and RATE_LIMIT_RENDER_ASSUME_SINGLE support"
type: source
tags: []
date: 2025-11-11
source_file: raw/prs-/pr-641.md
sources: []
last_updated: 2025-11-11
---

## Summary
Fixes VIP allowlist fallback support and critical bug where `RATE_LIMIT_RENDER_ASSUME_SINGLE` was not being honored, which caused production deployments on Render/Cloud Run to incorrectly apply ultra-strict 1 req/min limits.

## Metadata
- **PR**: #641
- **Merged**: 2025-11-11
- **Author**: jleechan2015
- **Stats**: +205/-8 in 4 files
- **Labels**: none

## Connections
