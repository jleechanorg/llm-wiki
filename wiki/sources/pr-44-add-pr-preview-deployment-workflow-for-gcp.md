---
title: "PR #44: Add PR preview deployment workflow for GCP"
type: source
tags: [codex]
date: 2025-09-26
source_file: raw/prs-/pr-44.md
sources: []
last_updated: 2025-09-26
---

## Summary
- add a PR-triggered workflow that authenticates to GCP, runs deploy.sh, and deploys each pull request to its own preview Cloud Run service identified by PR number
- label deployed preview services, surface the preview URL on the pull request, and warn about preview services older than 24 hours
- extend deploy.sh to support overriding the service name, Redis instance, and CORS origins so the workflow can safely create per-PR environments

## Metadata
- **PR**: #44
- **Merged**: 2025-09-26
- **Author**: jleechan2015
- **Stats**: +24118/-66 in 50 files
- **Labels**: codex

## Connections
