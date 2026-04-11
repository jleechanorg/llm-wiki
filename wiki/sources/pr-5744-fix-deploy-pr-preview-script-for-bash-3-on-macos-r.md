---
title: "PR #5744: Fix Deploy PR Preview script for Bash 3 on macOS runners"
type: source
tags: []
date: 2026-02-23
source_file: raw/prs-worldarchitect-ai/pr-5744.md
sources: []
last_updated: 2026-02-23
---

## Summary
- remove Bash 4 associative-array usage from `.github/scripts/pr-server-pool.sh`
- replace it with Bash 3 compatible `jq` lookup logic
- preserve existing assignment output format and behavior

## Metadata
- **PR**: #5744
- **Merged**: 2026-02-23
- **Author**: jleechan2015
- **Stats**: +67/-32 in 2 files
- **Labels**: none

## Connections
