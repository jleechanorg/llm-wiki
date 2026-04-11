---
title: "PR #105: fix: keep SecretManager JSON credential support across deploy copies"
type: source
tags: [codex]
date: 2025-10-01
source_file: raw/prs-/pr-105.md
sources: []
last_updated: 2025-10-01
---

## Summary
- document that `deploy.sh` copies the shared library sources into `backend/shared-libs`, which overwrites direct edits to the backend copy of `SecretManager.ts`
- move the GOOGLE_APPLICATION_CREDENTIALS_JSON handling into the canonical shared library version so deploy-time sync keeps the JSON credential flow
- add regression tests that cover successful JSON credential parsing and the fallback path when parsing fails

## Metadata
- **PR**: #105
- **Merged**: 2025-10-01
- **Author**: jleechan2015
- **Stats**: +171/-65 in 2 files
- **Labels**: codex

## Connections
