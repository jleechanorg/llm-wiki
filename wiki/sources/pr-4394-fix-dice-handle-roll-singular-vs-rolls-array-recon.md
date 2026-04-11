---
title: "PR #4394: fix(dice): handle roll singular vs rolls array + reconciliation with stdout"
type: source
tags: []
date: 2026-02-01
source_file: raw/prs-worldarchitect-ai/pr-4394.md
sources: []
last_updated: 2026-02-01
---

## Summary
Fixes dice roll extraction bugs where:
1. LLM uses inconsistent stdout schema (`"roll": 15` singular instead of `"rolls": [15]` array)
2. LLM incorrectly puts total in `rolls` field instead of raw die value
3. NDJSON parsing fails when stdout contains multiple JSON objects on separate lines

**Test Results: 11/12 pass (92%)** - One known limitation with Qwen model (no code_execution support).

## Metadata
- **PR**: #4394
- **Merged**: 2026-02-01
- **Author**: jleechan2015
- **Stats**: +867/-107 in 10 files
- **Labels**: none

## Connections
