---
title: "PR #47: Ensure Firebase config is injected for preview deployments"
type: source
tags: [codex]
date: 2025-10-01
source_file: raw/prs-/pr-47.md
sources: []
last_updated: 2025-10-01
---

## Summary
- inject runtime Firebase config into the served index.html so Cloud Run env variables populate the client
- expose Firebase secrets to PR preview deployments through github-actions-deploy secret mappings
- include Firebase environment variables when deploying via Cloud Build

## Metadata
- **PR**: #47
- **Merged**: 2025-10-01
- **Author**: jleechan2015
- **Stats**: +806/-30 in 14 files
- **Labels**: codex

## Connections
