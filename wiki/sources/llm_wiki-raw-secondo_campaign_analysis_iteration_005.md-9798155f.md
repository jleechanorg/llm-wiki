---
title: "Second Opinion: Campaign Coherence Analysis (Iteration 005)"
type: source
tags: ["second-opinion", "coherence", "campaign-testing", "validation", "dnd"]
date: 2026-01-12
source_file: "raw/llm_wiki-raw-secondo_campaign_analysis_iteration_005.md"
sources: []
last_updated: 2026-04-07
---

## Summary
Analysis of a 20-turn faction campaign test across 4 models (including Cerebras - Qwen 3 Thinking) totaling 55,631 tokens at $0.1334 cost. Evaluates coherence fixes from previous iterations including timestamp progression, gold calculations, level progression, and tutorial messaging clarity.

## Key Claims

### Timestamp Progression Fix
- The "always forward" rule is now effective — previous 2h40m backward jump (09:55 → 08:05) corrected to forward progression (09:55 → 10:55)
- **Recommendation:** Run a simple script that parses every "Timestamp:" line and verifies monotonic increase across the entire 20-turn log

### Gold Calculations (Faction vs. Personal)
- Dual gold clarification working — separate "Gold: 200" (faction) and "Gold: 10gp (Personal)" now consistently displayed
- Earlier mismatches (110gp vs 10gp, 758gp vs 748gp) resolved
- **Remaining gap:** Missing explicit arithmetic narration for gold changes (e.g., "Collected 124gp from market taxes, raising treasury from 200gp to 324gp")
- **Recommendation:** Add automated sanity-check that recomputes faction treasury after every transaction

### Level Progression Fix
- Incremental only rule working — no illegal 1→3 jumps detected, level remains stable at 2 (Fighter)
- **Recommendation:** Keep XP-to-level table visible in UI so level-ups are automatically justified by displayed XP

### Tutorial Messaging Clarity
- Previous ambiguous tutorial text (implying campaign finished) appears resolved
- **Recommendation:** Verify exact banner "[TUTORIAL PHASE COMPLETE – Campaign continues]" appears exactly once before first real campaign turn

## Overall Impact Assessment

| Prompt Fix | Observed Effect |
|------------|-----------------|
| Dual gold clarification | Working — separate faction/personal gold now displayed |
| Timestamp progression rule | Working — reversal eliminated, forward progression confirmed |
| Tutorial completion clarification | Resolved — no contradictory language observed |
| Level progression rule | Working — no illegal jumps detected |
| Gold calculation examples | Partial — values present but narrative explanations missing |

## Remaining Gaps to Address

1. **Missing arithmetic narration** for gold changes
2. **Full-log timestamp verification** needed for complete validation
3. **Explicit tutorial completion banner** needs verification

## Connections
- [[Second Opinion Workflow]] — this analysis is an example of the second opinion verification process
- [[Campaign Coherence]] — broader concept of maintaining consistency across campaign turns
- [[WorldArchitect.AI]] — the platform conducting this analysis