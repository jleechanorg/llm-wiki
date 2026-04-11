---
title: "PR #5810: fix: redirect orchestration worktrees to /tmp to prevent disk bloat"
type: source
tags: []
date: 2026-03-02
source_file: raw/prs-worldarchitect-ai/pr-5810.md
sources: []
last_updated: 2026-03-02
---

## Summary
- Orchestration harness worktrees were accumulating in `~/projects/orch_{repo_name}/` — found 274 dirs totaling ~70 GB during disk cleanup
- Changed `_get_worktree_base_path()` default from `~/projects/` to `/tmp/orch_worktrees/` since these are ephemeral pair-programming worktrees
- Added `ORCHESTRATION_WORKTREE_BASE` env var override for cases where persistence is needed
- Included detailed disk breakdown doc from 2026-03-01 cleanup session (recovered 194 GB total)

## Metadata
- **PR**: #5810
- **Merged**: 2026-03-02
- **Author**: jleechan2015
- **Stats**: +641/-2 in 4 files
- **Labels**: none

## Connections
