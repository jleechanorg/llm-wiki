# PR #7: Expand system instruction with layered cs8 mechanics

**Repo:** jleechanorg/worldai_claw
**Merged:** 2026-02-22
**Author:** jleechan2015
**Stats:** +707/-30 in 11 files

## Summary
- Expand `system_instruction.md` with the cs8 Layer 1-6 content:
  - Canonical field contract + deprecation guard.
  - Unsupported/ambiguous input flow.
  - Dice mandate with no dice-in-narrative + missing_die mechanic requests.
  - Social HP trigger and required challenge box format.
  - Combat structure constraints (initiative order, no consecutive player turns, hit-only damage, end-phase XP).
  - Social/relationship/reputation invariants.
  - Evidence-fidelity contract linking scene claims to

## Raw Body
## Summary
- Expand `system_instruction.md` with the cs8 Layer 1-6 content:
  - Canonical field contract + deprecation guard.
  - Unsupported/ambiguous input flow.
  - Dice mandate with no dice-in-narrative + missing_die mechanic requests.
  - Social HP trigger and required challenge box format.
  - Combat structure constraints (initiative order, no consecutive player turns, hit-only damage, end-phase XP).
  - Social/relationship/reputation invariants.
  - Evidence-fidelity contract linking scene claims to state/mechanic outputs.
  - Living world + reward coherence constraints.
  - Level-up planning-block requirements and XP-visible progression flow.
- Add prompt as Markdown source artifact at `packages/backend/src/llm/prompts/system_instruction.md`.
- Update `packages/backend/src/llm/system_instruction.ts` to load markdown from filesystem with fallback candidate paths.

## Validation
- Ran targeted test in `packages/backend`:
  - `npm test -- systemInstruction.test.ts` → PASS (3 tests)

## Notes
- Existing PR was already open on `sysi` → `main`; this commit updates that PR with this task set.

<!-- CURSOR_SUMMARY -->
---

> [!NOTE]
> **Medium Risk**
> Changes the core system prompt content and how it’s loaded/validated at server startup; misconfigured paths or prompt growth could cause boot-time failures and behavior shifts in model outputs.
> 
> **Overview**
> Expands the WorldArchitect system prompt into a new `system_instruction.md` with stricter output/schema contracts and gameplay rules (canonical field/deprecation policy, ambiguity handling, dice/social/combat protocols, evidence-fidelity, rewards/living-world coherence, and level-up planning requirements).
> 
> Switches `SYSTEM_INSTRUCTION` to be loaded from the markdown file at runtime (with an env override and multiple fallback paths) and adds a hard startup guard (`assertSystemInstructionTokenLimit`) wired into app initialization plus a test ensuring the prompt stays within the 10k token budget.
> 
> Adds
