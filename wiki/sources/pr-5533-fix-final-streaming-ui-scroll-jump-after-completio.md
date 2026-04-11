---
title: "PR #5533: Fix final streaming UI scroll jump after completion"
type: source
tags: []
date: 2026-02-16
source_file: raw/prs-worldarchitect-ai/pr-5533.md
sources: []
last_updated: 2026-02-16
---

## Summary
**Primary fix:** God Mode streaming completion now renders correctly.

On `origin/main`, God Mode streaming can finish with an empty `full_narrative`, so the frontend completes the stream and renders blank text even when `structured_response.god_mode_response` is populated.

This PR fixes that by:
- Emitting `done.display_text` server-side (falls back to `structured_response.god_mode_response` when narrative is empty)
- Teaching the streaming client/frontend completion path to prefer `display_te

## Metadata
- **PR**: #5533
- **Merged**: 2026-02-16
- **Author**: jleechan2015
- **Stats**: +2400/-101 in 20 files
- **Labels**: none

## Connections
