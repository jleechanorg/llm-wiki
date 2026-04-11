---
title: "PR #5584: Schema Prompt Drift Fixes + Field Constants Generation"
type: source
tags: []
date: 2026-02-21
source_file: raw/prs-worldarchitect-ai/pr-5584.md
sources: []
last_updated: 2026-02-21
---

## Summary
This PR now includes the follow-up fixes for schema evidence consistency and test collection stability:

- `testing_mcp/schema/test_schema_enforcement_journey_real_api.py`
  - `errors` now represent **blocking** failures only.
  - Non-blocking findings are recorded under `warnings`.
- `testing_mcp/lib/schema_test_base.py`
  - Canonical-check warning aggregation aligned with scenario metrics.
  - Added canonical-check metrics block and source breakdown.
- `testing_mcp/test_evidence_utils_unit.py`

## Metadata
- **PR**: #5584
- **Merged**: 2026-02-21
- **Author**: jleechan2015
- **Stats**: +5069/-1024 in 66 files
- **Labels**: none

## Connections
