---
title: "PR #1810: Add smart fake code detection hook"
type: source
tags: [codex]
date: 2025-10-02
source_file: raw/prs-worldarchitect-ai/pr-1810.md
sources: []
last_updated: 2025-10-02
---

## Summary
- add a smart fake code detection hook that runs `/fake` headlessly with `claude -p --dangerously-skip-permissions --model sonnet` after each Write tool use
- document the new hook alongside existing tooling guidance
- register the hook in the project settings so it executes with other post-write safeguards

## Metadata
- **PR**: #1810
- **Merged**: 2025-10-02
- **Author**: jleechan2015
- **Stats**: +159/-0 in 3 files
- **Labels**: codex

## Connections
