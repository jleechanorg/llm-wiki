# Planning Protocol (Unified)

**Purpose**: Single source of truth for planning block structure and rules.

This protocol applies to all planning blocks regardless of mode. The key difference between modes is TIME HANDLING:

| Mode | Trigger | Time Behavior | Agent |
|------|---------|---------------|-------|
| **Think Mode** | `THINK:` prefix or `mode="think"` | Time FROZEN (+1 microsecond only) | `PlanningAgent` |
| **Story Mode** | Every story response | Time ADVANCES normally | `StoryModeAgent` |

---

## Planning Block Structure

The canonical schema is defined below. (Note: This schema is automatically injected from `narrative_response_schema.py` - you see the full schema content here, not just a reference.)

### Core Fields (Canonical Schema)

{{PLANNING_BLOCK_SCHEMA}}

### Choice Structure

{{CHOICE_SCHEMA}}

**CRITICAL ORDERING RULE**: When a parallel execution option is included, it **MUST be placed LAST** in the choices array. All individual situational choices must come first, followed by the parallel execution option as the final choice. This ensures consistent UI presentation with the parallel option always appearing at the bottom.

**Example with Parallel Execution (correct ordering):**
```json
{
  "thinking": "The player faces three critical objectives that could be tackled sequentially or in parallel.",
  "context": "Post-battle strategic planning phase",
  "choices": [
    {
      "id": "audit_avernus",
      "text": "Audit Avernus Remnants",
      "description": "Systematically collect the remaining diabolical assets and souls in the First Layer while the Hells are in shock.",
      "risk_level": "high",
      "pros": ["Massive soul harvest", "Consolidate Hells territory"],
      "cons": ["Increases chance of meeting Hellfire Auditors"],
      "confidence": "high"
    },
    {
      "id": "return_to_waterdeep",
      "text": "Return to Waterdeep",
      "description": "Personally oversee the final conversion of the Watchful Order and the Masked Lords to secure the North.",
      "risk_level": "high",
      "pros": ["Total shadow control of the North", "Stabilize 'Paradise' network"],
      "cons": ["Direct exposure to Elminster's proximity"],
      "confidence": "high"
    },
    {
      "id": "parallel_synergistic",
      "text": "Delegate Avernus, Focus Waterdeep (Synergistic)",
      "description": "Ketheric handles the Avernus audit while you personally secure Waterdeep - tasks in different planes, no interference.",
      "risk_level": "high",
      "pros": ["Maximum ROI", "Maintain momentum on all fronts", "Synergy: Hell distraction covers Waterdeep moves"],
      "cons": ["Must trust Ketheric with Hell operations"],
      "confidence": "high",
      "analysis": {
        "combination_type": "synergistic",
        "synergy_bonus": "Chaos in Avernus draws planar attention away from Material Plane operations",
        "delegation_targets": ["Ketheric handles Avernus audit"],
        "personal_focus": "Waterdeep conversion requires direct oversight",
        "dc_modifier": 0,
        "coordination_dc": 16
      }
    },
    {
      "id": "parallel_conflicting",
      "text": "Personal Oversight of Both (+3 DC)",
      "description": "Use planar projection to maintain direct oversight of Ketheric in Avernus while physically present in Waterdeep.",
      "risk_level": "high",
      "pros": ["Complete control of both operations", "Catch any deception from Ketheric immediately"],
      "cons": ["Divided attention across planes (+3 DC)", "Vulnerability while projecting"],
      "confidence": "medium",
      "analysis": {
        "combination_type": "conflicting",
        "unique_outcome": "Detect and counter any betrayal by Ketheric in real-time - impossible if delegated fully",
        "delegation_targets": [],
        "personal_focus": "Both require direct oversight",
        "dc_modifier": 3,
        "coordination_dc": 19
      }
    }
  ]
}
```

**Note**: The `parallel_execution` choice is always the **last** element in the choices array. Individual situational choices come first.

### Field Requirements by Mode

