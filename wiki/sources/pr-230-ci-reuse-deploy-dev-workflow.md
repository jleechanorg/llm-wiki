---
title: "PR #230: ci: reuse deploy-dev workflow"
type: source
tags: []
date: 2025-11-13
source_file: raw/prs-/pr-230.md
sources: []
last_updated: 2025-11-13
---

## Summary
- extract the dev deployment logic into a reusable workflow so auto-deploy and manual runs share the exact same steps
- keep the full Cloud Run deploy, health check, and failure issue path in deploy-dev.yml, then call it from the push-triggered workflow

## Metadata
- **PR**: #230
- **Merged**: 2025-11-13
- **Author**: jleechan2015
- **Stats**: +215/-172 in 2 files
- **Labels**: none

## Connections
