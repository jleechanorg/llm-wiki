---
title: "PR #322: Fix stale shared-libs detection and rebuild automation"
type: source
tags: [codex]
date: 2025-10-13
source_file: raw/prs-/pr-322.md
sources: []
last_updated: 2025-10-13
---

## Summary
- Guard the shared-libs preparation script against missing dependency maps while preserving recursive dependency resolution to keep installs reliable. 
- Clear `node_modules` before every `npm ci` invocation in the backend coverage workflow so cached file: tarballs cannot serve stale builds.
- Run the CI environment replication script’s apt installs in noninteractive mode and check specifically for the Bazelisk package directory to avoid false positives.

## Metadata
- **PR**: #322
- **Merged**: 2025-10-13
- **Author**: jleechan2015
- **Stats**: +17/-9 in 3 files
- **Labels**: codex

## Connections
