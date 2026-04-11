---
title: "PR #438: fix: align secondary opinion prompts with unicode-safe truncation"
type: source
tags: [codex]
date: 2025-10-30
source_file: raw/prs-/pr-438.md
sources: []
last_updated: 2025-10-30
---

## Summary
- add unicode-aware truncation helpers with explicit suffixes for snippets and response context in SecondOpinionAgent
- apply truncation when embedding secondary and failed responses plus use display names consistently in streaming synthesis
- extend source extraction tests to cover ellipsis behavior at the 5000 character cap

## Metadata
- **PR**: #438
- **Merged**: 2025-10-30
- **Author**: jleechan2015
- **Stats**: +209/-62 in 4 files
- **Labels**: codex

## Connections
