---
title: "PR #4224: Add component-level budget allocation for LLM requests"
type: source
tags: []
date: 2026-02-02
source_file: raw/prs-worldarchitect-ai/pr-4224.md
sources: []
last_updated: 2026-02-02
---

## Summary
This PR implements intelligent token budget allocation for LLM requests with component-level compaction, ensuring story context quality while preventing any single component from consuming excessive tokens.

**Fixed 6 review comments using TDD approach:**
1. Fixed structured_response serialization (Major) - Pydantic models now properly serialize with `mode="json"`
2. Fixed campaign setting duplication (Medium) - Removed duplicate call in build_god_mode_instructions()
3. Fixed type guard on custo

## Metadata
- **PR**: #4224
- **Merged**: 2026-02-02
- **Author**: jleechan2015
- **Stats**: +6447/-136 in 33 files
- **Labels**: none

## Connections
