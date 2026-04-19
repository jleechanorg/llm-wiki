# WorldArchitect.AI Roadmap — 2026-04-18

## Active Work: Level-Up Bug Fix Stack

### Current Priority Queue

| Priority | PR | Branch | Status | Blocker |
|---|---|---|---|---|
| 1 | [#6370](https://github.com/jleechanorg/worldarchitect.ai/pull/6370) | fix/split-A-level-up-canonicalization | CHANGES_REQUESTED | CR: tri-state flags, legacy gs fallback, surgical planning_block removal |
| 2 | [#6371](https://github.com/jleechanorg/worldarchitect.ai/pull/6371) | fix/split-B-testing-mcp-stream-infra | CHANGES_REQUESTED | CR: endpoint validation + malformed done_payload |
| 3 | [#6372](https://github.com/jleechanorg/worldarchitect.ai/pull/6372) | fix/split-C-repro-scripts | UNSTABLE | Cursor 1 issue, CI settling |
| 4 | [#6373](https://github.com/jleechanorg/worldarchitect.ai/pull/6373) | fix/split-D-ci-docs-beads | UNSTABLE | CR re-review positive; CI running |

### What These Fix
The 6 user-reported level-up bugs (all REPRODUCED/WARN-FINAL in /er audits):
- `wOhBvrJ0gYA2Ox9g1kLC` (dev) — Class 4: "Level up to Level 1" stale story entries
- `WQEl4sJb7RqWLndJK4GU` (dev) — Class B: suppression cascade hides rewards box
- `WQEl4sJb7RqWLndJK4GU` (s10) — Class 4+B: same campaign, both environments
- `3JM2gKc3eTFZHQnBtO8m` (s10) — Class 2: missing rewards box  
- `gufBO3EVc0GAp5LmVzWG` (s10) — Class A+C: planning block/rewards box missing
- `KtKlU0rOV6MmG3b6cOxd` (s10) — Class D+E: rewards box not showing

### Fix #6370 Specific Issues (CR CHANGES_REQUESTED)
1. `agents.py` lines 1130-1165, 1415-1427, 3027-3072 — replace raw truthiness with `_is_state_flag_true/false`
2. `world_logic.py` `_resolve_level_up_signal` — add fallback to top-level `game_state_dict` when `custom_campaign_state` absent (legacy saves)
3. `rewards_engine.py` `_extract_xp_robust` — add legacy XP shapes (`player_data["xp_current"]`, scalar `player_data["experience"]`)
4. `world_logic.py` lines 1809-1839 — set `resolved_target_level` when XP-threshold fallback triggers
5. `world_logic.py` lines 1902-1907 — surgical removal of stale level-up choices from planning_block (not wholesale drop)

### Merge Strategy
- Merge in order: A → B → C → D (each depends on A)
- All require explicit `MERGE APPROVED` from user
- CI core-mvp-1/2/3 failures are infrastructure flakes (confirmed by agent audit)
- Must get CR APPROVED on each before merge

---

## Related Open PRs (CLEAN — not blocking)
- [#6363](https://github.com/jleechanorg/worldarchitect.ai/pull/6363) fix/atomicity-test-xp-injection — CLEAN
- [#6360](https://github.com/jleechanorg/worldarchitect.ai/pull/6360) feat/rewards-engine-tdd-baseline — CLEAN
- [#6359](https://github.com/jleechanorg/worldarchitect.ai/pull/6359) test/level-up-repros — CLEAN
- [#6355](https://github.com/jleechanorg/worldarchitect.ai/pull/6355) feat/worker-b-level-up-production-fix — CLEAN
- [#6358](https://github.com/jleechanorg/worldarchitect.ai/pull/6358) fix/level-up-rewards-integrated-main — UNSTABLE (superseded by split stack)

## Evidence State
- 6/6 bugs REPRODUCED in /er audits (WARN-FINAL — max achievable for historical captures)
- New campaign Classes F/G from 3 additional repros — WARN-FINAL
- Streaming E2E 2/2 PASS at iteration_012 (commit 12bfbdba5)

## Branch Hygiene Debt
- 15+ stale local branches behind remote (1-200 commits)
- 7 merge conflict pairs among PR heads (#6373 overlaps most)
- Prune stale branches: `fix/widen-state-flag-semantics` (-200), `fix/rewards-box-synthesis-robustness` (-125), etc.

---

_Last updated: 2026-04-18_
