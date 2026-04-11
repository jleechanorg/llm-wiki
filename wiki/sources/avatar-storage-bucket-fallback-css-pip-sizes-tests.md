---
title: "TDD Tests for Avatar Storage Bucket Fallback and CSS Pip Sizes"
type: source
tags: [python, testing, unittest, avatar, firebase, storage, css]
source_file: "raw/avatar-storage-bucket-fallback-css-pip-sizes-tests.md"
sources: []
last_updated: 2026-04-08
---

## Summary
Python unittest suite for avatar storage bucket fallback logic and CSS pip sizing in WorldArchitect.AI. Tests validate bucket URL conversion from Firebase format (.firebasestorage.app) to working GCS bucket (.appspot.com), environment variable priority, and avatar CSS pip size correctness.

## Key Claims
- **Bucket Fallback**: .firebasestorage.app URLs automatically convert to working .appspot.com bucket
- **Project-Preserving**: Fallback maintains project context when converting URL formats
- **Explicit Priority**: AVATAR_STORAGE_BUCKET env var takes precedence over FIREBASE_STORAGE_BUCKET
- **Normal Passthrough**: Standard bucket names (e.g., worldarchitecture-ai-frontend-static) pass through unchanged

## Key Code Components
- **_resolve_bucket**: Simulates bucket resolution from firestore_service.py
- **TestStorageBucketFallback**: Test class covering 5 bucket resolution scenarios
- **TestAvatarCSSPipSizes**: Validates correct pip sizing in avatar CSS

## Connections
- [[Firebase]] — GCS bucket provider with .firebasestorage.app URL format
- [[WorldArchitect.AI]] — Project using Firebase storage for avatars
- [[Avatar API]] — Storage bucket system this test validates
