# Competing-PR Canonical-Field Resolution

When two PRs target the same architectural problem with **opposite canonical
field choices** and one merges first, the later PR must:

1. Take THEIRS on every file touching the canonical field (including tests).
2. Identify dead artifacts in the loser-PR (modules with zero callers).
   Decide: delete OR keep as additive scaffolding. Document the choice.
3. Add only **additive** changes on top of THEIRS — never re-write the
   canonical field choice.

Picking OURS on the canonical re-breaks every downstream consumer that
landed in the winner-PR.

## Example
PR #7048 (canonical = `world_data.location` string, via `location_util`
module) raced PR #6896 (canonical = `world_data.current_location_name`,
inline `resolve_location`). #6896 merged first. #7048 took THEIRS on
`agent_prompts.py`, `context_compaction.py`, `llm_parser.py`,
`llm_service.py`, `preventive_guards.py`, `tests/test_preventive_guards.py`;
kept `location_util.py` as additive scaffolding.

## Related
- [[pr7048-location-centralization-merged]]

## Source
- ~/.claude/projects/-Users-jleechan-projects-worktree-location-centralize/memory/feedback_2026-05-24_competing_pr_canonical_field_resolution.md

## Subsumption resolution — close the subset, keep the superset (2026-06-07)

When two competing PRs overlap the same production files and one is a strict
behavioral **superset**, the resolution is **subsumption**, not merge-both: close
the subset PR as subsumed and migrate its unique follow-ups/caveats to a comment
on the superset before closing. Merging the incomplete subset first guarantees
conflicts against the superset on the shared files and can land an inert half-fix
that looks done. Confirm the superset relation by reading the production hunks,
not a raw `gh pr diff | grep` (see [[CodeReviewMethodology]] §Grep-on-PR-diff).
Incident: PR #7330 (tool-attach only, gate never fires) subsumed by PR #7280
(attaches tool + sets `code_execution_used` + new audit module).
Source: [[sources/2026-06-07-competing-pr-subsumption-close-subset]] · bead rev-15x97.
