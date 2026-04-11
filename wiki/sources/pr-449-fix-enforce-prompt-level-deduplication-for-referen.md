---
title: "PR #449: fix: enforce prompt-level deduplication for references"
type: source
tags: [codex]
date: 2025-10-30
source_file: raw/prs-/pr-449.md
sources: []
last_updated: 2025-10-30
---

## Summary
- add shared synthesis-structure instructions that tell models not to repeat Top 5 sources in the All References section
- remove the post-response normalization step so deduplication happens via the generated prompt guidance instead
- update the unit test to assert the new prompt requirement for avoiding duplicate references

## Metadata
- **PR**: #449
- **Merged**: 2025-10-30
- **Author**: jleechan2015
- **Stats**: +15/-8 in 2 files
- **Labels**: codex

## Connections
