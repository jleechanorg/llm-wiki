# Campaign Evaluation Feedback Analysis

**Generated:** 2026-01-12  
**Source:** Evaluation feedback from campaign log review

## Critical Issues (Fix in This PR)

### 1. Context Hallucination - Scene 20
**Severity:** CRITICAL  
**Issue:** Player asks to attack "Golden Dawn" but AI responds about "Blood Ravens" from previous scene.  
**Root Cause:** LLM ignoring current user intent, repeating previous scene content.  
**Fix:** Add intent/entity matching guardrail (bead created).  
**PR Scope:** Prompt engineering + server-side validation.

### 2. XP Monotonic Violation - Scene 16→17
**Severity:** CRITICAL  
**Issue:** XP decreased from 800/900 to 550/900.  
**Root Cause:** No server-side validation enforcing monotonic XP.  
**Fix:** Add monotonic counter validation (bead created).  
**PR Scope:** Server-side validation (minimal code change).

### 3. FP Calculation Transparency - Scene 5→6
**Severity:** CRITICAL  
**Issue:** FP jumped from 5,750 to 12,000 with no action.  
**Root Cause:** FP formula not visible to LLM, no delta breakdown.  
**Fix:** Show FP components and delta breakdown in prompts.  
**PR Scope:** Prompt engineering (add FP calculation explanation).

### 4. Gold Accounting - Scene 26 Hyper-Inflation
**Severity:** CRITICAL  
**Issue:** Gold jumped from 331 to 26,756 (+26,425) in one week.  
**Root Cause:** No weekly/turn ledger showing income/expense sources.  
**Fix:** Add ledger block showing income sources and expenses.  
**PR Scope:** Prompt engineering (complements arithmetic narration we just added).

## Major Issues (Fix in This PR if Prompt-Only)

### 5. Troop Count Contradictions - Scene 25
**Severity:** MAJOR  
**Issue:** Status shows 4,281 soldiers but narrative says "5,000 total personnel."  
**Root Cause:** No canonical representation (soldiers vs guards vs militia).  
**Fix:** Define canonical representation in prompts.  
**PR Scope:** Prompt engineering (clarify unit categories).

### 6. Turn Advancement Mechanics
**Severity:** MAJOR  
**Issue:** All Scenes 1-25 occur in Turn 1 despite major campaign.  
**Root Cause:** Turn only advances on explicit command, not gated by actions.  
**Fix:** Define Turn as strategic tick, gate actions (1-3 per turn).  
**PR Scope:** Prompt engineering (clarify turn system).

### 7. Capacity Formula Transparency
**Severity:** MAJOR  
**Issue:** Max citizens jumps without explanation (25,000/26,150 → 25,425/33,100).  
**Root Cause:** Formula not explicit, capacity changes not explained.  
**Fix:** Show capacity breakdown when it changes.  
**PR Scope:** Prompt engineering (add capacity formula explanation).

## Medium Priority (Defer to Follow-up PR)

### 8. HP/Hit Dice Tracking
**Severity:** MEDIUM  
**Issue:** Level 5 Fighter still has 20/20 HP and HD 1/1 (should be 5 total).  
**Fix:** Track HD as spent/total, increase HP on level up.  
**PR Scope:** Server-side character progression logic.

### 9. XP Pacing (Level 2→5 Jump)
**Severity:** MEDIUM  
**Issue:** Jumped from Level 2 to Level 5 in single combat (9,400 XP).  
**Fix:** Cap XP per encounter or spread across milestones.  
**PR Scope:** Server-side XP award logic.

### 10. Construction Cost Standardization
**Severity:** MEDIUM  
**Issue:** Costs inconsistent (farms 500gp/5, fortifications "at least 100gp").  
**Fix:** Standardize cost structure in prompts.  
**PR Scope:** Prompt engineering (can be done later).

## Low Priority / Design Issues (Defer)

### 11. Economic Balance (Hyper-Inflation)
**Severity:** LOW (Design)  
**Issue:** Economy scales from tight (24gp) to trivial (26,756gp) in one week.  
**Fix:** Rebalance income formulas, add upkeep costs.  
**PR Scope:** Game design rebalance (separate PR).

### 12. Ranking Stagnation
**Severity:** LOW (Design)  
**Issue:** Rank stays #100/201 despite major victories.  
**Fix:** Rebalance ranking calculation, show movement after actions.  
**PR Scope:** Game design rebalance (separate PR).

### 13. Resource Blocking Patterns
**Severity:** LOW (Design)  
**Issue:** Repeated failures create "nothing works until combat" loop.  
**Fix:** Rebalance DCs, add alternative paths, improve fail-forward mechanics.  
**PR Scope:** Game design rebalance (separate PR).

## This PR vs Later

### ✅ THIS PR (Prompt-Only + Critical Validation)

**High Priority:**
1. **Intent/Entity Matching Guardrail** - Prevent context hallucination
2. **Monotonic Counter Validation** - Server-side XP/gold/territory checks
3. **FP Calculation Transparency** - Show components and delta in prompts
4. **Gold Ledger Block** - Weekly/turn income/expense breakdown
5. **Unit Category Clarification** - Canonical representation in prompts
6. **Turn System Clarification** - Define strategic tick and action gating
7. **Capacity Formula Explanation** - Show breakdown when capacity changes

**Rationale:**
- Items 1-4 address CRITICAL bugs that break gameplay
- Items 5-7 are prompt-only clarifications that prevent future issues
- All can be done without major infrastructure changes
- Complements arithmetic narration + delta log we just added

### ⏸️ DEFER TO LATER

**Server-Side Logic:**
- HP/Hit Dice tracking (item 8)
- XP pacing caps (item 9)

**Game Design Rebalance:**
- Economic balance (item 11)
- Ranking calculation (item 12)
- Resource blocking patterns (item 13)

**Rationale:**
- Require game design decisions
- May affect existing tests
- Better as separate focused PRs

## Implementation Plan

### Phase 1: Critical Fixes (This PR)
1. Add intent/entity matching to prompts
2. Add server-side monotonic validation
3. Add FP calculation explanation to prompts
4. Add gold ledger block format to prompts
5. Clarify unit categories in prompts
6. Clarify turn system in prompts
7. Add capacity formula explanation to prompts

### Phase 2: Follow-up PRs
- Character progression fixes (HP/HD)
- Game design rebalance (economy, ranking, DCs)

## Beads Created

All critical and major issues have been tracked in `.beads/`:
- Context hallucination fix
- XP monotonic validation
- FP calculation transparency
- Troop count contradictions
- Gold accounting inconsistencies
- HP/Hit Dice tracking
- Turn advancement mechanics
- Capacity formula transparency
- Intent/entity matching guardrail
- Monotonic counter validation
