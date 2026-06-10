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

## Superset-merge + deflate — byte-identical duplicate streams (2026-06-09)

Third variant: when the overlap is **byte-identical** (same agent's edits
recovered into one PR while the agent opened its own PR of the same content),
neither close-the-subset nor THEIRS-resolution is needed:

1. Prove subset vs divergence first: `git diff brA brB --stat` between the two
   heads — decide from bytes, not PR descriptions.
2. Merge the green superset (`gh pr merge --squash --admin`).
3. In the duplicate's branch, `git merge origin/main --no-edit` — identical
   hunks become no-ops, the merge is conflict-free, and the PR diff deflates
   automatically to its unique contribution (verify via `gh pr view N --json files`).
4. Fix the unique remnant per review, then merge the deflated PR normally.

This keeps the worker's authorship, needs no force-push approval, and skips
rebase conflict churn. **Divergent** (non-identical) overlap is instead the
stacked-PR single-writer stop-the-line case.
Incident: dark-factory PR #40 (`bf694ad`, superset) / PR #41 (`fee8f01`,
deflated to `minimal_research.dot` lane).
Source: [[sources/duplicate-pr-superset-merge-2026-06-09]] · bead jleechan-clh.
