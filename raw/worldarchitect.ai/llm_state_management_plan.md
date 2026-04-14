# LLM-First State Management Plan
**PR #2778 Campaign Coherence Fixes**

## Core Principle
**Let LLM manage state through better instructions, context, and structured output. Server-side fixes only for critical safety.**

---

## Scope Analysis: Normal vs Faction Campaigns

### Does This Affect Normal Campaigns or Just Faction Management?

**Answer: BOTH - but faction campaigns expose issues more readily.**

**TL;DR**: 
- ✅ **Normal campaigns**: Same LLM path, same potential issues (timestamp, gold, level coherence)
- ✅ **Faction campaigns**: Additional complexity (dual gold tracking, turn numbers, tutorial) makes issues more visible
- ✅ **Solution**: LLM improvements benefit both, but faction needs extra clarity about dual gold tracking

#### Shared LLM Path (Both Campaigns)
- ✅ **Same LLM service** (`llm_service.py`)
- ✅ **Same narrative generation** (`world_logic.py`)
- ✅ **Same state management** (GameState, world_time, character stats)
- ✅ **Same timestamp tracking** (world_time progression)
- ✅ **Same character gold tracking** (character.gold)
- ✅ **Same level progression** (character.level, character.xp)

**Normal Campaigns** use the exact same LLM narrative generation path as faction campaigns. The coherence issues (timestamp inconsistencies, gold errors, level gaps) would affect **both** campaign types because they stem from the same LLM narrative generation logic.

#### Why Faction Campaigns Expose Issues More
1. **Longer sequences**: 20-turn test generates 25+ scenes (normal campaigns might be shorter)
2. **More complex state**: Dual gold tracking (character.gold + faction.resources.gold)
3. **Additional state variables**: Turn numbers, rankings, tutorial progress
4. **Structured testing**: 20-turn E2E test specifically designed to catch long-term drift

#### Faction-Specific Complexity
- **Dual Gold Tracking**: 
  - `character.gold` (personal wealth)
  - `faction.resources.gold` (faction treasury)
  - LLM might confuse these (Scene 18 gold error might be this!)
- **Turn Number Tracking**: Strategic turns vs narrative scenes
- **Tutorial Progress**: Multi-phase tutorial with completion detection

#### Normal Campaign State
- Character gold (`character.gold`)
- Character level (`character.level`)
- Character XP (`character.xp`)
- World time (`world_time`)
- Location, HP, conditions, exhaustion

**Conclusion**: LLM state management improvements will benefit **BOTH** normal and faction campaigns. Faction campaigns are more likely to expose issues due to longer sequences and more complex state, but normal campaigns would have the same underlying coherence problems over long sequences.

---

## Problem Summary

Campaign coherence issues found in 20-turn E2E test:
1. **Timestamp inconsistencies**: Scene 14→15 jumps 08:05→10:45, Scene 20→21 reverses 11:15→10:45
2. **Gold calculation errors**: Scene 18 shows 110gp (should be 10gp), Scene 21 discrepancy
3. **Level progression gaps**: Character jumps Level 1→3 without showing Level 2
4. **Tutorial completion timing**: Appears mid-campaign (Scene 15) but gameplay continues

**Root Cause**: LLM drift over long sequences (15+ scenes). 5-turn test didn't catch because issues appear after Scene 14.

---

## Implementation Strategy

### Priority 1: Prompt Engineering (Primary Fix)
**Goal**: Address root cause through better LLM instructions

**Scope**: Benefits BOTH normal and faction campaigns

#### 1.1 Add State Coherence Requirements to Prompts
**Files**: 
- `mvp_site/prompts/faction_minigame_instruction.md` (faction-specific)
- `mvp_site/prompts/game_master_instruction.md` or similar (normal campaigns)

