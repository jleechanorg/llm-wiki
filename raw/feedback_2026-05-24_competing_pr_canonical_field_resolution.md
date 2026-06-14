---
name: When competing PRs choose opposite canonical fields, the later PR must take THEIRS everywhere
description: PR #7048 raced #6896 — both location-centralization, opposite canonical fields. Resolution = take THEIRS on all touched files + add only additive changes on top.
type: feedback
bead: rev-igs3c
---

Two PRs (#7048 location_util module with `world_data.location` canonical,
#6896 inline `resolve_location` with `world_data.current_location_name`
canonical) targeted the same architectural problem with **opposite canonical
field choices**. PR #6896 merged first.

**Why this matters:** picking OURS on any location-touching file after #6896
merged would have re-introduced a write to `world_data.location` while the
rest of `main` (deployed) reads `current_location_name`. Every downstream
consumer would have broken silently.

**How to apply (general race-resolution pattern):**

1. When taking a merge of `origin/main` and conflicts surface in files
   that touch the same architectural decision the loser-PR designed
   around, **take THEIRS for ALL of those files**, including their tests.
2. Identify dead artifacts that loser-PR created (in #7048: `location_util.py`
   has zero callers after taking THEIRS for 6 files). Decide explicitly:
   delete OR keep as scaffolding. Document the choice.
3. Add only **additive** changes on top of THEIRS — e.g. PR #7048 kept the
   additive `locations` (plural) strip, the freeze-time location-guard, end2end
   test fixes, CI inclusion, beads dedupe. These don't fight the canonical.
4. Tests must match production. If you take THEIRS on production, take
   THEIRS on the matching test file too (signature mismatch otherwise).

**Concrete files this session (took THEIRS):** `mvp_site/agent_prompts.py`,
`mvp_site/context_compaction.py`, `mvp_site/llm_parser.py`,
`mvp_site/llm_service.py`, `mvp_site/preventive_guards.py`,
`mvp_site/tests/test_preventive_guards.py`.

**Kept OURS** (genuinely cleaner): `testing_mcp/schema/test_schema_migration_flow_real_api.py`
(defensive dict check at backend boundary), `.gitattributes` initially (later
re-took THEIRS on CR feedback — AGENTS.md:174 explicitly pins `merge=beads`).

**Verification:** all 6 affected files compile and import cleanly; whole-file
test suites pass (47 end2end + 12 location_util + 74 preventive_guards);
`location_util.py` retained as future scaffolding with 12 standalone unit
tests still passing.

Related: [[7green-proof-artifact]], [[pr-race-conditions]]
