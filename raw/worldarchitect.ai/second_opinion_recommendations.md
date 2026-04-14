# Second Opinion Analysis Recommendations

**Generated:** 2026-01-12  
**Source:** `.claude/scripts/secondo_campaign_analysis_iteration_005.md`

## Summary

Second opinion analysis from 4 AI models (Cerebras, Grok, Perplexity, GPT-5) confirms that 4 of 5 prompt fixes are effective. Remaining issues are minor and addressable.

## New Findings

### Core Issues (Address in This PR)

1. **Missing Arithmetic Narration** (Priority: High)
   - **Problem:** Scene 15 shows +124gp gain but doesn't explain the source
   - **Recommendation:** Add explicit math equations before narrative for all resource changes
   - **Example:** `Gold (Faction): 200 − deployment cost (0?) + loot (+124) + tax tick (+0) = 324`
   - **Impact:** Addresses core coherence gap identified by all models
   - **Effort:** Prompt-only change, low risk

2. **Delta Log in Status Blocks** (Priority: High)
   - **Problem:** Resource changes lack transparent audit trail
   - **Recommendation:** Add "Delta Log" section in status blocks showing all resource changes
   - **Example:** `+124gp from skirmish: 200 base + 124 spoils`
   - **Impact:** Makes arithmetic transparent and prevents reconciliation errors
   - **Effort:** Prompt-only change, complements arithmetic narration

### Nice-to-Have Improvements (Defer to Later)

3. **Standardize Dice Notation** (Priority: Medium)
   - **Current:** `1d20 +1 INT = 20 +1 INT = 21`
   - **Recommended:** `Construction Oversight (INT): 1d20 (20) +1 = 21 vs DC 12 — Critical Success`
   - **Impact:** Formatting improvement, not blocking coherence
   - **Effort:** Prompt change, can be done in follow-up PR

4. **Clarify Unit Semantics** (Priority: Medium)
   - **Recommendation:** Make unit semantics explicit in visible legend
   - **Example:** `Block = 10 soldiers; Equip new block = 100 gp; Deploying existing block = 0 gp`
   - **Impact:** Documentation improvement, prevents reader assumptions
   - **Effort:** Prompt documentation, can be done in follow-up PR

5. **Separate Campaign Turn from In-world Time** (Priority: Medium)
   - **Problem:** Both Scenes 14 and 15 claim "Turn 1" causing confusion
   - **Recommendation:** Separate "Campaign Turn" counter from in-world clock
   - **Example:** `Turn 1 — Phases A/B` or omit "Turn" from narrative scenes
   - **Impact:** Clarity improvement, may affect existing tests
   - **Effort:** Prompt restructuring, better as separate PR

### Infrastructure/Testing (Defer to Later)

6. **Automated Validators** (Priority: High, but infrastructure)
   - **Recommendation:** Add automated validators for:
     - Timestamp monotonicity (Harptos month ordering)
     - XP threshold checks (5e table)
     - Resource equation balance (sum of deltas = displayed total)
     - Scene-to-scene consistency
   - **Impact:** Ensures future 25/25 passes remain stable
   - **Effort:** Infrastructure work, requires test framework changes, separate PR

7. **Verify Full 20-Turn Log** (Priority: Medium)
   - **Problem:** Sample only covers Scenes 14-15; earlier issues were in Scenes 18-22
   - **Recommendation:** Create script to parse all "Timestamp:" lines and verify monotonic increase
   - **Impact:** Verification task, can be done post-merge
   - **Effort:** Testing/verification, separate PR or follow-up

## Recommendation: This PR vs Later

### ✅ THIS PR (Prompt-Only, High Value)

Focus on items **1-2** (arithmetic narration + delta log):
- Address core coherence gaps identified by second opinion
- Prompt-only changes, no infrastructure risk
- Low risk, high impact
- Complements existing 5 prompt fixes

### ⏸️ DEFER TO LATER

Items **3-7**:
- Formatting/documentation improvements (items 3-4)
- Clarity improvements that may affect tests (item 5)
- Infrastructure/testing work (items 6-7)
- Can be done in follow-up PRs without blocking coherence

## Consensus Across Models

All 4 models agreed:
- ✅ Prompt fixes significantly improved coherence
- ✅ Remaining issues are edge cases, not breaking problems
- ✅ System is ready for user-facing campaigns with minor refinements
- ⚠️ Core gap: Missing explicit arithmetic narration for resource changes

## Next Steps

1. **This PR:** Implement items 1-2 (arithmetic narration + delta log)
2. **Follow-up PRs:** Address items 3-7 as separate improvements
3. **Testing:** Verify full 20-turn log post-merge
