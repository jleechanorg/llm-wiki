# Manual Beads Creation Guide

**Generated:** 2026-01-12  
**Source:** Evaluation feedback analysis

## Critical Issues (Priority 1)

### 1. Fix Context Hallucination - Scene 20 Intent Mismatch
- **Type:** bug
- **Priority:** 1
- **Description:** Player asks to attack "Golden Dawn" but AI responds about "Blood Ravens" from previous scene. Add intent/entity matching guardrail in prompts.
- **Labels:** critical, prompt-engineering, evaluation-feedback

### 2. Add Monotonic Counter Validation
- **Type:** bug
- **Priority:** 1
- **Description:** XP decreased from 800/900 to 550/900 in Scene 16-17. Add server-side validation enforcing monotonic counters for XP, gold, territory.
- **Labels:** critical, validation, evaluation-feedback

## Major Issues (Priority 2)

### 3. Add FP Calculation Transparency
- **Type:** feature
- **Priority:** 2
- **Description:** FP jumped from 5,750 to 12,000 with no action. Show FP components and delta breakdown in prompts.
- **Labels:** prompt-engineering, evaluation-feedback

### 4. Add Gold Ledger Block
- **Type:** feature
- **Priority:** 2
- **Description:** Gold jumped from 331 to 26,756 (+26,425) in one week. Add weekly/turn ledger block showing income sources and expenses.
- **Labels:** prompt-engineering, evaluation-feedback

### 5. Clarify Unit Categories
- **Type:** bug
- **Priority:** 2
- **Description:** Troop counts contradict - narrative says "5,000 total personnel" but status shows 4,281 soldiers. Define canonical representation for soldiers/guards/militia.
- **Labels:** prompt-engineering, evaluation-feedback

### 6. Clarify Turn Advancement Mechanics
- **Type:** feature
- **Priority:** 2
- **Description:** All Scenes 1-25 occur in Turn 1 despite major campaign. Define Turn as strategic tick and gate actions (1-3 per turn).
- **Labels:** prompt-engineering, evaluation-feedback

### 7. Fix HP and Hit Dice Tracking
- **Type:** bug
- **Priority:** 2
- **Description:** Level 5 Fighter still has 20/20 HP and HD 1/1 (should be 5 total). Track HD as spent/total, increase HP on level up.
- **Labels:** character-progression, evaluation-feedback

## Medium Priority (Priority 3)

### 8. Add Capacity Formula Explanation
- **Type:** feature
- **Priority:** 3
- **Description:** Max citizens jumps without explanation (25,000/26,150 → 25,425/33,100). Show capacity breakdown when it changes.
- **Labels:** prompt-engineering, evaluation-feedback

### 9. Add XP Pacing Caps
- **Type:** feature
- **Priority:** 3
- **Description:** Jumped from Level 2 to Level 5 in single combat (9,400 XP). Cap XP per encounter or spread across milestones.
- **Labels:** character-progression, evaluation-feedback

### 10. Rebalance Economic Income Formulas
- **Type:** feature
- **Priority:** 3
- **Description:** Economy scales from tight (24gp) to trivial (26,756gp) in one week. Rebalance income formulas and add upkeep costs.
- **Labels:** game-design, evaluation-feedback

### 11. Fix Ranking Calculation
- **Type:** feature
- **Priority:** 3
- **Description:** Rank stays #100/201 despite major victories. Rebalance ranking calculation and show movement after actions.
- **Labels:** game-design, evaluation-feedback

### 12. Improve Fail-Forward Mechanics
- **Type:** feature
- **Priority:** 3
- **Description:** Failed rolls sometimes succeed with cost, sometimes hard stop. Standardize fail-forward mechanics.
- **Labels:** game-design, evaluation-feedback

### 13. Standardize Construction Costs
- **Type:** feature
- **Priority:** 3
- **Description:** Costs inconsistent (farms 500gp/5, fortifications "at least 100gp"). Standardize cost structure in prompts.
- **Labels:** prompt-engineering, evaluation-feedback

## Usage

These beads can be created manually using the MCP beads tool or tracked in the analysis document until the MCP tool JSON parsing issue is resolved.
