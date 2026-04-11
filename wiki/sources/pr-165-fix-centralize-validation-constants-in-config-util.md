---
title: "PR #165: fix: centralize validation constants in config utils"
type: source
tags: [codex]
date: 2025-10-04
source_file: raw/prs-/pr-165.md
sources: []
last_updated: 2025-10-04
---

## Summary
- expose client metadata validation limits through `@ai-universe/config-utils` so they can be shared without backend wrappers
- update the SecondOpinion agent to import validation limits directly from the shared package and remove the redundant backend constants file

redo of this PR https://github.com/jleechanorg/ai_universe/pull/75

## Metadata
- **PR**: #165
- **Merged**: 2025-10-04
- **Author**: jleechan2015
- **Stats**: +10/-38 in 3 files
- **Labels**: codex

## Connections
