# REWARDS_STATE_ERROR Auto-Correction Production Bug

**Type**: Production Bug  
**Severity**: Medium  
**Component**: RewardsAgent / State Management  
**Discovered**: 2026-01-21 (PR #3903 E2E testing)

## Problem

The LLM generates rewards (XP, loot, rewards_box) but doesn't reliably set `combat_state.rewards_processed=true`. The system detects this state inconsistency and injects auto-corrections:

```
SYSTEM CORRECTION QUEUED: REWARDS_STATE_ERROR: Combat ended (phase=ended) 
with summary, but rewards_processed=False. You MUST set 
combat_state.rewards_processed=true.
```

## Evidence

**Location**: `/tmp/worldarchitect.ai/test/organic-rewards-e2e/rewards_agent_refactored/iteration_005/artifacts/server.log:2036`

**Sequence**:
1. **Sequence 7**: Combat ends, LLM generates rewards_box with 50 XP
2. **Bug**: LLM doesn't set `rewards_processed=true` in state_updates
3. **Detection**: Server detects discrepancy (combat_phase="ended" + combat_summary exists + rewards_processed=False)
4. **Band-Aid**: System queues REWARDS_STATE_ERROR and injects into Sequence 8
5. **Fix**: LLM in Sequence 8 sets rewards_processed=true

## Impact

- ✅ Rewards still work (users get XP/loot)
- ❌ System relies on auto-correction band-aids
- ❌ Cannot claim "clean organic rewards" without caveats
- ⚠️ Extra LLM call needed to fix state inconsistency

## Root Cause Analysis Needed

Investigate:
1. **RewardsAgent prompts**: Does the prompt clearly instruct setting rewards_processed=true?
2. **State update validation**: Is there schema enforcement for rewards flow?
3. **LLM reliability**: Does the LLM consistently follow state update instructions?

## Potential Fixes

**Option 1**: Strengthen RewardsAgent prompts with explicit instruction
**Option 2**: Add server-side auto-set (when XP changes + combat_phase=ended → set rewards_processed=true)
**Option 3**: Make rewards_processed optional and infer from combat_summary presence

## Test Coverage

E2E test in `testing_mcp/test_rewards_agent_real_e2e.py` now validates:
- ✅ Organic combat flow (no pre-narration)
- ✅ Single XP award (no double-counting)
- ✅ rewards_box presence
- ⚠️ Exposes this auto-correction issue

**Related PR**: #3903  
**Evidence Bundle**: `iteration_005`
