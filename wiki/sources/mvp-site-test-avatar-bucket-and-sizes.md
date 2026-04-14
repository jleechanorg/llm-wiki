---
title: "test_avatar_bucket_and_sizes.py"
type: source
tags: [test, avatar, storage, bucket, css]
date: 2026-04-14
source_file: raw/mvp_site_all/test_avatar_bucket_and_sizes.py
---

## Summary
TDD tests for avatar storage bucket fallback and CSS pip sizes. Tests bucket resolution logic and validates CSS for avatar display.

## Key Claims
- .firebasestorage.app URLs convert to hardcoded worldarchitecture-ai-frontend-static bucket
- AVATAR_STORAGE_BUCKET env var takes priority over FIREBASE_STORAGE_BUCKET
- Normal GCS bucket names pass through unchanged
- Default bucket when no env vars set is worldarchitecture-ai-frontend-static
- Desktop avatar pip size: 176px width and height
- Mobile avatar pip size: 88px (50% of desktop)

## Key Quotes
> "TDD tests for avatar storage bucket fallback and CSS pip sizes"

## Connections
- [[AvatarStorage]] — bucket resolution logic
- [[AvatarCSS]] — avatar display sizing

## Contradictions
- None identified in this test file