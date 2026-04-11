---
title: "PR #105: [agento] feat(tracker-beads): inject bead context into AO worker prompts (bd-ggf)"
type: source
tags: []
date: 2026-03-22
source_file: raw/prs-worldai_claw/pr-105.md
sources: []
last_updated: 2026-03-22
---

## Summary
AO workers spawned with bead IDs (bd-xxx) received only `Work on issue: bd-xxx` with zero task context. There was no tracker plugin for beads — only GitHub, Linear, and GitLab trackers existed. This caused workers (ao-415, ao-417) to think for hours or produce nothing because they literally did not know what to build.

## Metadata
- **PR**: #105
- **Merged**: 2026-03-22
- **Author**: jleechan2015
- **Stats**: +499/-45 in 7 files
- **Labels**: none

## Connections
