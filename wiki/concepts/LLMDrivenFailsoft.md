---
title: "LLM Driven Failsoft"
type: concept
tags: [pairv2, enhancement-pattern, automation]
sources: []
last_updated: 2026-04-13
---

## Description

The LLM driven failsoft pattern treats missing user-provided files (contract files, design-doc paths) as warnings with fallback to LLM generation, not hard failures. Missing files are brittle operational issues, not evidence that implementation is invalid.

## Why It Matters

Pairv2 should not stop early because user-provided file paths are missing. Hard-failing on missing files prevents the workflow from continuing via LLM contract generation, which is a more robust approach.

## Key Technical Details

- **Pattern**: Missing user-provided files warn and fall back to LLM generation
- **Scope**: `.claude/pair/pair_execute_v2.py`
- **Key insight**: File path typos or version mismatches are operational issues, not code validity issues

## Related Beads

- BD-pairv2-llm-driven-failsoft-files
- ArtifactPathFragility (concept)
