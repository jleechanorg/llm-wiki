---
title: "PR #118: fix: Resolve Firebase Auth project ID mismatch in backend"
type: source
tags: []
date: 2025-10-01
source_file: raw/prs-/pr-118.md
sources: []
last_updated: 2025-10-01
---

## Summary
Fixes authentication error: **"Firebase ID token has incorrect aud claim"**

The backend was using the wrong Firebase project ID for authentication validation, causing all user authentication attempts to fail.

## Metadata
- **PR**: #118
- **Merged**: 2025-10-01
- **Author**: jleechan2015
- **Stats**: +8/-6 in 3 files
- **Labels**: none

## Connections