Add new section:
```markdown
## 🎯 State Coherence Requirements

### Timestamp Tracking Rules
- **Always advance time logically** from previous timestamp
- Small actions (build, recruit): +5-15 minutes
- Combat actions: +30-60 minutes
- End turn: +7 days (advance to next week)
- **NEVER go backwards in time**
- If previous was `08:05`, next must be `>= 08:05`

**Example**:
```
Previous timestamp: 1492 DR, Alturiak 1, 08:05
Current action: Build library (takes ~10 minutes)
New timestamp: 1492 DR, Alturiak 1, 08:15
```

### Gold Calculation Rules
- **Always calculate**: Previous Gold - Costs + Rewards = New Gold
- **Show calculation before narrative**
- **Faction Mode**: Track BOTH character.gold (personal) AND faction.resources.gold (faction treasury) separately
- Building costs: Farms (100gp), Libraries (100gp), Training Grounds (100gp), etc.
- Combat rewards: Vary by battle outcome (typically 200-800gp)

**Normal Campaign Example**:
```
Previous character gold: 110gp
Action: Buy equipment (cost: 100gp)
Calculation: 110 - 100 = 10gp
New character gold: 10gp
```

**Faction Campaign Example**:
```
Previous character gold: 110gp (personal wealth)
Previous faction gold: 500gp (faction treasury)
Action: Build library (cost: 100gp from faction treasury)
Character gold calculation: 110 - 0 = 110gp (unchanged)
Faction gold calculation: 500 - 100 = 400gp
New character gold: 110gp
New faction gold: 400gp
```

### Level Progression Rules
- **Show progression incrementally**: Level 1 → Level 2 → Level 3
- **Never skip levels** (no 1 → 3 jumps)
- Include XP tracking: "Level 2 (XP: 300/900)"
- Show level-up message **before** applying level

**Example**:
```
Current: Level 1 Fighter (XP: 0/300)
After combat: XP gained = 1125
Check: 1125 >= 300? Yes → Level up to 2
Check: 1125 >= 900? Yes → Level up to 3
Final: Level 3 Fighter (XP: 1125/2700)
```

### Tutorial Completion Clarification
- "Tutorial complete" means **"tutorial phase complete"**
- Campaign continues normally after tutorial completion
- Do NOT end campaign narrative after tutorial message
- Continue with full faction management gameplay

**Format**:
```
[TUTORIAL PHASE COMPLETE - Campaign continues]
[Continue narrative normally with faction management]
```
```

#### 1.2 Add Chain-of-Thought State Tracking
**File**: `mvp_site/prompts/faction_minigame_instruction.md`

Add requirement:
```markdown
## 📊 State Update Format

Before generating narrative, you MUST show state calculations:

```
[STATE CALCULATION]
Previous timestamp: [INJECT FROM STATE]
Previous gold: [INJECT FROM STATE]
Previous level: [INJECT FROM STATE]
Action: [ACTION TYPE]
Cost: [COST IF APPLICABLE]
Reward: [REWARD IF APPLICABLE]

Timestamp calculation: [SHOW REASONING]
Gold calculation: [SHOW MATH]
Level check: [SHOW XP THRESHOLD CHECK]

New timestamp: [RESULT]
New gold: [RESULT]
New level: [RESULT]

[NARRATIVE]
[Generated story here using calculated state]
```
```

#### 1.3 Add Self-Validation Checklist
**File**: `mvp_site/prompts/faction_minigame_instruction.md`

Add requirement:
```markdown
## ✅ State Coherence Checklist

Before finalizing your response, verify:
- [ ] Timestamp advances logically (>= previous timestamp)
- [ ] Gold calculation matches (previous - costs + rewards)
- [ ] Level progression is incremental (no skips)
- [ ] Tutorial completion doesn't end campaign
- [ ] All state values are consistent with calculations

If any check fails, recalculate and regenerate.
```

---

### Priority 2: Context Management (Secondary Fix)
**Goal**: Prevent LLM drift over long sequences

#### 2.1 State Summary Injection
**File**: `mvp_site/agents.py` or `mvp_site/world_logic.py`

Before each LLM call, inject state summary:
```python
def inject_state_summary(game_state: GameState) -> str:
    """Inject current state summary into prompt context."""
    faction = game_state.faction_minigame or {}
    resources = faction.get("resources", {})
    
    return f"""
[CURRENT STATE SUMMARY]
- Timestamp: {game_state.world_time.formatted()}
- Gold: {resources.get('gold', 0)}gp
- Level: {game_state.character.level} {game_state.character.class_type}
- XP: {game_state.character.xp}/{xp_needed_for_level(game_state.character.level + 1)}
- Faction Turn: {faction.get('turn_number', 1)}
- Last Action: [INJECT FROM PREVIOUS ACTION]
"""
```

