---
title: "PR #6349 autor PRM XP progress tracking"
type: source
tags: [autor, prm, worldarchitect-ai]
sources: []
last_updated: 2026-04-17
---

## Summary

PR #6349 is an AI-generated autor PR using the PRM (Process Reward Model) technique to apply the XP progress tracking fix to rewards_box visibility. The autor PR receives a quality score of 87/100 — a clean, targeted fix matching the approach of original PR #6254.

## Key Claims

- XP progress tracking (current_xp + next_level_xp) should make rewards_box visible even when xp_gained=0
- The fix adds one condition to the `has_visible_content` check: `or (current_xp > 0 and next_level_xp > 0)`
- 4 new test cases cover edge cases: both fields present, only one present, zero values
- PRM step-by-step reasoning guides the implementation

## Score Breakdown

| Dimension | Score | Max | Notes |
|-----------|-------|-----|-------|
| Naming | 13 | 15 | Good test names: test_xp_gained_zero_with_progress_tracking_is_visible |
| Error Handling | 17 | 20 | Correct XP progress visibility condition; None returns preserved |
| Type Safety | 17 | 20 | Proper int comparisons; coerce_int used for XP values |
| Architecture | 17 | 20 | Minimal targeted fix: one condition added; follows existing pattern |
| Test Coverage | 14 | 15 | 4 comprehensive test cases for XP progress edge cases |
| Documentation | 9 | 10 | Docstring updated; inline comments explain the bug |
| **Total** | **87** | **100** | |

## Connections

- [[PR6254]] — original PR this autor PR mirrors (same fix, different test additions)
- [[PR6349]] — this autor PR
