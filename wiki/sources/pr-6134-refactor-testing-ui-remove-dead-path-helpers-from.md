---
title: "PR #6134: refactor(testing_ui): remove dead path helpers from config"
type: source
tags: []
date: 2026-04-07
source_file: raw/prs-worldarchitect-ai/pr-6134.md
sources: []
last_updated: 2026-04-07
---

## Summary
- Remove unused `_resolve_branch_scoped_dir` and redundant `testing_utils.evidence` imports from `testing_ui/config.py`.
- `SCREENSHOT_DIR` / `VIDEO_DIR` are set directly from `testing_utils.browser.resolve_screenshot_dir` / `resolve_video_dir` (`worldarchitectai`).
- Add `__all__` to document the intended public API for browser tests.
- Tighten `test_testing_utils_centralization` to require imports from `testing_utils.browser`; fix Ruff PLR1714 on module checks in the same file.

## Metadata
- **PR**: #6134
- **Merged**: 2026-04-07
- **Author**: jleechan2015
- **Stats**: +42/-75 in 3 files
- **Labels**: none

## Connections