#### 2.2 Recent State History
**File**: `mvp_site/world_logic.py`

Include last 3 state transitions:
```python
def inject_state_history(story_entries: list, num_scenes: int = 3) -> str:
    """Inject recent state history to prevent drift."""
    recent = story_entries[-num_scenes:] if len(story_entries) >= num_scenes else story_entries
    
    history = []
    for entry in recent:
        timestamp = entry.get("world_time", {}).get("formatted", "?")
        gold = entry.get("faction_header", "").split("💰 Gold: ")[1].split(" ")[0] if "💰 Gold:" in entry.get("faction_header", "") else "?"
        level = entry.get("character", {}).get("level", "?")
        history.append(f"Scene {len(history)+1}: Gold {gold}gp, Level {level}, Time {timestamp}")
    
    return f"""
[RECENT STATE HISTORY]
{chr(10).join(history)}
"""
```

#### 2.3 Progressive Context Refresh
**File**: `mvp_site/world_logic.py`

After every 5 scenes, inject state checkpoint:
```python
def should_refresh_context(scene_number: int) -> bool:
    """Check if we should inject state checkpoint."""
    return scene_number > 0 and scene_number % 5 == 0

def inject_state_checkpoint(game_state: GameState, scene_number: int) -> str:
    """Inject state checkpoint to refresh LLM memory."""
    return f"""
[STATE CHECKPOINT - Scene {scene_number}]
Current timestamp: {game_state.world_time.formatted()}
Current gold: {game_state.faction_minigame.resources.gold}gp
Current level: {game_state.character.level} {game_state.character.class_type}
Current turn: {game_state.faction_minigame.turn_number}

Use this checkpoint to maintain consistency in subsequent scenes.
"""
```

#### 2.4 Action-to-State Mapping Rules
**File**: `mvp_site/prompts/faction_minigame_instruction.md`

Add explicit mapping:
```markdown
## 🔄 Action State Change Rules

| Action Type | Timestamp Change | Gold Change | Level Change | Turn Change |
|-------------|------------------|-------------|--------------|-------------|
| Build | +5-15 min | -building_cost | None | None |
| Recruit | +5-15 min | -recruitment_cost | None | None |
| Combat | +30-60 min | +spoils (varies) | +XP (may level up) | None |
| Intel | +10-20 min | -intel_cost | None | None |
| End Turn | +7 days | +taxes | None | +1 |

**Always calculate state changes explicitly before narrative.**
```

---

### Priority 3: Structured Output (Tertiary Fix)
**Goal**: Enforce consistency through format requirements

#### 3.1 Define State Update Schema
**File**: `mvp_site/narrative_response_schema.py` (or create new)

Add schema for state updates:
```python
STATE_UPDATE_SCHEMA = {
    "type": "object",
    "properties": {
        "state_updates": {
            "type": "object",
            "properties": {
                "timestamp": {"type": "string", "description": "New timestamp (must be >= previous)"},
                "gold": {"type": "integer", "description": "New gold amount (calculated)"},
                "level": {"type": "integer", "description": "New level (incremental only)"},
                "xp": {"type": "integer", "description": "New XP amount"},
                "turn_number": {"type": "integer", "description": "Faction turn number"},
                "reasoning": {"type": "string", "description": "Explanation of state changes"}
            },
            "required": ["timestamp", "gold", "level", "reasoning"]
        },
        "narrative": {
            "type": "string",
            "description": "Story narrative using calculated state"
        }
    },
    "required": ["state_updates", "narrative"]
}
```

#### 3.2 Require Structured Output in Prompts
**File**: `mvp_site/prompts/faction_minigame_instruction.md`

Add requirement:
```markdown
## 📋 Response Format Requirement

Your response MUST include both state updates and narrative:

```json
{
  "state_updates": {
    "timestamp": "[calculated timestamp]",
    "gold": [calculated gold],
    "level": [calculated level],
    "reasoning": "[explanation of calculations]"
  },
  "narrative": "[story text using state values]"
}
```

The narrative MUST use the exact state values from state_updates.
```

---

### Priority 4: Minimal Server-Side Safeguards (Last Resort)
**Goal**: Safety only, not state management

