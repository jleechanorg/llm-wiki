# Easy vs Hard Fixes: PR #2778 Coherence Issues

## Categorization: What Can We Fix in This PR vs Defer?

---

## ✅ EASY FIXES (Can Do in This PR)

**Criteria**: Low risk, high impact, quick to implement, prompt-only changes

### 1. **Dual Gold Tracking Clarification** ⭐ EASIEST
**Issue**: Scene 18 gold error - LLM confusing character.gold vs faction.resources.gold

**Fix**: Add explicit clarification to faction prompts
- **File**: `mvp_site/prompts/faction_minigame_instruction.md`
- **Change**: Add section explaining dual gold pools
- **Time**: 15 minutes
- **Risk**: Very low (just clarification)

**Implementation**:
```markdown
## 💰 Gold Tracking (Faction Mode)

**CRITICAL**: Faction mode has TWO separate gold pools:

1. **Character Gold** (`character.gold`): Personal wealth
   - Used for: Equipment, personal expenses, individual purchases
   - Shown in: Character status block
   - Example: "Gold: 110gp" in character status

2. **Faction Gold** (`faction.resources.gold`): Faction treasury
   - Used for: Buildings, recruitment, faction expenses
   - Shown in: Faction header (`💰 Gold: X`)
   - Example: "💰 Gold: 500" in faction header

**When building/recruiting**: Use FACTION gold, not character gold.
**When buying equipment**: Use CHARACTER gold, not faction gold.

**Always specify which gold pool** when showing calculations.
```

### 2. **Tutorial Completion Clarification** ⭐ EASY
**Issue**: Tutorial completion appears mid-campaign, confusing users

**Fix**: Clarify tutorial phase vs campaign
- **File**: `mvp_site/prompts/faction_minigame_instruction.md`
- **Change**: Add clarification about tutorial phase completion
- **Time**: 10 minutes
- **Risk**: Very low

**Implementation**:
```markdown
## 📚 Tutorial Completion

**IMPORTANT**: "Tutorial complete" means "tutorial PHASE complete", NOT "campaign complete".

When tutorial is completed:
1. Show message: "[TUTORIAL PHASE COMPLETE - Campaign continues]"
2. Continue campaign narrative normally
3. Do NOT end the campaign
4. Full faction management gameplay continues

The tutorial is just the onboarding phase. The campaign continues indefinitely.
```

### 3. **Level Progression Clarification** ⭐ EASY
**Issue**: Character jumps Level 1→3 without showing Level 2

**Fix**: Add explicit incremental progression instruction
- **File**: `mvp_site/prompts/faction_minigame_instruction.md` or `mvp_site/prompts/game_state_instruction.md`
- **Change**: Add level progression rules
- **Time**: 10 minutes
- **Risk**: Very low

**Implementation**:
```markdown
## 📈 Level Progression Rules

**CRITICAL**: Always show level progression incrementally.

**CORRECT**:
- "Level 1 Fighter (XP: 0/300)"
- "Level up! Level 2 Fighter (XP: 300/900)"
- "Level up again! Level 3 Fighter (XP: 1125/2700)"

**WRONG**:
- "Level 1 Fighter" → "Level 3 Fighter" (skipping Level 2)

**Rule**: If character gains enough XP for multiple levels, show each level-up separately.
```

### 4. **Timestamp Progression Rules** ⭐ EASY
**Issue**: Timestamp jumps and reversals

**Fix**: Add explicit timestamp rules
- **File**: `mvp_site/prompts/faction_minigame_instruction.md`
- **Change**: Add timestamp progression rules
- **Time**: 15 minutes
- **Risk**: Low

**Implementation**:
```markdown
## ⏰ Timestamp Progression Rules

**CRITICAL**: Timestamps MUST always advance forward.

**Rules**:
- Small actions (build, recruit): +5-15 minutes
- Combat actions: +30-60 minutes
- End turn: +7 days (advance to next week)
- **NEVER go backwards in time**

**Example**:
- Previous: `1492 DR, Alturiak 1, 08:05`
- Action: Build library (takes ~10 minutes)
- New: `1492 DR, Alturiak 1, 08:15` ✅

**If large time gap needed** (e.g., 2+ hours), add narrative explanation:
- "Several hours later, as the sun sets..."
- "The next morning..."
```

### 5. **Gold Calculation Examples** ⭐ EASY
**Issue**: Gold calculation errors (Scene 18, Scene 21)

**Fix**: Add explicit calculation examples
- **File**: `mvp_site/prompts/faction_minigame_instruction.md`
- **Change**: Add gold calculation examples
- **Time**: 10 minutes
- **Risk**: Very low

**Implementation**:
```markdown
## 💰 Gold Calculation Examples

**Before generating narrative, calculate gold explicitly:**

**Example 1: Building**
```
Previous faction gold: 110gp
Action: Build library (cost: 100gp)
Calculation: 110 - 100 = 10gp
New faction gold: 10gp
```

**Example 2: Combat Rewards**
```
Previous faction gold: 110gp
Action: Skirmish victory (spoils: 100gp)
Calculation: 110 + 100 = 210gp
New faction gold: 210gp
```

**Always show calculation before narrative.**
```

