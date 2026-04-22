---
title: "Video Frame Extraction"
type: concept
tags: [video, frames, extraction, evidence, worldai]
last_updated: 2026-04-14
---

## Summary

Video Frame Extraction is the process of converting video artifacts (asciinema recordings, terminal recordings, browser captures) into individual image frames for OCR-based validation.

## Asciinema (.cast) Files

Asciinema recordings are terminal session recordings in a specific JSON format:
```python
def extract_asciinema_frames(cast_path: str) -> list[Image]:
    with open(cast_path) as f:
        events = json.load(f)

    frames = []
    terminal_renderer = TerminalRenderer()

    for timestamp, _, data in events:
        # data is ANSI escape sequences + text
        frame = terminal_renderer.render(data, timestamp)
        frames.append(frame)

    return frames
```

## FFmpeg-Based Extraction

For MP4/WebM/GIF:
```bash
ffmpeg -i input.mp4 -vf "fps=1" frame_%03d.png
```

```python
def extract_video_frames(video_path: str, fps: int = 1) -> list[Image]:
    output_dir = tempfile.mkdtemp()
    subprocess.run([
        "ffmpeg", "-i", video_path,
        "-vf", f"fps={fps}",
        "-q:v", "2",  # Quality setting
        f"{output_dir}/frame_%03d.png"
    ])
    return [Image.open(f) for f in sorted(Path(output_dir).glob("*.png"))]
```

## Frame Selection

Not all frames need OCR — select key frames:
1. First frame (verify recording started)
2. Every 5th frame (sampling)
3. Last frame (verify completion)

## OCR Pipeline

```python
async def ocr_frames(frames: list[Image]) -> list[str]:
    texts = []
    for frame in frames:
        text = await async_ocr(frame)  # Use pytesseract or cloud OCR
        texts.append(text)
    return texts
```

## Connections
- [[VideoEvidenceGate]] — Gate that uses extracted frames
- [[VideoEvidenceFailure]] — Failure analysis
- [[EvidencePipeline]] — Evidence collection
