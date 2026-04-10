---
title: "Storage Bucket Fallback"
type: concept
tags: [storage, firebase, gcs, fallback]
sources: []
last_updated: 2026-04-08
---

Storage bucket fallback is a resilience pattern in WorldArchitect.AI that handles Firebase Storage URL format conversion.

## How It Works

1. **Priority Order**:
   - First: `AVATAR_STORAGE_BUCKET` env var (explicit override)
   - Second: `FIREBASE_STORAGE_BUCKET` env var
   - Third: Hardcoded default `worldarchitecture-ai-frontend-static`

2. **URL Format Conversion**:
   - Input: `project-id.firebasestorage.app`
   - Output: `project-id.appspot.com` (working bucket)
   - Special case: `worldarchitecture-ai.firebasestorage.app` → `worldarchitecture-ai-frontend-static` (project-preserving fallback)

3. **Passthrough**: Normal bucket names (non-.firebasestorage.app) pass through unchanged

## Why This Matters

Firebase sometimes returns `.firebasestorage.app` URLs which don't work for direct GCS access. The fallback ensures avatars remain accessible by converting to the working bucket format.

## Connections
- [[Firebase]] — Source of the .firebasestorage.app URL format
- [[Avatar API]] — Consumer of bucket configuration
- [[Environment Variable Configuration]] — How bucket is configured
