---
title: "PR #2223: Clean up JSON/serialization; consolidate entities; fix HP validation"
type: source
tags: []
date: 2025-12-01
source_file: raw/prs-worldarchitect-ai/pr-2223.md
sources: []
last_updated: 2025-12-01
---

## Summary
- centralize JSON serialization (new mvp_site/serialization.py) and remove duplicates
- merge robust_json_parser into json_utils and delete dead debug modules; clean stale refs
- consolidate entity validation/preloader with shims, remove dead code, and enforce hp <= hp_max
- add mega-file decomposition note to CODE_REVIEW_SUMMARY.md

## Metadata
- **PR**: #2223
- **Merged**: 2025-12-01
- **Author**: jleechan2015
- **Stats**: +879/-1416 in 32 files
- **Labels**: none

## Connections
