---
title: "PR #151: fix: restrict CORS wildcard to Cloud Run domains"
type: source
tags: [codex]
date: 2025-10-03
source_file: raw/prs-/pr-151.md
sources: []
last_updated: 2025-10-03
---

## Summary
- tighten the default backend CORS wildcard so that only Cloud Run run.app hosts are accepted
- align the production deploy configuration and unit tests with the safer origin pattern and ensure lookalike domains are rejected

## Metadata
- **PR**: #151
- **Merged**: 2025-10-03
- **Author**: jleechan2015
- **Stats**: +17/-3 in 3 files
- **Labels**: codex

## Connections
