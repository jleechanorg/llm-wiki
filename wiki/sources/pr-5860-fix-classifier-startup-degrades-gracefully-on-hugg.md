---
title: "PR #5860: fix: classifier startup degrades gracefully on HuggingFace 429"
type: source
tags: []
date: 2026-03-05
source_file: raw/prs-worldarchitect-ai/pr-5860.md
sources: []
last_updated: 2026-03-05
---

## Summary
- Extract `check_classifier_startup()` from `create_app()` into `intent_classifier.py`
- Change `raise RuntimeError` to `logging_util.warning` when classifier model download fails
- Prevents Cloud Run crash loop when HuggingFace returns 429 (rate limiting)
- Semantic routing degrades to MODE_CHARACTER fallback automatically

## Metadata
- **PR**: #5860
- **Merged**: 2026-03-05
- **Author**: jleechan2015
- **Stats**: +108/-140 in 4 files
- **Labels**: none

## Connections
