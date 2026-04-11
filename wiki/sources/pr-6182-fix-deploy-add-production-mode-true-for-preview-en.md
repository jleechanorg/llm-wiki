---
title: "PR #6182: fix(deploy): add PRODUCTION_MODE=true for preview environment"
type: source
tags: []
date: 2026-04-10
source_file: raw/prs-worldarchitect-ai/pr-6182.md
sources: []
last_updated: 2026-04-10
---

## Summary
- Add `PRODUCTION_MODE=true` to the preview environment case in `deploy.sh`
- Preview deployments now enforce production auth like staging/stable
- Fixes bug rev-w1dt from PR #6174 where preview had weaker auth enforcement

## Metadata
- **PR**: #6182
- **Merged**: 2026-04-10
- **Author**: jleechan2015
- **Stats**: +10/-3 in 2 files
- **Labels**: none

## Connections
