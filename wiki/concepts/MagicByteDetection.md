---
title: "Magic Byte Detection"
type: concept
tags: [file-detection, image-processing, security]
sources: ["avatar-api-layer-1-unit-tests"]
last_updated: 2026-04-08
---

Magic byte detection is a technique for identifying file types by examining their header bytes (magic numbers). For images:
- **JPEG**: `\xff\xd8\xff`
- **PNG**: `\x89PNG\r\n\x1a\n`
- **GIF87a/GIF89a**: `GIF87a` / `GIF89a`
- **WEBP**: `RIFF....WEBP` (RIFF header + WEBP fourcc)

**Mentioned in**: [[Avatar API Layer 1 Unit Tests]]
