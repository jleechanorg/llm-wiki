---
title: "test_avatar_api_unit.py"
type: source
tags: [test, avatar, api, image-validation]
date: 2026-04-14
source_file: raw/mvp_site_all/test_avatar_api_unit.py
---

## Summary
Layer 1 unit tests for avatar API logic. Covers content type validation, magic byte extension detection, GCS blob management, URL validation, static asset presence, and avatar download functionality.

## Key Claims
- AVATAR_CONTENT_TYPES whitelist: only jpeg, png, gif, webp allowed
- Magic byte detection works for jpeg, png, gif87a, gif89a, webp formats
- Rejects unsupported content types (bmp, svg)
- Upload campaign avatar validates and builds correct blob path
- Delete campaign avatar cleans up matching blobs
- URL validation checks for null, empty, whitespace, type, and length
- Default Arion avatar file exists and is reasonable size (>10KB)
- Cache buster (?v=) included in default avatar URL

## Key Quotes
> "Layer 1 unit tests for avatar API logic"

## Connections
- [[AvatarAPI]] — avatar upload/download/delete functions
- [[MagicByteDetection]] — image format detection
- [[AvatarStorage]] — GCS blob management

## Contradictions
- None identified in this test file