#### 4.1 Bounds Checking
**File**: `mvp_site/world_logic.py`

Add minimal validation:
```python
def validate_state_bounds(state_updates: dict) -> tuple[bool, list[str]]:
    """Validate state updates are within safe bounds. Returns (is_valid, errors)."""
    errors = []
    
    # Gold bounds
    gold = state_updates.get("gold", 0)
    if gold < 0:
        errors.append(f"Gold cannot be negative: {gold}")
    
    # Level bounds
    level = state_updates.get("level", 1)
    if level < 1 or level > 20:
        errors.append(f"Level out of bounds: {level}")
    
    # Timestamp validation (basic)
    timestamp = state_updates.get("timestamp", "")
    if not timestamp or len(timestamp) < 10:
        errors.append(f"Invalid timestamp format: {timestamp}")
    
    return len(errors) == 0, errors
```

#### 4.2 Retry Logic with Stronger Instructions
**File**: `mvp_site/world_logic.py`

If validation fails, retry with enhanced instructions:
```python
def retry_with_enhanced_instructions(original_prompt: str, validation_errors: list[str]) -> str:
    """Add validation error feedback to prompt for retry."""
    error_feedback = "\n".join([f"- {error}" for error in validation_errors])
    
    return f"""
{original_prompt}

[VALIDATION ERRORS DETECTED - PLEASE CORRECT]
{error_feedback}

Please recalculate state values and regenerate response with corrected values.
"""
```

**Retry Policy**: Max 2 retries before accepting (to avoid infinite loops)

#### 4.3 Logging for Analysis
**File**: `mvp_site/world_logic.py`

Log when server-side intervention occurs:
```python
if not is_valid:
    logging_util.warning(
        f"⚠️ State validation failed: {errors}. "
        f"Retrying with enhanced instructions (attempt {retry_count + 1}/2)"
    )
    
    # Track for analysis
    track_intervention({
        "campaign_id": campaign_id,
        "scene_number": scene_number,
        "errors": errors,
        "retry_count": retry_count
    })
```

---

## Implementation Phases

### Phase 1: Prompt Engineering (Week 1)
- [ ] Add State Coherence Requirements section to `faction_minigame_instruction.md` (faction campaigns)
- [ ] Add State Coherence Requirements to normal campaign prompts (normal campaigns)
- [ ] Add Chain-of-Thought State Tracking format (both)
- [ ] Add Self-Validation Checklist (both)
- [ ] Clarify dual gold tracking for faction mode (faction-specific)
- [ ] Test with 20-turn E2E test (faction)
- [ ] Test with normal campaign (10-15 turn test if available)
- [ ] Measure improvement (target: 50%+ issue resolution)

### Phase 2: Context Management (Week 1-2)
- [ ] Implement State Summary Injection
- [ ] Implement Recent State History (last 3 scenes)
- [ ] Implement Progressive Context Refresh (every 5 scenes)
- [ ] Add Action-to-State Mapping Rules
- [ ] Test with 20-turn E2E test
- [ ] Measure improvement (target: 80%+ issue resolution)

### Phase 3: Structured Output (Week 2)
- [ ] Define State Update Schema
- [ ] Require Structured Output in prompts
- [ ] Update response parsing to extract state_updates
- [ ] Test with 20-turn E2E test
- [ ] Measure improvement (target: 90%+ issue resolution)

### Phase 4: Minimal Server Safeguards (Week 2-3)
- [ ] Implement bounds checking (gold >= 0, level 1-20, valid timestamp)
- [ ] Implement retry logic (max 2 retries)
- [ ] Add intervention logging
- [ ] Test with 20-turn E2E test
- [ ] Measure improvement (target: 95%+ issue resolution)

---

## Success Metrics

### Timestamp Coherence
- ✅ 100% forward progression (no reversals)
- ✅ Large gaps (>1 hour) include narrative explanation
- ✅ End turn advances time by 7 days

### Gold Accuracy
- ✅ 100% match between calculation and narrative
- ✅ Building costs properly deducted
- ✅ Combat rewards properly added

### Level Progression
- ✅ 100% incremental (no skips)
- ✅ Level-up messages appear before level change
- ✅ XP tracking visible in narrative

