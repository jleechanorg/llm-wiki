---
title: "PR #2598: fix(prompts): Clarify XP threshold table to prevent level confusion"
type: source
tags: []
date: 2025-12-27
source_file: raw/prs-worldarchitect-ai/pr-2598.md
sources: []
last_updated: 2025-12-27
---

## Summary
Fixes the root cause of LLM level-up inconsistency where the AI was quoting wrong XP thresholds.

### Root Cause Analysis

**Evidence:** `docs/debugging/Alexiel Assiah V2 (2).txt` lines 1395-1408

The LLM was misreading the XP table:
- User asked: "How much XP for level 8?" (status showed `XP: 33,025/34,000`)
- LLM responded: "To reach the eighth tier...you require 48,000 XP" ❌
- Correct answer: 34,000 XP (48,000 is for level 9)

**Why this happened:**
The table header said "Total XP Required" w

## Metadata
- **PR**: #2598
- **Merged**: 2025-12-27
- **Author**: jleechan2015
- **Stats**: +863/-32 in 5 files
- **Labels**: none

## Connections
