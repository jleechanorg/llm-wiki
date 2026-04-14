# Deferred Rewards Protocol

<!-- ESSENTIALS (token-constrained mode)
- Runs every 10 player turns (scene_number), excluding GOD mode turns
- Scans recent story for missed XP/loot awards
- Fills rewards_box for any previously unprocessed rewards
- CRITICAL: Never double-count rewards already processed
- Check rewards_processed flags before awarding anything
/ESSENTIALS -->

## Overview

This protocol runs **in parallel with story mode** every 10 player turns to catch rewards that may have been missed during normal gameplay. It scans recent story events and ensures players receive appropriate XP and loot.

**Key Principle:** Fill gaps in rewards WITHOUT double-counting what was already awarded.

## When This Runs

- Automatically triggered every 10 scenes (every 10 player turns, i.e., when turn_number % 10 == 0; GOD mode turns are excluded)
- Executes within the same LLM call as story generation
- Does NOT interrupt the narrative flow

## Deferred Rewards Checklist

Scan the recent story (last scenes, matching the deferred rewards interval) for any of these reward-eligible events that may NOT have been properly processed:

### 1. Combat Victories
- Check `combat_state.rewards_processed` - if `false` and combat ended, rewards were missed
- Calculate XP from enemies defeated
- DO NOT award if `rewards_processed: true`

### 2. Encounter Completions
- Check `encounter_state.rewards_processed` - if `false` and encounter completed, rewards were missed
- Calculate XP based on encounter difficulty and type
- DO NOT award if `rewards_processed: true`

### 3. Quest Milestones
- Check `active_quests` for completed objectives without XP
- Check story narrative for significant achievements
- Cross-reference with `encounter_history` to avoid duplicates

### 4. Social/Roleplay Awards
- Significant NPC relationship changes
- Clever problem-solving that bypassed combat
- Successful skill checks that advanced the story

## Deduplication Protocol (CRITICAL)

Before awarding ANY rewards, verify they haven't been processed (primary deduplication is rewards_processed flags; XP checks are a secondary heuristic when flags are missing or ambiguous):

```json
{{STATE_EXAMPLE:RewardsPending}}

```

### XP Verification (Secondary Heuristic)

1. Calculate expected XP from all eligible events
2. Check current player XP (`player_character_data.experience.current`)
3. Only award DIFFERENCE between expected and actual when rewards_processed flags are insufficient
4. If player already has expected XP, award ZERO

**Example:**
- Combat should have awarded 100 XP
- Player already has 100 XP more than before combat
- Award: 0 XP (already processed)

**Example 2:**
- Combat should have awarded 100 XP
- Player XP unchanged from before combat
- Award: 100 XP (missed reward)

## Rewards Box Output

When missed rewards are detected, include a `rewards_box` in your response:

```json
{
  "rewards_box": {
    "source": "deferred",
    "deferred_reason": "Missed rewards from Scene [N]",
    "xp_gained": 50,
    "current_xp": 350,
    "next_level_xp": 900,
    "progress_percent": 38,
    "level_up_available": false,
    "loot": ["Items missed earlier"],
    "gold": 0
  }
}
```

### Source Field

Use `"source": "deferred"` to indicate these are catch-up rewards.

### Deferred Reason Field

Include `"deferred_reason"` to explain what was missed:
- "Missed combat rewards from Scene 5"
- "Uncredited encounter completion from heist"
- "Quest milestone XP not previously awarded"

## Narrative Integration

When awarding deferred rewards, integrate naturally into the narrative:

**Good:**
> "As you catch your breath, you realize the full weight of your recent victories. The experience gained from your encounter with the goblins settles into your muscles and mind."

**Bad:**
> "SYSTEM: You missed 50 XP from an earlier combat."

## State Updates

Include proper state updates to prevent future double-processing:

```json
{
  "state_updates": {
    "player_character_data": {
      "experience": {"current": 350}
    },
    "combat_state": {
      "rewards_processed": true
    },
    "encounter_state": {
      "rewards_processed": true
    }
  }
}
```

## Edge Cases

### No Missed Rewards
If all rewards were properly processed, do NOT output a rewards_box.
Simply continue with the normal story narrative.

### Multiple Missed Rewards
Combine all missed rewards into a single `rewards_box`:
- Sum XP from all sources
- Combine all loot items
- Use `"deferred_reason"` to list all sources

### Level-Up Detection
If deferred rewards push player to level-up threshold:
1. Set `level_up_available: true` in rewards_box
2. Include level-up offer in narrative
3. Provide planning_block choices for level-up

## CRITICAL RULES

1. **NEVER double-count** - Always verify `rewards_processed` flags
2. **NEVER interrupt narrative** - Integrate rewards naturally
3. **ALWAYS include rewards_box** when awarding deferred XP
4. **ALWAYS set rewards_processed: true** after awarding
5. **ALWAYS check XP totals** to verify rewards weren't already applied
6. **SKIP if nothing missed** - No output if all rewards processed correctly
