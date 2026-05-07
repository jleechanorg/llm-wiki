# Nextsteps — Stale rewards_box xp_gained divergence — 2026-04-30

## Table of contents

- [Executive summary](#executive-summary)
- [Context](#context)
- [Bead index](#bead-index)
- [Work queue](#work-queue)
- [PR / merge state](#pr--merge-state)
- [Learnings pointer](#learnings-pointer)
- [Roadmap pointer](#roadmap-pointer)

## Executive summary

- **Outcomes:** Bug reproduced and root cause identified. `xp_gained=2300` stale in Firestore `structured_fields`, acknowledged by LLM in prose but never cleared because LLM narrative ≠ Firestore write.
- **Risks / blockers:** `br` database is broken (PRIMARY KEY constraint); GitHub issue [#6732](https://github.com/jleechanorg/worldarchitect.ai/issues/6732) created as bead proxy. Root cause investigation in progress via subagent.
- **Next:** Root cause investigation → fix design → PR
- **Beads:** [#6732](https://github.com/jleechanorg/worldarchitect.ai/issues/6732) — stale rewards_box xp_gained divergence

## Context

Repro session for campaign `7IobpFpcOcibSyJ1pI5h` (Frieren v1). User reported stale rewards box showing `+2300 XP` that doesn't dismiss. Copied twin campaigns to jleechantest (`0wf6sCREyLcgynidU5LjyZEfm7D2`) for investigation:
- **Test subject:** `vPZUnBAKMDsbN3HS95wF` (repro-stale-rewards-box)
- **Baseline:** `dUzgmHXlWOeFsOfaz9Ei` (repro-baseline read-only)

**Root cause confirmed:** `_canonicalize_core` in `rewards_engine.py` (line 1481-1538) has no dismissal guard for stale non-level-up `xp_gained`. When a user takes a subsequent turn without a new XP award, the stale `xp_gained=2300` from the previous turn is picked up from `updated_game_state_dict["rewards_box"]` (line 1486-1488), normalized unchanged (line 1517), and written back to Firestore (line 7348 of world_logic.py). The LLM's narrative acknowledgment ("State Cleanup: Deleted...") is prose only — it does NOT write to Firestore.

**Not caused by PR #6719**: PR #6719's guard only handles `level_up_available` flag, not `xp_gained`.

**Missing guard**: `_canonicalize_core` has a SIM102 block (lines 1499-1506) that clears stale `level_up_available` but no equivalent for stale `xp_gained`. The XP-progress rewards box (xp_gained > 0 without level-up) has no dismissal mechanism — it persists until a new XP award overwrites it or a level-up occurs.

## Bead index

| Bead | Title | Link |
|------|-------|------|
| #6732 | Stale rewards_box xp_gained persists despite LLM acknowledgment | [jleechanorg/worldarchitect.ai#6732](https://github.com/jleechanorg/worldarchitect.ai/issues/6732) |

## Work queue

1. ~~**Root cause deep-dive**~~ — ✅ **COMPLETE**. Confirmed: `_canonicalize_core` (rewards_engine.py:1481-1538) has no dismissal guard for stale non-level-up `xp_gained`. Stale `xp_gained=2300` persists via game state merge at line 1486-1488, normalized unchanged, and written back to Firestore every turn. — tracks [#6732](https://github.com/jleechanorg/worldarchitect.ai/issues/6732)
2. **Fix design + implementation** — Add dismissal guard to `_canonicalize_core`: when no new XP award is present on a subsequent turn, clear `xp_gained` from the merged rewards_box. TBD specifics: determine whether dismissal should be automatic (always clear xp_gained when no new award) or conditional (require explicit acceptance signal). — tracks [#6732](https://github.com/jleechanorg/worldarchitect.ai/issues/6732)

## PR / merge state

No PRs open for this bug yet.

## Learnings pointer

- `~/roadmap/learnings-2026-04.md` — section `2026-04-30 — Stale rewards_box xp_gained persists after LLM acknowledgment`

## Roadmap pointer

- Updated `roadmap/README.md` — Recent activity (rolling)
