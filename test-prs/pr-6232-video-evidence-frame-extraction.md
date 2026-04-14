---
title: "PR #6232: feat(testing): add video evidence frame extraction"
type: test-pr
date: 2026-04-13
pr_number: 6232
files_changed: [extract_video_evidence_frames.sh, base_test.py, evidence_utils.py]
---

## Summary
Adds an opt-in pipeline to extract reviewable JPEG frames from generated .webm/.mp4 evidence videos. Provides "review" mode (1fps, scene-change thumbnails, tiled contact sheet, manifest) and "all" mode (every frame). Extraction runs non-fatal and emits warnings if tools or videos are missing.

## Key Changes
- **extract_video_evidence_frames.sh**: New script with hard-fail on unrecognized modes, proper ffprobe/ffmpeg error handling, correct shebang path
- **base_test.py**: Revised video recording/bundling flow, supports companion asciinema recording, shortened conversion timeouts (60s → 30s)
- **evidence_utils.py**: Catches ffmpeg errors to enforce non-zero return codes, prevents silent extraction skips

## Motivation
Test suites in CI often omit visual video evidence. This provides automated frame extraction for /es compliance.