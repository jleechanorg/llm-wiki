---
title: "PR #6: feat(gcp): add Cloud Run deployment for gateway + relay services"
type: source
tags: []
date: 2026-04-05
source_file: raw/prs-/pr-6.md
sources: []
last_updated: 2026-04-05
---

## Summary
- **deploy.sh**: local/dev/staging/prod deploy script using `gcloud run deploy`
- **cloudbuild.yaml**: Cloud Build pipeline (shared → gateway → relay images to GCR)
- **deploy-dev.yml**: GitHub Actions — PR previews + main-branch pushes deploy to Cloud Run dev/staging
- **deploy-production.yml**: GitHub Actions — manual workflow_dispatch for prod with environment approval gate
- **smoke-test.yml** + **scripts/gcp-smoke-test.mjs**: E2E smoke test (gateway health + relay health + streaming error)

## Metadata
- **PR**: #6
- **Merged**: 2026-04-05
- **Author**: jleechan2015
- **Stats**: +2475/-39 in 49 files
- **Labels**: none

## Connections
