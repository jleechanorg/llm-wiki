---
title: "PR #5723: fix(ui,contracts): treat planning confidence as mechanics-only"
type: source
tags: []
date: 2026-02-24
source_file: raw/prs-worldarchitect-ai/pr-5723.md
sources: []
last_updated: 2026-02-24
---

## Summary
- Treats `planning_block.choice.confidence` as mechanics-only in the planning UI and protocol, while keeping all behavior in sync between prompt docs, frontend parsing/rendering, and tests.
- Removes the obsolete `fix-comment-e2e-claude.md` marker file.
- Fixes literal `\\n` escape sequences in `docs/automation/fix-comment-e2e-claude-20260222-112327.md` and `docs/automation/fix-comment-e2e-minimax-20260222-112327.md` headers.

## Metadata
- **PR**: #5723
- **Merged**: 2026-02-24
- **Author**: jleechan2015
- **Stats**: +39/-43 in 6 files
- **Labels**: none

## Connections
