---
title: "PR #31: fix: restore MAX_CONTENT_LENGTH to 200,000 characters"
type: source
tags: []
date: 2025-10-10
source_file: raw/prs-/pr-31.md
sources: []
last_updated: 2025-10-10
---

## Summary
Fixes critical regression in MAX_CONTENT_LENGTH that was dropped from 200,000 to 10,000 characters, breaking existing workflows that send longer content (LLM transcripts, attachments).

## Metadata
- **PR**: #31
- **Merged**: 2025-10-10
- **Author**: jleechan2015
- **Stats**: +41/-4 in 4 files
- **Labels**: none

## Connections
