---
title: "PR #2950: fix(ci): Install full requirements for daily campaign report"
type: source
tags: []
date: 2026-01-01
source_file: raw/prs-worldarchitect-ai/pr-2950.md
sources: []
last_updated: 2026-01-01
---

## Summary
- Fixed daily campaign report workflow failing silently due to missing `pydantic` dependency
- Root cause: Workflow only installed `firebase-admin` and `google-cloud-firestore`, but importing `mvp_site` package requires additional dependencies

## Metadata
- **PR**: #2950
- **Merged**: 2026-01-01
- **Author**: jleechan2015
- **Stats**: +6/-4 in 1 files
- **Labels**: none

## Connections
