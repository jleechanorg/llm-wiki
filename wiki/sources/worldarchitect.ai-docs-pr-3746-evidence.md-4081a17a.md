---
title: "PR #3746: Session Header Fix - Before/After Evidence"
type: source
tags: [session-header, dnd-game-state, bug-fix, worldarchitect, validation]
sources: []
date: 2026-04-07
source_file: docs/pr_memory_mvp_description.md
last_updated: 2026-04-07
---

## Summary
Production campaign analysis revealed 27% empty session headers, 10% wrong format, and resources confusion. PR #3746 implemented server-side fallback generation and standardized resource display format, achieving 100% test pass rate (0/3 → 3/3).

## Key Claims
- **Problem**: 27% empty session headers, 10% wrong format (dict-as-string or missing prefix), resources confusion ("0/1" meaning "0 used" vs "0 available")
- **Before Fix**: LLM completely omitted `session_header` field - 0/3 tests passing
- **After Initial Fix**: Server-side fallback generation + normalization - 2/3 tests passing
- **After Final Fix**: 100% passing (3/3 strong passes) with proper CURRENT/MAX format

## Key Improvements

### 1. Empty Header → Fallback Generation
When LLM omits `session_header`, `generate_session_header_fallback()` creates header from `game_state`:
```
[SESSION_HEADER]
Timestamp: 1492 DR, Hammer 1, 08:00
Location: Roadside Outside Phandalin
Status: Lvl 1 Fighter | HP: 12/12 | XP: 0/300 | Gold: 10gp
Conditions: None | Exhaustion: 0 | Inspiration: No
Resources: HD: 1/1 | Second Wind: 1/1
```

### 2. Resources Format Clarity
Changed from confusing "used/max" to clear "current/max":
- **Before**: `HD: 0/1` meant "0 used of 1 max" (confusing)
- **After**: `HD: 0/1` means "0 available of 1 max" (clear)

## Connections
- [[PR #2778 Code Review Issues Summary]] — related coherence work on session header validation
- [[PR: Behavioral Compliance MVP]] — broader behavioral automation context

## Contradictions
- None identified - this PR builds on and extends the validation improvements from earlier PRs