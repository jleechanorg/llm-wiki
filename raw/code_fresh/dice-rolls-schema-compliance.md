# dice_rolls Schema Compliance Issue

**Status**: Open
**Date**: 2026-01-22
**Priority**: Medium
**Type**: LLM Content Generation

## Problem Statement

LLM sometimes omits the `dice_rolls` field during combat actions, causing server warnings. This indicates incomplete schema compliance in responses.

**Evidence**: test_rewards_agent_real_e2e.py server logs show:
```
⚠️ LLM_MISSING_FIELDS: Response missing ['dice_rolls']
SYSTEM WARNING: Missing required fields: dice_rolls
```

Frequency: 5+ occurrences in combat_win_organic scenario (multiple combat rounds)

## Root Cause

Unlike `rewards_processed` (administrative flag), `dice_rolls` is **LLM-generated content** representing what the LLM "imagined" happened during combat actions (attacks, damage rolls, skill checks).

**Why LLM Omits It**:
1. Narrative generation prioritized over structured fields
2. Field is technically optional in schema (no enforcement)
3. Multiple combat fields compete for LLM attention (action_resolution, combat_state updates, etc.)
4. Long responses may "forget" to include all fields

## Severity Assessment

**Impact**: Medium
- Server computes dice rolls anyway (game logic doesn't depend on LLM providing them)
- User experience unaffected (combat still functions)
- Audit trail incomplete (missing roll details for transparency)
- Test validation can flag this as quality issue

**Not Blocking**: Combat works without dice_rolls field, unlike missing rewards_box which makes rewards invisible.

## Current State

**Schema Definition**: `mvp_site/narrative_response_schema.py`
```python
dice_rolls: list[str] | None = None  # Optional field
```

**Server Behavior**:
- Logs warning when missing
- Accepts response anyway (no retry)
- Computes rolls server-side if needed

## Proposed Solutions

### Option A: JSON Schema Enforcement (High Effort)

Make `dice_rolls` a required field in combat responses.

**Changes Required**:
1. Update `narrative_response_schema.py` to make field required
2. Add validation that rejects responses without dice_rolls
3. Implement retry logic for rejected responses
4. Risk of infinite retry loops if LLM can't comply

**Pros**: Guaranteed compliance
**Cons**:
- High complexity (schema validation + retry logic)
- May break existing functionality
- LLM may still fail to provide correct format

### Option B: Prompt Engineering (Medium Effort)

Strengthen instructions to emphasize dice_rolls importance.

**Changes to combat_system_instruction.md**:
```markdown
## MANDATORY: dice_rolls Field

For EVERY combat action (attacks, skill checks, saves), you MUST include dice_rolls.

**Format**:
{
  "dice_rolls": [
    "Attack roll: d20+7 = 19 (hit)",
    "Damage roll: 2d6+3 = 11 slashing"
  ]
}

**CRITICAL**: Without dice_rolls, the combat audit trail is incomplete.
Players cannot see what you rolled, reducing transparency and trust.

**When to include**:
- Every attack (yours or enemy)
- Every saving throw
- Every skill check in combat
- Every damage roll

**Example for missed attack**:
{
  "dice_rolls": [
    "Goblin attack: d20+4 = 7 (miss)"
  ]
}
```

**Add to ESSENTIALS section** (top of prompt):
```markdown
- 🚨 MANDATORY: Include dice_rolls for ALL combat actions
- 🚨 dice_rolls = audit trail for player transparency
```

**Pros**:
- Simple to implement
- No risk to existing functionality
- Addresses root cause (LLM forgets)

**Cons**:
- No guarantee of 100% compliance
- Still relies on LLM following instructions

### Option C: Hybrid Validation (Recommended)

Combine prompt strengthening with soft validation.

**Implementation**:
1. Update combat_system_instruction.md per Option B
2. Add server-side check that warns more prominently when missing
3. Track compliance rate in logs for monitoring
4. DON'T reject responses (keep current behavior)

**Additional Monitoring**:
```python
# In structured_fields_utils.py or similar
if mode == MODE_COMBAT and not structured_fields.get("dice_rolls"):
    logging_util.warning(
        "🎲 DICE_ROLLS_MISSING: LLM omitted dice_rolls in combat response. "
        "This reduces transparency. Check combat_system_instruction.md compliance."
    )
    # Track metric for monitoring
    metrics.increment("llm.dice_rolls.missing")
```

**Pros**:
- Improves compliance without breaking functionality
- Provides data on compliance rates
- Can iterate on prompt if compliance stays low

**Cons**:
- Not guaranteed 100% compliance

### Option D: Post-Processing Synthesis (Fallback)

Server generates synthetic dice_rolls when LLM omits them.

**Example**:
```python
def synthesize_dice_rolls(action_resolution: dict) -> list[str]:
    """Generate synthetic dice_rolls from action_resolution for audit trail."""
    if not action_resolution:
        return []

    rolls = []
    if "attack" in action_resolution:
        attack = action_resolution["attack"]
        rolls.append(f"Attack roll: d20 = {attack.get('roll', '?')} ({attack.get('outcome', '?')})")

    if "damage" in action_resolution:
        damage = action_resolution["damage"]
        rolls.append(f"Damage: {damage.get('amount', '?')} {damage.get('type', '')}")

    return rolls
```

**Pros**:
- Guarantees audit trail completeness
- No dependency on LLM compliance

**Cons**:
- Synthetic data lacks LLM's narrative flavor
- Maintenance burden (keep synthesis logic updated)

## Comparison to rewards_processed

| Aspect | rewards_processed | dice_rolls |
|--------|-------------------|------------|
| **Type** | Administrative flag | Content generation |
| **Owner** | Server (per Option D) | LLM |
| **Required for** | Preventing duplicate rewards | Audit trail transparency |
| **Impact if missing** | Critical (duplicate rewards) | Low (combat works anyway) |
| **Solution** | Server auto-set | Prompt engineering + soft validation |
| **Enforcement** | Mandatory | Nice-to-have |

## Testing Strategy

**Test Case**: Combat scenario with multiple rounds

**Metrics to Track**:
- % of combat responses with dice_rolls
- Average dice_rolls per combat action
- Correlation between response length and omission rate

**Before Fix**:
```
Combat responses: 5
With dice_rolls: 0
Compliance: 0%
```

**After Fix (Option C)**:
```
Combat responses: 5
With dice_rolls: 4
Compliance: 80%
(Acceptable improvement)
```

## Implementation Priority

**Relative to rewards_processed fix**: Lower priority
- rewards_processed is critical for correctness
- dice_rolls is quality-of-life for transparency

**Recommendation**:
1. Fix narrative XP rewards first (achieve 2/2 test pass)
2. Then implement Option C for dice_rolls
3. Monitor compliance for 1 week
4. Iterate on prompt if compliance < 70%

## Implementation Location

**Prompt Changes**: `mvp_site/prompts/combat_system_instruction.md`
**Monitoring**: `mvp_site/world_logic.py` or `structured_fields_utils.py`

## Success Criteria

- [ ] Combat instruction emphasizes dice_rolls importance
- [ ] ESSENTIALS section includes dice_rolls mandate
- [ ] Server logs track compliance rate
- [ ] Compliance rate > 70% after prompt update
- [ ] Evidence bundle shows dice_rolls in most combat responses

## Related Issues

- E2E test: `testing_mcp/test_rewards_agent_real_e2e.py`
- Schema definition: `mvp_site/narrative_response_schema.py`
- Combat instructions: `mvp_site/prompts/combat_system_instruction.md`

## Decision

**Status Update (2026-01-22)**: Rewards test now passes 2/2 ✅

**Codex Review Findings**:
- Evidence bundle iteration_011 confirms dice_rolls missing in raw LLM output
- Server post-processes and synthesizes dice_rolls array from action_resolution
- 3/4 combat actions triggered warnings (actions 3, 4, 5)
- Severity confirmed as Medium

**Next Action**: Implement Option C (Hybrid Validation)

## Followup Tasks (Priority: Medium)

### Phase 1: Prompt Strengthening (Week 1)
- [ ] Update `mvp_site/prompts/combat_system_instruction.md`
  - Add dice_rolls to ESSENTIALS section (🚨 MANDATORY marker)
  - Add explicit examples showing dice_rolls for every combat action
  - Emphasize audit trail transparency requirement
- [ ] Update combat schema documentation
  - Mark dice_rolls as "strongly recommended" in schema comments
- [ ] Deploy prompt changes to staging

### Phase 2: Monitoring (Week 2)
- [ ] Add compliance tracking in `mvp_site/world_logic.py`
  - Log `llm.dice_rolls.missing` metric when dice_rolls absent
  - Track compliance rate per session
- [ ] Run test suite with new prompts
  - Target: >70% compliance in combat scenarios
  - Collect 20+ combat responses for sample size
- [ ] Review server.log for improvement

### Phase 3: Iteration (Week 3)
- [ ] If compliance < 70%:
  - Review prompt placement (move dice_rolls instructions higher)
  - Consider adding dice_rolls reminder in system message
  - Test with different combat scenarios
- [ ] If compliance > 70%:
  - Document success in bead
  - Close issue

### Acceptance Criteria
- ✅ Prompt explicitly requires dice_rolls for all combat actions
- ✅ ESSENTIALS section includes dice_rolls mandate
- ✅ Server logs track compliance rate
- ✅ Compliance rate > 70% in test suite
- ✅ Evidence bundles show dice_rolls in most combat responses

### Non-Goals
- ❌ 100% compliance (LLMs are probabilistic)
- ❌ Rejecting responses without dice_rolls (keeps combat working)
- ❌ Schema enforcement with retry logic (too complex)

## Timeline

**Start Date**: After rewards PR merged
**Target Completion**: 3 weeks after start
**Owner**: TBD
