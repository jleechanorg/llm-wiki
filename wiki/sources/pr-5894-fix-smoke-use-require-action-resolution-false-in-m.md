---
title: "PR #5894: fix(smoke): use require_action_resolution=False in mock mode for dice roll"
type: source
tags: []
date: 2026-03-09
source_file: raw/prs-worldarchitect-ai/pr-5894.md
sources: []
last_updated: 2026-03-09
---

## Summary
- Fix `testing_mcp/test_smoke.py` SCENARIO 4 (Dice Roll Action) failure in Mock APIs smoke run
- In mock mode, `quality_issues` was computed with `require_action_resolution=True` even though the mock LLM is not a real gameplay path and may not return `action_resolution` on the preview server
- Split quality check by mode: mock uses relaxed checks, real mode keeps strict `require_action_resolution=True` + `require_rng_when_code_execution_used=True`
- Improve failure message to print actual `quali

## Metadata
- **PR**: #5894
- **Merged**: 2026-03-09
- **Author**: jleechan2015
- **Stats**: +20/-8 in 1 files
- **Labels**: none

## Connections
