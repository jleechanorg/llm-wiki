---
title: "PR #2270: Follow-up: improve Cerebras message parsing robustness"
type: source
tags: [codex]
date: 2025-12-02
source_file: raw/prs-worldarchitect-ai/pr-2270.md
sources: []
last_updated: 2025-12-02
---

## Summary
- make message parsing case-insensitive and only fall back to reasoning when content is absent
- validate message objects are dicts and handle empty content without overriding it
- expand Cerebras provider tests for reasoning, precedence, and empty content handling

## Metadata
- **PR**: #2270
- **Merged**: 2025-12-02
- **Author**: jleechan2015
- **Stats**: +89/-35 in 2 files
- **Labels**: codex

## Connections
