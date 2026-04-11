---
title: "PR #148: [agento] feat(web): validate world ID before navigating from wizard"
type: source
tags: []
date: 2026-03-29
source_file: raw/prs-worldai_claw/pr-148.md
sources: []
last_updated: 2026-03-29
---

## Summary
Fixes a race condition / bad navigation in the `NewCampaignWizard` "Launch World" flow. When the backend API response was malformed (no `id` field), the app silently navigated to `/game/undefined` instead of surfacing an error to the user.

## Metadata
- **PR**: #148
- **Merged**: 2026-03-29
- **Author**: jleechan2015
- **Stats**: +163/-13 in 3 files
- **Labels**: none

## Connections
