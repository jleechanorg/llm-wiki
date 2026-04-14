# PR #2778 Code Review Issues Summary

**Review Date**: 2026-01-12  
**PR**: #2778 - Faction minigame + force creation mechanics  
**Reviewers**: CodeRabbit, Cursor Bot, Codex

---

## 🔴 CRITICAL Issues (Priority 1)

### 1. **Fix state_updates path in FACTION MODE example** ⚠️ CRITICAL
**Bead**: `worktree_world_faction-1fl`  
**File**: `mvp_site/prompts/game_state_instruction.md` lines 222-246  
**Issue**: Example uses wrong schema path - `state_updates.faction_minigame` instead of `state_updates.custom_campaign_state.faction_minigame`  
**Impact**: LLMs will emit incorrect schema structure that backend doesn't recognize  
**Fix**: Update example to use correct nested path

---

## 🟠 MAJOR Issues (Priority 2-3)

### 2. **Harden combat helper functions against non-string inputs** ⚠️ MAJOR
**Bead**: `worktree_world_faction-hta`  
**File**: `mvp_site/faction/combat.py` lines 39-90  
**Issue**: `get_position_multiplier()` and `get_school_counter_bonus()` call `.lower()` without validation  
**Impact**: Runtime AttributeError if LLM passes None/non-string values  
**Fix**: Add `isinstance()` checks, return safe defaults (1.0)

### 3. **Guard random_range and clamp damage calculation inputs** ⚠️ MAJOR
**Bead**: `worktree_world_faction-6zr`  
**File**: `mvp_site/faction/combat.py` lines 154-205  
**Issue**: 
- `random.uniform(a, b)` throws if `a > b` (no validation)
- `efficiency`, `accuracy`, `avg_resistance` not clamped to [0, 1]
- Values outside range cause damage amplification bugs  
**Impact**: Runtime errors and incorrect damage calculations  
**Fix**: Validate random_range, clamp all values to [0, 1]

### 4. **Move RAW_LIMIT_DEFAULT constant after imports** ⚠️ MAJOR (Code Org)
**Bead**: `worktree_world_faction-cci`  
**File**: `mvp_site/llm_service.py` lines 78-92  
**Issue**: Constant and function defined between imports (violates Python guidelines)  
**Impact**: Code organization violation  
**Fix**: Move after all imports complete

---

## 🟡 MEDIUM Issues (Priority 2)

### 5. **Fix inconsistent AC averaging in fast battle simulation** ⚠️ MEDIUM
**Bead**: `worktree_world_faction-uic`  
**File**: `mvp_site/faction/battle_sim.py` around line 336-344  
**Issue**: AC averaging is unweighted while HP averaging is weighted (inconsistent)  
**Impact**: Incorrect battle calculations for mixed unit types  
**Fix**: Use weighted AC average consistent with HP calculation

### 6. **Fix zero-casualty stalls in fast battle simulation** ⚠️ MEDIUM
**Bead**: `worktree_world_faction-wp9`  
**File**: `mvp_site/faction/battle_sim.py` around line 336-344  
**Issue**: When damage < 1 HP per round, casualties = 0, causing infinite loops  
**Impact**: Battle simulation stalls/hangs for low-damage engagements  
**Fix**: Accumulate fractional damage or use minimum casualty of 1

---

## 🟢 MINOR Issues (Priority 4)

### 7. **Fix priority comment numbering** ⚠️ MINOR
**Bead**: `worktree_world_faction-qur`  
**File**: `mvp_site/agents.py` line 1942  
**Issue**: Comment says "Priority 8" but should be "Priority 9"  
**Impact**: Comment accuracy only  
**Fix**: Update comment to "Priority 9"

---

## Summary

**Total Issues**: 7
- **Critical**: 1 (schema mismatch - must fix)
- **Major**: 3 (runtime errors, code org)
- **Medium**: 2 (battle calculation bugs)
- **Minor**: 1 (comment fix)

**Recommended Fix Order**:
1. **Critical**: Fix state_updates path (affects LLM training)
2. **Major**: Harden combat functions (prevents runtime errors)
3. **Major**: Guard damage calculations (prevents runtime errors)
4. **Medium**: Fix AC averaging (battle accuracy)
5. **Medium**: Fix zero-casualty stalls (prevents hangs)
6. **Major**: Move constant after imports (code org)
7. **Minor**: Fix comment numbering (cosmetic)

---

## Beads Tracking

All issues tracked in `.beads/issues.jsonl`:
- `worktree_world_faction-1fl`: Critical schema fix
- `worktree_world_faction-hta`: Combat function hardening
- `worktree_world_faction-6zr`: Damage calculation guards
- `worktree_world_faction-uic`: AC averaging fix
- `worktree_world_faction-wp9`: Zero-casualty stall fix
- `worktree_world_faction-cci`: Import organization
- `worktree_world_faction-qur`: Comment fix

---

**Created**: 2026-01-12  
**Related PR**: #2778
