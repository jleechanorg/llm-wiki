---
title: "OCR Teardown Validation"
type: concept
tags: [testing, video-capture, verification, ocr, e2e-testing]
sources: []
last_updated: 2026-04-13
---

## Summary
A test verification approach that extracts frames at key positions (25%, 50%, 75%, final) during test teardown and runs OCR to validate that the game displayed meaningful content, not error states. Replaces duration-only validation with content-aware verification.

## The Problem

The original video verification in worldarchitect.ai E2E tests used duration-only checks:

```python
# Original verification
duration = ffprobe.get_duration(video_path)
assert duration >= 20  # 20 second minimum
```

This passes when:
- A valid .webm file exists
- ffprobe reports valid metadata
- Frame count >= 20

**The failure case:** A 101.76-second video was created showing "[CHARACTER CREATION - No Character Built]" throughout. Duration passed. Frame count passed. But the game was non-functional the entire time.

## The Solution

At test teardown, extract frames at multiple positions and validate content:

```python
def validate_video_content(video_path, expected_scenes=None):
    # Extract frames at key positions
    positions = [0.25, 0.5, 0.75, 1.0]
    frames = extract_frames_at_positions(video_path, positions)
    
    for frame in frames:
        text = ocr_extract(frame)  # Use pytesseract or similar
        
        # Check for error states
        if is_error_state(text):
            raise AssertionError(f"Error state detected in video: {text}")
    
    # Optionally verify expected content present
    if expected_scenes:
        for frame in frames:
            frame_text = ocr_extract(frame)
            if not any(scene in frame_text for scene in expected_scenes):
                raise AssertionError(f"Expected scene content not found")
```

## Why Multiple Positions?

- **25%**: Captures early game state (initialization, loading)
- **50%**: Middle of session (main gameplay)
- **75%**: Late session (session winding down)
- **100%**: Final frame (end state)

Single-frame validation (e.g., only final frame) can miss issues where:
- Game works early but fails midway
- Game starts broken but recovers
- Error states are intermittent

## Implementation Requirements

1. **Frame extraction**: Use ffmpeg to extract frames at specified positions
2. **OCR**: Use pytesseract, easyocr, or cloud-based OCR
3. **Error pattern detection**: Define patterns like:
   - "[CHARACTER CREATION - No Character Built]"
   - "Error:"
   - "Connection lost"
   - "Loading..." (if persists beyond expected time)
4. **Expected scene list**: Define what content should appear in a passing test

## Connections
- [[Harness5LayerModel]] — this is an L4 (Verification) failure: duration-only checks don't verify meaningful content
- [[CanvasOverlayZIndexIssue]] — the L3 execution issue that caused the capture problems; OCR validation is the L4 complement to fix the verification gap

## Sources
- test_full_lifecycle_video.py
- worldarchitect.ai E2E testing infrastructure
- ffprobe duration validation approach