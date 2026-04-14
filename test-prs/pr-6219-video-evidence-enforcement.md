---
title: "PR #6219: feat(testing): add video evidence enforcement to base classes"
type: test-pr
date: 2026-04-12
pr_number: 6219
files_changed: [base_test.py, testing_ui/streaming/base.py, mock_llm_service.py, validate_imports.py, pr-6219.md, testing_ui/CLAUDE.md]
---

## Summary
Adds shared video-evidence capture to test infrastructure. `TmuxVideoRecorder` for testing_mcp (tmux console recording → .gif + .mp4) and `UIVideoRecorder` for testing_ui (browser UI recording via ffmpeg x11grab). Both produce BOTH .gif AND .mp4 per /es evidence standards.

## Key Changes
- **base_test.py**: Added `TmuxVideoRecorder` class with VIDEO_AVAILABLE check, H.264-safe scaling for MP4
- **testing_ui/streaming/base.py**: Added `UIVideoRecorder`, auto-enables when ffmpeg + display available, enforces both .mp4 and .gif before checksums, SIGINT shutdown
- **mock_llm_service.py**: Tweaks to better detect when to return structured responses (Think mode cues)
- **validate_imports.py**: Added video deps to allowed conditional imports

## Motivation
Evidence standards require video artifacts, but tests weren't consistently producing them. Both terminal and UI recording now mandatory when tools available.