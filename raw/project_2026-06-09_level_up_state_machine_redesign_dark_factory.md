---
name: level-up-state-machine-redesign-with-dark-factory-2026-06-09
description: "User pivoted the level-up fix to a 6-PR state-machine migration. /innovate redesign applied 5 dark-factory patterns + 3 anti-patterns + 6 brownfield Step-0 rules. Beads rev-254ez (interim 30-LOC gate), rev-544i4 (migration-aware observer), rev-9f200 (meta) updated; rev-g8s1z (brownfield Step-0) filed."
metadata:
  type: project
  originSessionId: 587748e4-1a5e-4699-bff2-28948fdd3b9f
---

# Level-up state-machine redesign with dark-factory patterns (2026-06-09)

**Source:** User pivot: "Wait just design this but use /ms we are transitioning to a level up state machine, would this still be useful?" + "also look at the dark factory repo we have locally in parallel and see if anything to learn from there too / continue"

**Why this matters:** The original /innovate answer (rev-254ez 30-LOC invariant gate + rev-544i4 daily observer) was a stopgap. Once the user designated `~/roadmap/level-up-session-state-machine-design-2026-06-08.md` as the north star, both beads had to be re-scoped: the 30-LOC gate becomes an INTERIM safety net (ships before PR 1, removed in PR 6), and the observer becomes MIGRATION-AWARE (pre-PR 5.5 mode watches 4 fields, post-PR 5.5 mode watches 6-state status + 14 invariants).

**How to apply:** When working on the level-up state-machine migration (rev-1qf5c parent + 7 children), always cite:
- rev-1qf5c (parent), rev-gt1as/0yvvv/lzx3k/isr27/iwito/547fk/pg5fj (PR 1-5.5/6)
- rev-254ez (interim gate, lives until rev-pg5fj)
- rev-544i4 (migration-aware observer)
- rev-9f200 (meta bead, includes the original 90-PR-in-60-days audit)
- rev-g8s1z (brownfield Step-0 classification, 6 dark-factory rules)
- dark-factory canonical state pattern: runner/engine.py:688-691, 1156-1158
- dark-factory pre-write validation: runner/handlers.py:772-845
- dark-factory sealed event log: runner/cxdb.py:21-53
- dark-factory declarative transition table: runner/parser.py:214, 435, 473
- dark-factory brownfield Step-0: ~/.claude/skills/factory-spec/SKILL.md:61-101

**5 dark-factory patterns applied to the migration:**

1. **Canonical state object** — `game_state.level_up_session` mirrors `ctx.state` (engine.py:688-691, 1156-1158). One source of truth, all 5 legacy fields become derived compatibility outputs.

2. **Pre-write validation hook** — `assert_level_up_invariants()` before any commit mirrors `_tool` validation (handlers.py:772-845). Pure function, no side effects, returns violation list.

3. **Sealed event log** — PR 5.5 (rev-547fk) structured transition log mirrors CXDB append-only schema (cxdb.py:21-53). Every reducer call writes a transition record for the observer (rev-544i4) to consume.

4. **Declarative transition table** — Status enum + allowed-next-states table mirrors parser.py:214/435/473 load-time condition validation. The 6 statuses and 7 allowed transitions are validated at module load.

5. **Brownfield Step-0 classification** — The 6-PR migration is brownfield (5 fields removed → 1 object); must apply the 6 rules before any code is written. Filed as rev-g8s1z.

**3 dark-factory anti-patterns the migration must NOT replicate:**

1. **Stale-success (runs.final masking)** — never let `CI green` mask a partial migration. The 6-PR plan MUST NOT report "migration complete" until PR 6 (legacy writer deletion) lands and the grep gates pass.

2. **Backwards-proof staging** — never prove the new code path works while the old path is still active. PR 5 (routing migration) must flip the router atomically; do not run old + new routers in parallel "for safety."

3. **Dead code passing test_e2e** — the legacy 4-field writers must be DELETED in PR 6, not merely "no longer called." Grep gates enforce this. Test e2e on the post-deletion tree is the only acceptable proof.

**6 brownfield Step-0 rules mapped to each PR (rev-g8s1z full matrix):**

| Rule | Description | Where in migration |
|---|---|---|
| 1 | DELETE-FIRST ordering (deletions planned in PR description, not follow-up) | Every PR |
| 2 | Deletion in executor node (same commit as flip) | PR 2, 3, 4, 5, 6 |
| 3 | Net production LOC ≤ 0 | Every PR (5.5 excepted, justified) |
| 4 | Reference from runtime call site (no new modules) | Every PR |
| 5 | Replace at same call site (delete + write in same hunk) | PR 5, 6 |
| 6 | Prove against post-deletion tree | PR 6 only (final proof) |

**Revised /innovate answer (the single smartest addition now):**

The 30-LOC invariant gate (rev-254ez) and the daily observer (rev-544i4) — but redesigned: the gate becomes INTERIM (ships before PR 1, removed in PR 6), and the observer becomes MIGRATION-AWARE (consumes PR 5.5's structured log). Together with the brownfield Step-0 classification (rev-g8s1z), they make the 6-PR migration un-gameable: the gate prevents new bugs from shipping, the observer detects current bugs and tracks migration progress, and the brownfield rules prevent the migration from drifting into 5 additive PRs + a follow-up cleanup PR (which is the "90 PRs in 60 days" pattern that produced the bug class in the first place).

**Beads updated in this session:**
- rev-254ez (interim 30-LOC invariant gate, lives until PR 6 / rev-pg5fj)
- rev-544i4 (migration-aware daily observer, pre-PR 5.5 + post-PR 5.5 modes)
- rev-9f200 (meta: state machine pivot + dark-factory patterns appended, original 90-PR audit preserved)
- rev-g8s1z (NEW: brownfield Step-0 classification, 6 rules mapped to 6 PRs)

**Related:** project_2026-06-08_level_up_session_state_machine_pivot.md (parent design), project_2026-06-08_level_up_diamond_state_class.md (bug class), project_2026-06-08_mppfHseT_finish_commit_real_bugs.md (raw LLM evidence), feedback_2026-05-30_dark_factory_brownfield_flaws.md (dark-factory brownfield history)
