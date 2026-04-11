---
title: "PR #311: [agento] fix: metadata-updater.sh regex fix and simplification"
type: source
tags: []
date: 2026-03-30
source_file: raw/prs-worldai_claw/pr-311.md
sources: []
last_updated: 2026-03-30
---

## Summary
The metadata-updater.sh PostToolUse hook had 3 issues: a regex that could over-match env-assignment prefixes, unnecessary character escaping in sed, and overly complex git verification for branch detection.

## Metadata
- **PR**: #311
- **Merged**: 2026-03-30
- **Author**: jleechan2015
- **Stats**: +17/-29 in 1 files
- **Labels**: none

## Connections
