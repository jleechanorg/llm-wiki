---
title: "PR #6063: [agento] feat(avatar): add download avatar image functionality"
type: source
tags: []
date: 2026-03-30
source_file: raw/prs-worldarchitect-ai/pr-6063.md
sources: []
last_updated: 2026-03-30
---

## Summary
- Adds `GET /api/avatar` endpoint to download authenticated user's avatar image as attachment
- Adds `GET /api/campaign/<campaign_id>/avatar` endpoint for campaign avatars
- Probes GCS for existing avatar extension (jpeg/png/gif/webp) before download
- Returns `Content-Disposition: attachment` with correct extension
- Includes extension-probing helpers in `firestore_service.py`

## Metadata
- **PR**: #6063
- **Merged**: 2026-03-30
- **Author**: jleechan2015
- **Stats**: +226/-38 in 5 files
- **Labels**: none

## Connections
