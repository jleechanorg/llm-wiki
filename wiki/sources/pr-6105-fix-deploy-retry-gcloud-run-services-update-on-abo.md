---
title: "PR #6105: fix(deploy): retry gcloud run services update on ABORTED version conflict"
type: source
tags: []
date: 2026-04-05
source_file: raw/prs-worldarchitect-ai/pr-6105.md
sources: []
last_updated: 2026-04-05
---

## Summary
The dev deployment workflow fails with a version conflict race condition (ABORTED error) in `update_service_timeout()`. Also fixes stale `rewards_pending` flag on level-up modal exit (Goal 2).

## Metadata
- **PR**: #6105
- **Merged**: 2026-04-05
- **Author**: jleechan2015
- **Stats**: +144/-2 in 4 files
- **Labels**: none

## Connections
