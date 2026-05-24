---
name: levelupagent-inline-override-must-name-exact-canonical-choice-ids
description: "Vague \"expose a change choice\" in agents.py inline override is insufficient; the model ignores it. The literal id string (e.g. level_up_change_prepared_spells) must appear in a MANDATORY statement."
metadata: 
  node_type: memory
  type: feedback
  bead: rev-vcm7y
  originSessionId: 690042ca-d406-4db8-bb67-52c95e31f023
---

## Context

PR [#7064](https://github.com/jleechanorg/worldarchitect.ai/pull/7064) — level-up modal fix on branch `pr6958-zfc-evidence-followups`.

The organic level-up test (`testing_mcp/core/test_level_up_organic.py --level-up-scenario single-organic`) ran 6 iterations. Iterations 4 and 5 both failed with adversarial codex VERDICT: FAIL:

> "the modal recommends prepared spells (Bless, Cure Wounds, Searing Smite) but exposes no planning-block edit path for prepared spells. Level-up modal choices only cover fighting style, HP roll, and finish."

## Root Cause

`mvp_site/agents.py` — `LevelUpAgent.build_system_instructions()` appends an inline string override at the END of every system prompt. The override explicitly says "if there is any conflict, follow this override."

**Before fix (iter4/5):** The override said:
```
"For prepared casters, recommend a complete prepared-spell loadout and expose a
manual/change preparation choice; do not count always-prepared..."
```
This is vague — "expose a change choice" does not specify which ID to use. The model treats spell preparation as automatic and omits the choice entirely, or uses a non-canonical ID.

**The iter4 fix** (commit `fdb2090d2`) updated `level_up_instruction.md` to name `level_up_change_prepared_spells` and add the Paladin Level 2 example. This did NOT fix the issue because the inline override (which takes precedence) still had the vague phrasing. The level_up_instruction.md change was ignored.

## Solution / Rule

The inline override must name the exact canonical ID in a MANDATORY statement:

```python
"For prepared casters (Paladin, Cleric, Druid, Wizard, Artificer, "
"etc.), MANDATORY: the planning block MUST include a choice with "
"id `level_up_change_prepared_spells` (use exactly that id string, "
"no variant) so the player can swap any recommended spell before "
"finishing. Paladin Level 2 gains spellcasting for the first time; "
"the `level_up_change_prepared_spells` choice is required even when "
"fighting style and HP choices are also present."
```

**Note:** The Gemini context cache (cachedContents/) was NOT the cause — the agents.py inline override is always appended at runtime directly, not from any cached content. The root cause was purely the vague phrasing in the override.

## Verification

After iter6 fix (commit `4addef91430baec4c681febb486ca137ed92878f`):
- `test_level_up_organic.py --level-up-scenario single-organic` → 3/3 PASS (100%)
- Adversarial codex review → VERDICT: PASS
- Evidence: `/tmp/worldarchitect.ai/pr6958-zfc-evidence-followups/test_level_up_organic/iteration_006/`
- Campaign: `gdfxr38Qn1sA1LEYswVo`

## Reusable Pattern

**Anti-Pattern (broken):**
```
"expose a manual/change preparation choice"  # Too vague — model ignores or invents ID
```

**Correct Pattern (working):**
```
"MANDATORY: the planning block MUST include a choice with id `level_up_change_prepared_spells`
(use exactly that id string, no variant)"  # Explicit ID → model complies
```

**General rule:** When an LLM inline override requires a specific structured field value (choice id, field name, enum value), the override must state the literal value verbatim. "Expose a choice for X" without naming the id is insufficient. Use "MANDATORY: include choice with id `exact_id_here`".

## References

- PR: https://github.com/jleechanorg/worldarchitect.ai/pull/7064
- Bead: rev-vcm7y
- Fix file: `mvp_site/agents.py` (LevelUpAgent.build_system_instructions, around line 1394)
- Fix commit: `4addef91430baec4c681febb486ca137ed92878f`
- Prompt fix: `mvp_site/prompts/level_up_instruction.md` (commit `fdb2090d2` — adds the ID to the canonical list, but was insufficient alone)
- Evidence: `/tmp/worldarchitect.ai/pr6958-zfc-evidence-followups/test_level_up_organic/iteration_006/`
