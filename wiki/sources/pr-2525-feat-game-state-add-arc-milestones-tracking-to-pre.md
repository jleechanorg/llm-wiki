---
title: "PR #2525: feat(game-state): Add arc_milestones tracking to prevent timeline confusion"
type: source
tags: []
date: 2025-12-24
source_file: raw/prs-worldarchitect-ai/pr-2525.md
sources: []
last_updated: 2025-12-24
---

## Summary
- Adds `arc_milestones` field to `custom_campaign_state` for structured tracking of narrative arc completion
- Implements immutable completion states - once an arc is "completed", it cannot regress to "in_progress"
- Provides `get_completed_arcs_summary()` for including deterministic state info in LLM context

## Metadata
- **PR**: #2525
- **Merged**: 2025-12-24
- **Author**: jleechan2015
- **Stats**: +1150/-2 in 7 files
- **Labels**: none

## Connections
