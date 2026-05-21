---
name: ZFC violation spiral from symptom-patching instead of root-cause prompt fix
description: PR #6908 accumulated 61 commits because server-side injection was added to patch symptoms instead of fixing the upstream LLM prompt — the canonical ZFC anti-pattern
type: feedback
bead: rev-vlf45
---

# ZFC Violation Spiral — Symptom-Patching Anti-Pattern (PR #6908)

## What happened

PR #6908 "fix: preserve model-owned choices after level-up finish" accumulated **61 commits** before the
actual 5-line root-cause fix was written. The root cause: the LevelUpAgent had no explicit instruction
telling the LLM to return story choices on the post-finish turn. Every other "fix" was server-side
symptom-patching.

**The spiral pattern:**
1. Symptom observed: fallback choices appear after level-up finish
2. Fix: add server-side choice injection (`_inject_modal_finish_choice_if_needed`)
3. New symptom: injection fires in wrong cases, corrupts other states
4. Fix: gate the injection with more conditions
5. New symptom: conditional injection misses edge cases
6. Fix: add more conditions, more guards...
7. (repeat 50+ more times)

The ZFC principle was violated at step 2. The server was inferring what choices should exist, which is
model territory. Each subsequent commit was making the violation worse, not better.

**The 5-line fix that ended 61 commits:**
- Remove all 4 `_inject_modal_finish_choice_if_needed` calls from `llm_parser.py`
- Remove `_ensure_custom_action_planning_block` from the canonical stream path (it was creating a
  `server_generated=True` block that replaced valid LLM choices)
- Remove `else: pop("planning_block")` that deleted valid Gemini choices when no canonical replacement
- Keep `_ensure_custom_action_planning_block` only as true last-resort (LLM returns nothing at all)
- Add LevelUpAgent post-finish prompt example so the LLM knows to return story choices

**Test result after fix:** GREEN — LLM returned `strike_with_smite`, `defensive_parry`, `cast_bless`,
`intimidating_challenge` without any server-generated choices.

## Why this kept compounding

1. **Misdiagnosis at commit 1**: The first `_inject_modal_finish_choice_if_needed` commit assumed
   the LLM would never return story choices on its own — rather than asking "why doesn't the prompt
   tell it to?"
2. **No ZFC pre-flight**: No one asked "Does the model have explicit instructions for this case?"
   before adding the injection. Answer: No. Fix: add the instruction.
3. **Symptom-visible, root-invisible**: Each iteration's test showed the wrong choices (symptom)
   but the root (missing prompt instruction) was invisible in test output.
4. **Backend complexity hides ZFC violations**: Each new guard made the injection look "smarter",
   reinforcing the wrong mental model.

## The ZFC pre-flight that would have caught this at commit 1

Before adding any server-side choice injection/fallback/inference, ask:
1. **Does the model have explicit instruction for this output?** (Check agent prompt / system instruction)
2. **Can the prompt fix this?** (Almost always yes — if model returns wrong output, fix the prompt)
3. **If yes, fix prompt first.** Only add backend as narrow logged invariant after prompt fix fails.

For PR #6908: the LevelUpAgent prompt had no post-finish JSON example → model guessed. Fix: add example.

## How to apply

- Before ANY `_inject_*`, `_fallback_*`, `_ensure_*`, `_repair_*` function that touches model output:
  run the 3-question ZFC pre-flight above.
- If a PR hits >15 commits on a single theme and the behavior is still wrong: **STOP**. Run `/zfclevel`.
  Odds are high the root is upstream in the prompt.
- `server_generated: True` on a planning_block is always a bug signal, not an acceptable state.
- Server can: persist, normalize, validate. Server CANNOT: infer, inject, synthesize choices.

**Why:** PR #6908 had 61 commits over multiple sessions. A 3-question pre-flight at commit 1 would have
revealed the missing prompt instruction and saved ~200+ engineer-hours across all sessions.
