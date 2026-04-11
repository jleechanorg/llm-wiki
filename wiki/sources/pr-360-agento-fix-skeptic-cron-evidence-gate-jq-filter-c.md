---
title: "PR #360: [agento] fix(skeptic-cron): Evidence Gate jq filter + CLAUDE.md rule + wholesome N/A fix"
type: source
tags: []
date: 2026-04-04
source_file: raw/prs-worldai_claw/pr-360.md
sources: []
last_updated: 2026-04-04
---

## Summary
PR #360 fixes multiple issues in the skeptic-cron Evidence Gate evaluation and wholesome.yml evidence checks. The jq filters had a null/missing conflation bug that made in-progress checks unreachable, and the GATE_COMMENT selector could pick stale results.

## Metadata
- **PR**: #360
- **Merged**: 2026-04-04
- **Author**: jleechan2015
- **Stats**: +115/-38 in 6 files
- **Labels**: none

## Connections