### Tutorial Clarity
- ✅ Clear phase distinction (tutorial vs campaign)
- ✅ Campaign continues after tutorial completion
- ✅ No confusion about campaign end

---

## Testing Strategy

### After Each Phase
1. Run 20-turn E2E test
2. Analyze campaign output for coherence issues
3. Measure improvement vs baseline
4. Document which issues resolved

### Success Criteria
- **Phase 1**: 50%+ of issues resolved through prompt changes
- **Phase 2**: 80%+ of issues resolved (prompt + context)
- **Phase 3**: 90%+ of issues resolved (prompt + context + structure)
- **Phase 4**: 95%+ of issues resolved (all + minimal safeguards)

### Fallback Plan
If LLM-first approach doesn't achieve 80%+ resolution after Phase 2:
- Re-evaluate prompt engineering approach
- Consider hybrid approach (LLM + light server validation)
- Document lessons learned

---

## Files to Modify

### Prompt Files
- `mvp_site/prompts/faction_minigame_instruction.md` - Add state coherence requirements
- `mvp_site/prompts/faction_management_instruction.md` - Add state tracking rules

### Code Files
- `mvp_site/agents.py` - Add state summary injection
- `mvp_site/world_logic.py` - Add context management, minimal validation
- `mvp_site/narrative_response_schema.py` - Add state update schema (or create new)

### Test Files
- `testing_mcp/faction/test_faction_20_turns_e2e.py` - Use for validation (faction campaigns)
- Normal campaign tests (if available) - Use for validation (normal campaigns)

---

## Principles

### ✅ DO (LLM-First)
- Provide clear, explicit instructions
- Include state context in prompts
- Use chain-of-thought reasoning
- Require structured output formats
- Refresh context periodically

### ❌ DON'T (Avoid Heavy Server-Side)
- Pre-calculate state and inject as "correct" values
- Override LLM state updates with server calculations
- Add complex validation layers that reject LLM output
- Strip LLM autonomy by making it "fill in templates"
- Add server-side state reconciliation layers

### ⚠️ LAST RESORT (Server-Side Only)
- Bounds checking (gold >= 0, level 1-20)
- Critical safety validation (prevent data corruption)
- Retry logic (max 2 retries with enhanced instructions)
- Logging for analysis (track when intervention needed)

---

## Expected Outcomes

### Best Case
- 95%+ of coherence issues resolved through LLM improvements alone
- Server-side intervention needed <5% of the time
- Campaign narratives maintain consistency over 20+ turns (faction) and 10+ turns (normal)
- Both normal and faction campaigns benefit equally

### Realistic Case
- 80-90% of coherence issues resolved through LLM improvements
- Server-side intervention needed 10-20% of the time
- Campaign narratives mostly consistent with occasional corrections
- Faction campaigns show more improvement (due to explicit dual gold tracking fixes)
- Normal campaigns show improvement but less dramatic (simpler state)

### Worst Case
- <50% of coherence issues resolved through LLM improvements
- Server-side intervention needed frequently
- Need to re-evaluate approach (hybrid or server-first)
- May need faction-specific server-side validation for dual gold tracking

---

## Next Steps

1. **Review this plan** with team/stakeholders
2. **Start Phase 1** (Prompt Engineering) - highest impact, lowest risk
   - Begin with faction campaigns (more complex, better test coverage)
   - Apply same improvements to normal campaign prompts
3. **Test incrementally** after each phase
   - Faction: Use existing 20-turn E2E test
   - Normal: Create/run 10-15 turn test if available
4. **Document results** and adjust plan based on findings
5. **Iterate** until success criteria met for both campaign types

## Key Insight: Dual Gold Tracking

**Critical Discovery**: Faction campaigns have **TWO separate gold pools**:
- `character.gold` - Personal wealth (used for equipment, personal expenses)
- `faction.resources.gold` - Faction treasury (used for buildings, recruitment, faction expenses)

The gold calculation error in Scene 18 might be the LLM confusing these two pools. The plan must explicitly clarify this distinction in faction mode prompts.

---

**Created**: 2026-01-12  
**Related PR**: #2778  
**Related Beads**: worktree_world_faction-4xh, worktree_world_faction-a64, worktree_world_faction-kdg, worktree_world_faction-1xw, worktree_world_faction-o74
