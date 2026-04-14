# Iteration 007 Campaign Analysis

**Test Run:** 20-turn E2E test (iteration 007)  
**Campaign ID:** `Gq4eDsBuWbHefnut1Qo8`  
**Date:** 2026-01-13  
**Status:** ✅ All 25 turns passed, but critical economic/ranking issues identified

## Summary

Iteration 007 shows **major improvements** over previous versions:
- ✅ Resource change logs are consistent and transparent
- ✅ FP calculation transparency (formula breakdown shown)
- ✅ Failed actions correctly blocked (spy checks, persuasion rolls)
- ✅ Economic collapse properly modeled (upkeep system works)

However, **critical design flaws** remain that make the game unplayable:
- 🔴 **Catastrophic economic failure** - upkeep 10x too high (instant bankruptcy)
- 🔴 **Ranking system broken** - stuck at #201 despite 11,923 FP
- 🟡 **FP formula imbalance** - territory disproportionately valuable
- 🟡 **Missing guardrails** - no warnings before bankruptcy

## Critical Issues (Priority 1)

### 1. Catastrophic Economic Failure
**Bead:** `worktree_world_faction-6qd`

**Problem:**
- Upkeep: **32,760gp** for 4,673 soldiers = **~7gp per soldier/week**
- Income: Only **590gp per turn** (from 20,000 citizens)
- Result: Treasury goes from +1,680gp to **-30,490gp** in one turn

**Root Cause:**
- Upkeep formula is **10x too high** compared to D&D 5e RAW
- Tax income is **50x too low** (0.02gp per citizen vs expected 1-2gp)

**Fix Required:**
- Reduce upkeep to **0.5-1gp per soldier/week** (conscript/regular pay)
- OR increase tax income to **1-2gp per citizen/week** (10,000-20,000gp from 20k citizens)

**Impact:** Game becomes unplayable after Turn 1 - instant bankruptcy with no recovery path.

---

### 2. Ranking System Broken
**Bead:** `worktree_world_faction-h2p`

**Problem:**
- Player accumulates **11,923 FP** through:
  - 4,673 soldiers (4,673 FP)
  - 525 territory (5,250 FP)
  - 2 fortifications (2,000 FP)
- Remains stuck at **Rank #201/201** (dead last)

**Root Cause:**
- Either ranking threshold is absurdly high (requires 50k+ FP to escape last place)
- OR ranking calculation doesn't update properly
- OR ranking system is not functional

**Fix Required:**
- Verify ranking calculation logic
- Adjust thresholds so player can advance from #201 with 10k+ FP
- OR explicitly state "Rank is unforgiving - most factions are extremely powerful"

**Impact:** No progression feedback - players feel stuck despite major achievements.

---

## Major Issues (Priority 2)

### 3. FP Formula Imbalance
**Bead:** `worktree_world_faction-pub`

**Problem:**
- Territory: **10 FP per acre** (525 acres = 5,250 FP)
- Soldiers: **1 FP per unit** (4,673 soldiers = 4,673 FP)
- Result: 25-acre gain (+250 FP) nearly offsets losing 262 soldiers (-262 FP)

**Impact:** Makes land grabbing more valuable than maintaining armies, contradicting "build an army" gameplay loop.

**Fix:** Rebalance formula - reduce territory FP or increase soldier FP.

---

### 4. Missing Upkeep Warnings
**Bead:** `worktree_world_faction-g3o`

**Problem:**
- Player builds structures leaving only 500gp
- Next turn: -32,760gp upkeep hits with no warning
- No guardrails prevent bankruptcy

**Fix:** Add prompt instruction to warn when treasury will go negative after next turn's upkeep.

---

### 5. Troop Accounting Inconsistencies
**Bead:** `worktree_world_faction-dgz`

**Problem:**
- Scene 25: "You have 5,000 total personnel"
- Status display: Shows only 4,673 soldiers
- Guards/militia not tracked separately

