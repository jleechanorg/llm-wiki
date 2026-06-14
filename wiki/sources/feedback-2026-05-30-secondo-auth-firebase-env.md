---
title: "Feedback 2026-05-30 Secondo Auth Firebase Env"
type: source
tags: [feedback, project, worldarchitect-ai, memory-file]
date: 2026-05-30
source_file: raw/memory_backfill_2026_06_13/feedback_2026-05-30_secondo_auth_firebase_env.md
---

## Summary

Root cause (2026-05-30) of the recurring AI Universe "Not authenticated" failure roughly every hour. / ran WITHOUT exporting / / . Without those, cannot SILENTLY refresh the 1-hour idToken via the long-lived refresh token → it falsely reports "Not authenticated" once the idToken expires (~hourly), even though the refresh token is still valid (no actual re-login needed).

## Key Claims

- (See raw memory file for full content)

## Key Quotes

_(No blockquotes in source)_

## Connections

- [[rebase]]