---

## ⚠️ HARD FIXES (Defer to Follow-Up PRs)

**Criteria**: High risk, requires infrastructure, needs extensive testing

### 1. **Context Management Infrastructure** 🔴 HARD
**Issue**: LLM drift over long sequences

**Why Hard**:
- Requires code changes in `mvp_site/world_logic.py`
- Needs state history tracking system
- Requires testing to ensure it doesn't break existing flows
- Complex integration with existing prompt building

**Defer To**: Follow-up PR focused on context management

### 2. **Structured Output Schema** 🔴 HARD
**Issue**: Need to enforce structured state updates

**Why Hard**:
- Requires schema definition and validation
- Needs response parsing changes
- Requires LLM to adopt new format (may need retraining/iterations)
- High risk of breaking existing responses

**Defer To**: Follow-up PR focused on structured output

### 3. **Progressive Context Refresh** 🟡 MEDIUM-HARD
**Issue**: Need to refresh LLM memory every 5 scenes

**Why Hard**:
- Requires scene counting infrastructure
- Needs integration with prompt building
- Requires testing to ensure refresh doesn't break narrative flow
- Medium complexity

**Defer To**: Follow-up PR or Phase 2 of fix plan

### 4. **Chain-of-Thought State Tracking** 🟡 MEDIUM-HARD
**Issue**: Need LLM to show calculations before narrative

**Why Hard**:
- Requires prompt format changes
- LLM may not consistently follow format
- Needs validation that format is followed
- Medium risk

**Defer To**: Follow-up PR or Phase 2 of fix plan

### 5. **Server-Side Validation** 🟡 MEDIUM-HARD
**Issue**: Need bounds checking and retry logic

**Why Hard**:
- Requires code changes in `mvp_site/world_logic.py`
- Needs retry logic implementation
- Requires testing to ensure retries don't cause loops
- Medium complexity

**Defer To**: Phase 4 of fix plan (last resort)

---

## Implementation Plan for This PR

### Quick Wins (Can Do Now)

1. **Add Dual Gold Clarification** (15 min)
   - File: `mvp_site/prompts/faction_minigame_instruction.md`
   - Add section explaining character.gold vs faction.resources.gold
   - Impact: HIGH (fixes Scene 18 error)

2. **Add Tutorial Completion Clarification** (10 min)
   - File: `mvp_site/prompts/faction_minigame_instruction.md`
   - Clarify tutorial phase vs campaign
   - Impact: MEDIUM (improves UX)

3. **Add Level Progression Rules** (10 min)
   - File: `mvp_site/prompts/faction_minigame_instruction.md` or `game_state_instruction.md`
   - Add incremental progression requirement
   - Impact: MEDIUM (fixes level skip issue)

4. **Add Timestamp Rules** (15 min)
   - File: `mvp_site/prompts/faction_minigame_instruction.md`
   - Add forward-only progression rules
   - Impact: HIGH (fixes timestamp reversals)

5. **Add Gold Calculation Examples** (10 min)
   - File: `mvp_site/prompts/faction_minigame_instruction.md`
   - Add explicit calculation examples
   - Impact: MEDIUM (helps prevent errors)

**Total Time**: ~60 minutes
**Total Impact**: Addresses 4 out of 5 major issues with prompt-only changes
**Risk**: Very low (just adding clarifications)

---

## Deferred to Follow-Up PRs

### Follow-Up PR #1: Context Management
- State summary injection
- Recent state history
- Progressive context refresh
- Action-to-state mapping

### Follow-Up PR #2: Structured Output
- State update schema
- Structured output format requirements
- Response parsing updates

### Follow-Up PR #3: Server-Side Safeguards (If Needed)
- Bounds checking
- Retry logic
- Intervention logging

---

## Success Criteria for This PR

**Easy Fixes Complete**:
- [ ] Dual gold clarification added
- [ ] Tutorial completion clarification added
- [ ] Level progression rules added
- [ ] Timestamp rules added
- [ ] Gold calculation examples added

**Testing**:
- [ ] Run 5-turn test (should still pass)
- [ ] Run tutorial test (should still pass)
- [ ] Document expected improvements (20-turn test will validate in follow-up)

**Documentation**:
- [ ] Plan documents committed (`llm_state_management_plan.md`, `pr_impact_analysis.md`, `easy_vs_hard_fixes.md`)
- [ ] Beads issues created and linked
- [ ] Follow-up PRs documented

---

**Created**: 2026-01-12  
**Related PR**: #2778  
**Related Beads**: worktree_world_faction-4xh, worktree_world_faction-a64, worktree_world_faction-kdg, worktree_world_faction-1xw, worktree_world_faction-o74, worktree_world_faction-c63
