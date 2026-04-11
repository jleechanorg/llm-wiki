---
title: "PR #6169: [agento] fix(test_cerebras): avoid KeyError in planning_block assertion"
type: source
tags: []
date: 2026-04-09
source_file: raw/prs-worldarchitect-ai/pr-6169.md
sources: []
last_updated: 2026-04-09
---

## Summary
- Fix KeyError risk in `test_cerebras_provider.py` by using safe `.get()` chain instead of direct dict access on `properties["planning_block"]`
- Follows issue #3462 guidance: \"avoid KeyError in assertions (assert key presence first)\"

## Metadata
- **PR**: #6169
- **Merged**: 2026-04-09
- **Author**: jleechan2015
- **Stats**: +7/-3 in 1 files
- **Labels**: none

## Connections
