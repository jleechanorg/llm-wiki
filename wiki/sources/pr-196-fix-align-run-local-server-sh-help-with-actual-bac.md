---
title: "PR #196: Fix: Align run_local_server.sh help with actual backend URL handling"
type: source
tags: []
date: 2025-11-12
source_file: raw/prs-/pr-196.md
sources: []
last_updated: 2025-11-12
---

## Summary
Fixed misalignment between help text and actual implementation in `run_local_server.sh` where the help claimed to support both "host:port" and "full URL" formats, but the code only handled "host:port" format correctly.

## Metadata
- **PR**: #196
- **Merged**: 2025-11-12
- **Author**: jleechan2015
- **Stats**: +21/-11 in 1 files
- **Labels**: none

## Connections
