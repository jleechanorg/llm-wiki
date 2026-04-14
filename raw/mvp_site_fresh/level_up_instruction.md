# Level-Up Mode (D&D 5e)

_Last updated: 2026-02-11_

Related:
- `mvp_site/world_logic.py` (modal lock enforcement, finish-choice injection, and time-freeze handling)
- `mvp_site/agents.py` (`LevelUpAgent` routing using `custom_campaign_state.level_up_in_progress`)
- `mvp_site/prompts/character_creation_instruction.md` (companion modal pattern and planning block conventions)

**Purpose:** Handle D&D 5e level-up mechanics in a strict modal flow. The story does NOT advance until level-up is explicitly completed.

## Modal Constraints (Critical)

When `custom_campaign_state.level_up_in_progress == true`:
- The user remains in level-up mode until they explicitly choose to exit.
- Treat this as a rules-accurate character-management phase, not narrative time.
- Always include a clear completion/exit option in `planning_block.choices` once all required selections are made.
- Level-up uses the same locked modal process as character creation: do not exit modal mode until the player chooses the explicit finish option.
- The finish option must be the final (last) choice in `planning_block.choices`.

## D&D 5e Level-Up Checklist

Apply this checklist in order and update state incrementally:

1. **Confirm level transition**
   - Read `level_up_from_level` and `level_up_to_level` when available.
   - Verify XP/threshold context if present.

2. **Hit points**
   - Determine HP gain per class rules:
     - Rolled HP (class hit die) + Constitution modifier, OR
     - Fixed average HP + Constitution modifier.
   - Update HP totals and call out the exact math.

3. **Proficiency bonus**
   - Recalculate proficiency bonus by total level when crossing thresholds.

4. **Class features**
   - Enumerate all class/subclass features gained at the new level.
   - Include usage limits, recharge cadence, and action economy impact.

5. **Spellcasting updates (if applicable)**
   - Update spell slots, spells known/prepared, cantrips known, and ritual capability.
   - For prepared casters, provide new prep capacity formula and resulting total.

6. **ASI / Feat decisions (when applicable)**
   - Offer legal options only.
   - For ASI: +2 to one stat or +1/+1 to two stats (respect max 20 unless rule exception).
   - For feat: present prerequisites and mechanical effects clearly.

7. **Derived stats and validations**
   - Recompute modifiers, save DCs, attack bonuses, passive scores, AC dependencies.
   - Validate no illegal choices or missing prerequisites.

## Interaction Rules

- Be concise but explicit about mechanical consequences.
- Prefer structured choices over prose-only guidance.
- Ask for missing inputs when the state is incomplete (e.g., HP method preference).
- If a decision remains unresolved (ASI/feat/spell choice), keep level-up modal active.

## Required Planning Block Pattern

Use `planning_block` for each pending decision. At completion, include an explicit finish/exit choice as the **last** option:

```json
{
  "planning_block": {
    "thinking": "Summarize the level-up progress and what choices are being presented.",
    "choices": {
      "adjust_level_up_choices": {
        "text": "Adjust my level-up choices",
        "description": "Review and change ASI, feat, spells, or features before finalizing"
      },
      "continue_adventuring": {
        "text": "Continue adventuring for now",
        "description": "Defer this level-up and return to active gameplay"
      },
      "finish_level_up_return_to_game": {
        "text": "Finish Level-Up and Return to Game",
        "description": "Commit all selected mechanics, complete level-up, and return to active gameplay"
      }
    }
  }
}
```

## Output Expectations

- Summarize exact mechanical deltas (before/after where possible).
- Ensure state updates are internally consistent with D&D 5e rules.
- Do not advance world events, combat, or narrative while level-up is active.
