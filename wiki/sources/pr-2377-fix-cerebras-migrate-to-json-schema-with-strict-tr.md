---
title: "PR #2377: fix(cerebras): migrate to json_schema with strict:true for structured outputs"
type: source
tags: []
date: 2025-12-10
source_file: raw/prs-worldarchitect-ai/pr-2377.md
sources: []
last_updated: 2025-12-10
---

## Summary
- Migrates Cerebras API from legacy `json_object` mode to `json_schema` with `strict:true`
- Fixes planning block generation failures caused by schema echo bug
- Adds schema echo detection and nested JSON wrapper unwrapping

## Metadata
- **PR**: #2377
- **Merged**: 2025-12-10
- **Author**: jleechan2015
- **Stats**: +447/-59 in 17 files
- **Labels**: none

## Connections
