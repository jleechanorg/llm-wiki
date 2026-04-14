# Phase 2 Recommendations: Context Management for Longer Campaigns

**Date**: 2026-01-12  
**Based on**: Iteration 005 analysis showing LLM drift over 15+ scenes

---

## Problem Statement

**Prompt fixes (Phase 1) are working** for early scenes (1-15), but **LLM drift** still occurs over longer sequences:

- ✅ Scenes 1-15: Timestamp progression correct, level progression incremental
- ⚠️ Scene 24→25: Level jump (2→5) despite prompt rules
- ⚠️ Gold tracking: Character gold vs faction gold confusion persists

**Root Cause**: LLM loses context over longer sequences (15+ scenes), even with improved prompts.

---

## Phase 2 Solution: Context Management

### 1. State Summary Injection (Every 5 Scenes)

**Goal**: Refresh LLM memory with current state checkpoint

**Implementation**:
```python
def inject_state_checkpoint(game_state: GameState, scene_number: int) -> str:
    """Inject state checkpoint every 5 scenes."""
    if scene_number > 0 and scene_number % 5 == 0:
        faction = game_state.faction_minigame or {}
        resources = faction.get("resources", {})
        
        return f"""
[STATE CHECKPOINT - Scene {scene_number}]
Current timestamp: {game_state.world_time.formatted()}
Current faction gold: {resources.get('gold', 0)}gp
Current character gold: {game_state.character.gold}gp
Current level: {game_state.character.level} {game_state.character.class_type}
Current turn: {faction.get('turn_number', 1)}

Use this checkpoint to maintain consistency in subsequent scenes.
"""
    return ""
```

**Files**: `mvp_site/world_logic.py` or `mvp_site/agents.py`

---

### 2. Recent State History (Last 3 Scenes)

**Goal**: Show LLM recent state transitions to prevent drift

**Implementation**:
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

**Files**: `mvp_site/world_logic.py`

---

### 3. Progressive Context Refresh (Scene-Based)

**Goal**: Refresh context at key milestones (every 5 scenes)

**Implementation**:
- Scene 5: First checkpoint
- Scene 10: Mid-campaign checkpoint
- Scene 15: Late-campaign checkpoint
- Scene 20: Final checkpoint

**Files**: `mvp_site/world_logic.py`

---

## Implementation Priority

### High Priority (Addresses Level Jump)
1. **State Summary Injection** - Prevents level jump by refreshing memory
2. **Recent State History** - Shows LLM recent progression

### Medium Priority (Addresses Gold Confusion)
3. **Dual Gold Clarification in Context** - Reinforce which gold pool to use
4. **State Checkpoint Format** - Explicitly show both gold pools

### Low Priority (Polish)
5. **Progressive Context Refresh** - Optimize checkpoint timing
6. **State Validation** - Server-side bounds checking (last resort)

---

## Expected Impact

**Before Phase 2**:
- ✅ Scenes 1-15: Coherent
- ⚠️ Scenes 16-25: Drift occurs (level jumps, gold confusion)

**After Phase 2**:
- ✅ Scenes 1-15: Coherent (unchanged)
- ✅ Scenes 16-25: Coherent (context refresh prevents drift)

---

## Testing Strategy

1. **Run 20-turn test** after Phase 2 implementation
2. **Compare** Scene 24→25 level progression (should be incremental)
3. **Verify** gold tracking consistency throughout
4. **Measure** improvement: % of scenes with coherence issues

---

## Files to Modify

1. `mvp_site/world_logic.py` - Add context injection functions
2. `mvp_site/agents.py` - Integrate context injection into prompt building
3. `mvp_site/prompts/faction_minigame_instruction.md` - Document context refresh behavior

---

**Related Documents**:
- `docs/llm_state_management_plan.md` - Full Phase 2-4 plan
- `docs/iteration_005_final_analysis.md` - Detailed findings
- `docs/20turn_test_comparison.md` - Before/after comparison
