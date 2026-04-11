---
title: "20-Turn Test Improvement Summary"
type: source
tags: [testing, iteration, timestamp, level-progression, gold-tracking, prompt-fixes, context-management]
source_file: "raw/20-turn-test-improvement-summary.md"
sources: []
last_updated: 2026-04-07
---

## Summary
Iteration 004 vs Iteration 005 comparison testing 20-turn campaign behavior. Five prompt clarifications successfully fixed timestamp reversals, tutorial messaging, early level progression, and dual gold tracking. Remaining issues include later-level jumps (LLM drift over longer sequences) and gold calculation verification.

## Key Claims
- **Timestamp Progression COMPLETELY FIXED**: No reversals detected in Iteration 005, logical 5-60 minute increments
- **Tutorial Messaging FIXED**: "[TUTORIAL PHASE COMPLETE - Campaign continues]" clear format adopted
- **Early Level Progression FIXED**: Level 1→2 incremental progression working
- **Dual Gold Tracking IMPROVED**: Character gold (10gp) and faction gold tracked separately
- **Later Level Jump (2→5)**: New issue at Scene 24→25, root cause is LLM drift over 15+ scenes

## Key Measurements

| Issue | Iteration 004 | Iteration 005 | Status |
|-------|---------------|---------------|--------|
| Timestamp Reversals | Scene 20→21 (11:15→10:45) | None | ✅ FIXED |
| Timestamp Jumps | Scene 14→15 (2h40m gap) | Logical progression | ✅ FIXED |
| Tutorial Messaging | Confusing | "[TUTORIAL PHASE COMPLETE]" | ✅ FIXED |
| Level 1→3 Jump | Yes | No (1→2 incremental) | ✅ FIXED |
| Level 2→5 Jump | N/A | Yes (Scene 24→25) | ⚠️ NEW ISSUE |
| Dual Gold Tracking | Confused | Working (separate pools) | ✅ IMPROVED |

## Phase Recommendations
- ✅ **Phase 1 (Prompt Fixes)**: Complete and working
- ⏭️ **Phase 2 (Context Management)**: Recommended for longer campaigns (15+ scenes)
- ⏭️ **Phase 3 (Structured Output)**: Consider if Phase 2 doesn't fully resolve drift
- ⏭️ **Phase 4 (Server Safeguards)**: Last resort only

## Connections
- [[TimestampProgression]] — fixed via prompt clarifications
- [[LevelProgression]] — early progression fixed, later drift remains
- [[GoldTracking]] — dual gold system working correctly
- [[ContextManagement]] — Phase 2 recommended for longer sequences

## Contradictions
- None detected with existing wiki content
