---
title: "PR #2263: Fix Cerebras provider to handle Qwen 3 reasoning field response"
type: source
tags: []
date: 2025-12-02
source_file: raw/prs-worldarchitect-ai/pr-2263.md
sources: []
last_updated: 2025-12-02
---

## Summary
- Fixed `cerebras_provider.py` to handle responses where content is returned in `reasoning` field instead of `content`
- This fixes production failures on dev environment when using Qwen 3 models

## Metadata
- **PR**: #2263
- **Merged**: 2025-12-02
- **Author**: jleechan2015
- **Stats**: +100/-1 in 2 files
- **Labels**: none

## Connections