| Field | Think Mode | Story Mode |
|-------|------------|------------|
| `plan_quality` | REQUIRED (INT/WIS roll) | Not used |
| `thinking` | REQUIRED (deep analysis) | Optional |
| `situation_assessment` | REQUIRED | Optional |
| `choices` | REQUIRED (situation-specific; include return-to-story only when appropriate) | REQUIRED |
| `analysis` | REQUIRED | Optional |

---

## Parallel Execution Option (MANDATORY)

🚨 **MANDATORY**: When presenting 2+ situational choices (excluding meta-choices), include parallel option(s). Must be placed **LAST** in choices array.

**Exclusions**: Only 1 choice available, mutually exclusive choices, meta-choices only, explicit sequential dependencies.

### Three-Tier Model

| Type | DC | Outcome | When |
|------|-----|---------|------|
| **Synergistic** | +0 | Bonus (enemies can't react) | Different assets/locations, timing advantage |
| **Compatible** | +0 | Time savings only | No overlap, no synergy |
| **Conflicting** | +2 to +4 | **Unique outcome** (impossible sequentially) | Same resource needed (attention, spell slot, key ally) |

**Key Rules:**
- Synergistic: Reward smart combinations. Synergy bonus = narrative outcome impossible if sequential.
- Conflicting: +2 mild, +3 significant, +4 severe. **Unique outcome MUST justify the DC penalty.**
- Success: ×1.2 XP, reduced time (2 tasks: 1.25-1.5x, 3 tasks: 1.5x, 4+: 1.75-2.5x)
- Partial/Failure: Some tasks delayed/fail, or coordination breakdown.

### Example

```json
"parallel_synergistic": {
  "text": "Pincer Strike (Synergistic)",
  "description": "Grey Worm seizes warehouses while Doves hit estates - different teams, different locations",
  "risk_level": "medium",
  "pros": ["Targets can't warn each other", "Ledgers intact"],
  "cons": ["Must trust both teams independently"],
  "confidence": "high",
  "analysis": {
    "combination_type": "synergistic",
    "synergy_bonus": "Merchants arrested before burning home records",
    "dc_modifier": 0,
    "coordination_dc": 14
  }
},
"parallel_conflicting": {
  "text": "Total Magical Dominance (+3 DC)",
  "description": "Divide magical attention to personally oversee ALL operations",
  "risk_level": "high",
  "pros": ["Complete control", "Intercept fleeing messenger"],
  "cons": ["Divided magical focus (+3 DC)"],
  "confidence": "medium",
  "analysis": {
    "combination_type": "conflicting",
    "unique_outcome": "Capture courier mid-flight - impossible if done sequentially",
    "dc_modifier": 3,
    "coordination_dc": 17
  }
}
```

**Note**: Conflicting option explicitly states DC penalty in text and justifies why unique outcome is worth the risk.

---

## Choice ID Naming

Choice `id` values must follow these conventions:
- **Format**: `snake_case` identifiers
- **Allowed prefixes**: `god:`, `think:`
- **Pattern**: `^(god:|think:)?[a-zA-Z_][a-zA-Z0-9_]*$`

### Contextual Choice IDs

Use these prefixes only when the situation calls for them:

| ID | Purpose |
|-----|---------|
| `think:continue` | Optional: stay in Think Mode for deeper analysis |
| `think:return_story` | Optional: include only when the situation calls for exiting Think Mode and resuming the story; omit otherwise |
| `god:*` | God Mode actions (DM commands) |

---

## Risk Levels

Valid values for `risk_level`: {{VALID_RISK_LEVELS}}

- `safe` - No risk, guaranteed success
- `low` - Minor consequences if failed
- `medium` - Notable consequences possible
- `high` - Significant danger or cost

---

## Confidence Levels

Valid values for `confidence`: {{VALID_CONFIDENCE_LEVELS}}

The `confidence` field is **mechanics-only** (adjusts execution DC) and is never shown to the player as a label. Express certainty through the *language* of pros/cons instead:
- High confidence → specific, concrete pros; vague or minor cons
- Low confidence → visceral, concrete cons; hedged or uncertain pros

**Plan quality stat-gating**: When plan_quality tier is `Confused` or `Muddled`, skew assessments to reflect the character's flawed analysis — dangerous options may feel safer than they are, cautious options may seem riskier than they are.

**Tradeoff framing**: Frame each option's costs on distinct axes (time, noise, relationships, resources, commitment, positioning) so no single option is strictly dominant. Avoid choices where one option is "just better".

---

## Mechanical Impact (Plan Quality → DC)

**Planning is NOT just flavor.** Plan quality and choice selection directly affect operation DCs.

### How It Works

When a player executes a choice from a planning block, the DC is adjusted:

| Factor | DC Modifier |
|--------|-------------|
| Chose `recommended_approach` | **-2** |
| Chose `high` risk option | **+2** |
| Planning tier `Brilliant`/`Masterful` | **-1** |
| Planning tier `Confused` | **+2** |
| Confidence `low` on chosen approach | **+1** |

### Why This Matters

- **Smart planning is rewarded**: Choosing the recommended approach gives a mechanical advantage
- **Risk has consequences**: High-risk choices are genuinely harder to execute
- **INT/WIS matters for execution**: A brilliant plan (high INT/WIS roll) makes operations easier
- **Failed planning hurts**: A confused analysis creates real obstacles

### Example Flow

1. Player enters Think Mode: "How do I sneak past the guards?"
2. **Planning check:** Character rolls INT 22 vs planning DC 12 → **Brilliant** tier (margin = 22 - 12 = +10)
3. Planning block presents options with `risk_level` and `confidence`
4. Player selects the `recommended_approach` (timing patrol rotations)
5. **Execution check:** Base execution DC 15 - 2 (recommended) - 1 (brilliant) = **DC 12**

*Note: Planning DC and execution DC are separate. The planning check determines quality tier; the execution DC is set by the situation and then adjusted by modifiers.*

### Caps

- Maximum adjustment: ±4 DC
- Minimum DC: 5 (trivial tasks don't need rolls)
- Maximum DC: 30 (impossible is impossible)

### Risk/Reward Balance

**High-risk options have higher DCs but better rewards on success - XP, loot, AND narrative.**

| Risk Level | DC Effect | XP | Loot | Narrative |
|------------|-----------|-----|------|-----------|
| `safe`/`low` | +0 | ×1.0 | Standard | Standard outcome |
| `medium` | +0 | ×1.25 | +10% gold | Minor bonus |
| `high` | **+2** | **×1.5** | **+25% gold, bonus item** | **Superior outcome** |

*`safe` = no meaningful downside; `low` = minor stakes. Both share mechanical modifiers but differ narratively.*

#### Planning Quality Reward Bonuses

| Tier | XP | Loot |
|------|-----|------|
| `Masterful` | ×1.25 | Rare item chance |
| `Brilliant` | ×1.1 | Uncommon item chance |
| Others | ×1.0 | Standard |

**Stack Example:** High-risk (×1.5) × Masterful (×1.25) = **×1.875 XP**

#### High-Risk Rewards Include:
- **More information** (interrogation vs killing)
- **Better positioning** (infiltrate vs sneak past)
- **Bonus loot** (claim artifact vs destroy it)
- **Story branches** (ally vs enemy)
- **Reputation gains** (bold success impresses NPCs)

#### Example Pairs

| Safe (easier) | Risky (harder but better) |
|--------------|---------------------------|
| Kill the guard | Capture for interrogation |
| Pick one lock | Disable whole alarm system |
| Flee the dragon | Negotiate an alliance |
| Destroy the artifact | Claim its power |

This creates meaningful choice: safe = reliable, risky = potentially superior outcome.

---

## Freeze Time Flag

The optional `freeze_time` boolean on a choice controls time advancement:

- `freeze_time: true` - When player selects this choice, time advances by only 1 microsecond (like Think Mode)
- `freeze_time: false` or omitted - Normal time advancement

### When to Use freeze_time

Set `freeze_time: true` for **meta-game decisions** that don't represent in-game time passing:

| Choice Type | freeze_time | Reason |
|------------|-------------|--------|
| `level_up_now` | `true` | Character advancement is instantaneous |
| `continue_adventuring` | `true` | Deferring level-up is a meta decision |
| Story actions (attack, explore, talk) | `false` | Real in-game actions take time |
| Think Mode choices | N/A | Already handled by Think Mode |

### Example

```json
{
  "choices": [
    {
      "id": "level_up_now",
      "text": "Level Up to Level 5",
      "description": "Apply Fighter level 5 benefits immediately",
      "risk_level": "safe",
      "freeze_time": true
    },
    {
      "id": "attack_goblin",
      "text": "Attack the Goblin",
      "description": "Swing your sword at the nearest goblin",
      "risk_level": "medium"
    }
  ]
}
```

---

## Quality Tiers (Think Mode)

Valid values: {{VALID_QUALITY_TIERS}}

**See `think_mode_instruction.md` for complete DC scaling and quality tier rules.**

Summary: Roll INT/WIS check vs DC (DC 2-20 for typical play, scales higher for epic scope). Quality tier determined by margin:
- **Success**: Competent (meet DC) → Sharp (+5) → Brilliant (+10) → Masterful (+15)
- **Failure**: Incomplete (-1 to -4) → Muddled (-5 to -9) → Confused (-10+)

---

## Time Handling Rules

### Think Mode (FROZEN)
When mode is "think" or user prefixed with `THINK:`:
- Time advances by exactly 1 microsecond
- Turn counter does NOT increment
- No narrative advancement (no dice rolls that advance story)
- Response is pure strategic analysis

### Story Mode (ADVANCES)
All other story responses:
- Time advances normally based on actions
- Turn counter increments
- Narrative progresses
- Choices represent player agency

**CRITICAL**: Time handling is determined by MODE, not by presence of planning_block.

---

## Field Separation Rule

The planning_block is a SEPARATE JSON field:
- Never embed planning_block JSON in the `narrative` field
- The `narrative` field contains story prose ONLY
- Choices go in `planning_block.choices`, not in narrative text
- The frontend reads `planning_block` as a structured object

---

## Plan Freeze Mechanic (Think Mode Only)

When a planning check **FAILS**, the character cannot re-think the same topic until a cooldown period passes.

### Freeze Duration by DC (Scales with Scope)

| Original DC | Freeze Duration |
|-------------|-----------------|
| DC 2-8 | 1 hour |
| DC 9-12 | 2 hours |
| DC 13-16 | 4 hours |
| DC 17-20 | 8 hours |
| DC 21+ | 24 hours |

**Note**: Freeze durations are in **game time**.

### Freeze Tracking in State

On failed planning check, add to `state_updates.frozen_plans`:

```json
"frozen_plans": {
    "<plan_topic_key>": {
        "failed_at": "<current_world_time>",
        "freeze_until": "<world_time + freeze_duration>",
        "original_dc": 14,
        "freeze_hours": 4,
        "description": "planning the warehouse ambush"
    }
}
```

### Freeze Rules

1. **On Failure**: Record frozen plan in state_updates
2. **On Re-attempt**: Check if topic is frozen; if so, reject with remaining time and skip re-rolling
3. **Different Topics**: Always allowed - freeze is topic-specific; use distinct topic keys
4. **Early Break**: Lift freeze when significant new information arrives, a materially different approach is taken (new topic key), relevant assistance is provided, or an orchestrator override/`gm_override` is explicitly set

---

## Validation

The validation code in `narrative_response_schema.py`:
- Validates against `VALID_RISK_LEVELS`
- Validates against `VALID_CONFIDENCE_LEVELS`
- Validates against `VALID_QUALITY_TIERS`
- Validates `plan_quality` DC/margin/success consistency and coerces invalid inputs
- Validates `freeze_time` as boolean (accepts string "true"/"false" for robustness)
- `frozen_plans` is enforced by the LLM via prompts (timestamps/DC-derived durations are constrained in prompts, not Python code)
- Sanitizes HTML/script content for security
- Requires both `text` and `description` for each choice
