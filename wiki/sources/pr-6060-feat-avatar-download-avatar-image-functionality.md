---
title: "PR #6060: feat(avatar): download avatar image functionality"
type: source
tags: []
date: 2026-03-30
source_file: raw/prs-worldarchitect-ai/pr-6060.md
sources: []
last_updated: 2026-03-30
---

## Summary
- Add `POST /api/avatar/download` endpoint that accepts a `url` parameter and proxies the image to Firebase Storage
- Store downloaded avatar under `avatars/{user_id}/avatar.{ext}`
- Update user settings with the new avatar_url

## Metadata
- **PR**: #6060
- **Merged**: 2026-03-30
- **Author**: jleechan2015
- **Stats**: +554/-3 in 4 files
- **Labels**: none

## Connections
