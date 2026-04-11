---
title: "PR #6052: fix(tests): convert 9 async tests to use asyncio.run()"
type: source
tags: []
date: 2026-03-31
source_file: raw/prs-worldarchitect-ai/pr-6052.md
sources: []
last_updated: 2026-03-31
---

## Summary
9 tests across 4 files used @pytest.mark.asyncio but pytest-asyncio is not installed, causing silent FAILED results.

## Metadata
- **PR**: #6052
- **Merged**: 2026-03-31
- **Author**: jleechan2015
- **Stats**: +86/-69 in 4 files
- **Labels**: none

## Connections
