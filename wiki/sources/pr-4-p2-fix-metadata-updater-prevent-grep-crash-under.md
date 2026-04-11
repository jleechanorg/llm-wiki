---
title: "PR #4: [P2] fix(metadata-updater): prevent grep crash under set -e"
type: source
tags: []
date: 2026-03-29
source_file: raw/prs-/pr-4.md
sources: []
last_updated: 2026-03-29
---

## Summary
- Fix grep crash in `.claude/metadata-updater.sh` when no PR URL is found in output
- With `set -euo pipefail`, `grep -Eo` returns exit code 1 on no-match causing script abort; add `|| true` to make the pipeline exit 0

## Metadata
- **PR**: #4
- **Merged**: 2026-03-29
- **Author**: jleechan2015
- **Stats**: +406/-2 in 6 files
- **Labels**: none

## Connections