**Fix:** Either show all unit types separately OR consolidate into one "soldiers" metric.

---

### 6. Missing Construction Cost Menu
**Bead:** `worktree_world_faction-qpp`

**Problem:**
- Costs discovered during play (farms: 1,000gp, shadow network: 1,500gp)
- No upfront pricing table for planning

**Fix:** Add cost table to prompts showing all building/recruitment prices upfront.

---

### 7. Shadow Network Not Recruiting Spies
**Bead:** `worktree_world_faction-2aa`

**Problem:**
- Shadow Network built (Scene 23)
- Spy count remains 0
- No recruitment phase or capacity increase

**Fix:** On build completion, add spy recruitment capacity and prompt for recruitment action.

---

### 8. Turn Action Budget Not Enforced
**Bead:** `worktree_world_faction-63f`

**Problem:**
- Turn 1 contains 10 actions (farms, training, workshops, mana font, library, fortifications, wards, shadow network, skirmish, assault)
- Should span multiple turns

**Fix:** Enforce 3-5 strategic action points per turn OR queue builds over multiple turns.

---

## Improvements Over Previous Versions

### ✅ Fixed Issues
1. **Resource change logs** - Consistent `[RESOURCE CHANGE LOG]` blocks
2. **FP transparency** - Formula breakdown shown (Scene 25)
3. **Failed actions** - Correctly blocked (spy checks, persuasion rolls)
4. **Economic modeling** - Upkeep system properly implemented (just needs rebalancing)
5. **Narrative consistency** - No entity hallucination (Scene 20 issue fixed)
6. **State tracking** - Soldier counts consistent (4,935 - 262 = 4,673)

### 📊 Test Results
- **Total turns:** 25
- **Successful:** 25/25 ✅
- **Failed:** 0
- **Faction headers:** 22/25
- **Tutorial detected:** 21 turns
- **Tools used:** `faction_calculate_power`, `faction_calculate_ranking`

---

## Recommended Fixes (Priority Order)

### Phase 1: Critical Economic Fixes (This PR)
1. **Rebalance upkeep formula** - Reduce to 0.5-1gp per soldier/week
2. **Increase tax income** - 1-2gp per citizen/week
3. **Add upkeep warnings** - Prompt instruction to warn before bankruptcy

### Phase 2: Ranking & Progression (Follow-up PR)
4. **Fix ranking calculation** - Verify thresholds and update logic
5. **Rebalance FP formula** - Reduce territory FP or increase soldier FP
6. **Add construction cost menu** - Publish all prices upfront

### Phase 3: Gameplay Polish (Future PR)
7. **Enforce turn action budget** - Limit actions per turn
8. **Fix spy recruitment** - Auto-capacity on shadow network build
9. **Clarify troop accounting** - Separate unit types or consolidate

---

## Beads Created

All 8 issues tracked in `.beads/`:
- `worktree_world_faction-6qd` - Economic failure (Priority 1)
- `worktree_world_faction-h2p` - Ranking broken (Priority 1)
- `worktree_world_faction-pub` - FP imbalance (Priority 2)
- `worktree_world_faction-g3o` - Missing warnings (Priority 2)
- `worktree_world_faction-dgz` - Troop accounting (Priority 2)
- `worktree_world_faction-qpp` - Missing cost menu (Priority 2)
- `worktree_world_faction-2aa` - Spy recruitment (Priority 2)
- `worktree_world_faction-63f` - Action budget (Priority 2)

---

## Conclusion

**Rating:** Logic: **A-** / Economy: **F**

The system logic is solid (narrative consistency, state tracking, failed action handling), but the **economy settings need immediate patching** or the game becomes unplayable after Turn 1.

**Next Steps:**
1. Fix economic balance (upkeep + income)
2. Fix ranking system
3. Add guardrails (warnings, cost menu)
4. Rebalance FP formula
