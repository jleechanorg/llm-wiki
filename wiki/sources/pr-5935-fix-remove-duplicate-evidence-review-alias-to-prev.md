---
title: "PR #5935: fix: remove duplicate evidence_review alias to prevent recursion"
type: source
tags: []
date: 2026-03-10
source_file: raw/prs-worldarchitect-ai/pr-5935.md
sources: []
last_updated: 2026-03-10
---

## Summary
- Remove duplicate `aliases: [evidence_review]` from er.md since evidence_review.md already declares `aliases: [er]`
- Having bidirectional aliases causes recursive command resolution

## Metadata
- **PR**: #5935
- **Merged**: 2026-03-10
- **Author**: jleechan2015
- **Stats**: +0/-1 in 1 files
- **Labels**: none

## Connections
