---
title: "PR #6075: fix(avatar): resolve CodeRabbit CHANGES_REQUESTED — seed avatar, improve evidence, remove dead code"
type: source
tags: []
date: 2026-04-05
source_file: raw/prs-worldarchitect-ai/pr-6075.md
sources: []
last_updated: 2026-04-05
---

## Summary
Avatar downloads in `firestore_service.py` were returning `(None, None)` on not-found, masking errors from callers. The GCS `list_blobs` probe silently dropped valid blobs with `blob.updated is None`. Non-404 errors in the fallback probe were swallowed, giving callers a misleading 404.

Closes #6058

## Metadata
- **PR**: #6075
- **Merged**: 2026-04-05
- **Author**: jleechan2015
- **Stats**: +629/-909 in 7 files
- **Labels**: none

## Connections
