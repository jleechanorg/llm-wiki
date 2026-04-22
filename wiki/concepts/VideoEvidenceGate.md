---
title: "Video Evidence Gate"
type: concept
tags: [video, evidence, gate, skeptic, worldai]
last_updated: 2026-04-14
---

## Summary

Video Evidence Gate is the Skeptic Gate component that validates video artifacts (asciinema recordings, GIFs, MP4s) submitted as evidence. It extracts frames, runs OCR, and checks for required content.

## Validation Steps

### 1. Format Validation
```python
def validate_video_format(path: str) -> bool:
    valid_extensions = {".mp4", ".gif", ".cast", ".webm"}
    return Path(path).suffix.lower() in valid_extensions
```

### 2. Duration Check
```python
def validate_duration(path: str) -> tuple[bool, str]:
    duration = get_video_duration(path)
    if duration == 0:
        return False, "Video has zero duration"
    if duration > 60:
        return False, "Video exceeds 60s without justification"
    return True, "ok"
```

### 3. Content Extraction
```python
async def extract_frames(path: str) -> list[Image]:
    if path.endswith(".cast"):
        return extract_asciinema_frames(path)
    return extract_video_frames(path)  # ffmpeg-based
```

### 4. OCR Validation
```python
async def validate_text_in_video(frames: list[Image], required_text: list[str]) -> bool:
    for frame in frames:
        text = await ocr_image(frame)
        if any(term in text.lower() for term in required_text):
            return True
    return False
```

## Pass Criteria

- Format is valid
- Duration is 1-60 seconds
- Required text appears in at least one frame
- No error states visible (blank screens, exception traces)

## Connections
- [[VideoFrameExtraction]] — Frame extraction details
- [[VideoEvidenceFailure]] — Failure mode analysis
- [[EvidencePipeline]] — Evidence collection pipeline
- [[SkepticGate]] — Parent gate system
