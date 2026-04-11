---
title: "Avatar API Layer 1 Unit Tests"
type: source
tags: [python, testing, unittest, avatar, gcs, image-processing]
source_file: "raw/avatar-api-layer-1-unit-tests.md"
sources: []
last_updated: 2026-04-08
---

## Summary
Python unit test suite for avatar API logic in WorldArchitect.AI. Tests cover upload validation, magic-byte extension detection for image types, GCS blob management, URL validation, static asset presence, and avatar download functionality including error propagation.

## Key Claims
- **AVATAR_CONTENT_TYPES Whitelist**: Only image/jpeg, image/png, image/gif, and image/webp are allowed; SVG and BMP are explicitly rejected
- **Magic Byte Detection**: _detect_image_extension function identifies image types by their magic bytes (JPEG: `\xff\xd8\xff`, PNG: `\x89PNG`, GIF: `GIF87a`/`GIF89a`, WEBP: `RIFF....WEBP`)
- **Upload Validation**: upload_campaign_avatar rejects unsupported content types with ValueError
- **Content Type to Extension Mapping**: Validates jpeg→.jpeg, png→.png, gif→.gif, webp→.webp mappings

## Test Classes
- **TestAvatarContentTypes**: Validates AVATAR_CONTENT_TYPES whitelist
- **TestDetectImageExtension**: Tests magic byte detection for various image formats
- **TestUploadCampaignAvatar**: Tests upload validation and blob path handling

## Connections
- [[Firebase]] — used for Firestore client in test stubs
- [[GoogleCloudStorage]] — GCS blob management for avatar uploads
- [[MagicByteDetection]] — technique for identifying file types by header bytes

## Contradictions
- None identified
