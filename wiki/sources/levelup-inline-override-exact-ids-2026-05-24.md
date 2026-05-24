# LevelUpAgent Inline Override Must Name Exact Canonical Choice IDs

**Date:** 2026-05-24  
**Type:** feedback / Anti-Pattern  
**Bead:** rev-vcm7y  
**PR:** https://github.com/jleechanorg/worldarchitect.ai/pull/7064

## Summary

When an LLM inline override (appended at runtime in agents.py) requires the model to output a specific `planning_block.choices` entry with a named id, the override must state the literal id verbatim. Vague instructions like "expose a change choice" are ignored.

## Anti-Pattern

```python
"For prepared casters, recommend a complete prepared-spell loadout and expose a
manual/change preparation choice"  # → model ignores or omits the choice
```

## Correct Pattern

```python
"MANDATORY: the planning block MUST include a choice with id
`level_up_change_prepared_spells` (use exactly that id string, no variant)"
```

## Evidence

- 6 iteration convergence loop on `test_level_up_organic.py --level-up-scenario single-organic`
- Iters 4 and 5 both produced VERDICT: FAIL (adversarial codex review)
- Iter 6 (agents.py fix with literal id) produced VERDICT: PASS, 3/3 scenarios
- Campaign: `gdfxr38Qn1sA1LEYswVo`, evidence: `/tmp/worldarchitect.ai/pr6958-zfc-evidence-followups/test_level_up_organic/iteration_006/`

## Source

`~/.claude/projects/-Users-jleechan-projects-worldarchitect-ai/memory/feedback_2026-05-24_levelup_inline_override_must_name_exact_ids.md`
