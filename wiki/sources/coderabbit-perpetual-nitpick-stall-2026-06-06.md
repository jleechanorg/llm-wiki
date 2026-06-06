---
title: "CodeRabbit perpetual-nitpick stall (PR #16) → admin squash-merge"
type: source
date: 2026-06-06
tags: [coderabbit, code-review, pr-merge, dark-factory, admin-merge, 7-green, stall, anti-pattern]
raw: raw/feedback_2026-05-31_pr10_coderabbit_stall.md
bead: jleechan-xpv
---

# CodeRabbit perpetual-nitpick stall on dark-factory PR #16; resolved via admin squash-merge

## Summary

While driving `jleechanorg/dark-factory` PR #16 to merge (2026-06-06), CodeRabbit
exhibited a **second stall flavor**, distinct from the PR #10 COMMENTED-stall.
On PR #16 CodeRabbit **did** re-review every new head (`415c77f`, `dcd5810`) —
so "CR won't re-review" is not universal — but on **every** pass it filed a fresh
`CHANGES_REQUESTED` carrying **new** low-severity nitpicks:

- unused loop variable `label` → `_` (in `tests/test_dynamic_fanout_sweep.py`)
- `_git` fail-fast on non-zero return code (in `benchmarks/workflow_graphgen/harness.py`)
- a `RESULTS.md` typo (`uncounfounded` → `unconfounded`)
- then 9 more nitpicks + re-raised "Duplicate" comments on a later pass

It never auto-dismissed its own change request and never flipped
`reviewDecision` to `APPROVED`, **even with CI green** (skeptic ✓, test ✓) and the
**local suite at 226 passed**. Net: chasing a clean `APPROVED` on this repo is a
treadmill — CodeRabbit generates new nitpicks faster than it clears the old ones.

## The two stall flavors (same repo, no branch protection)

| Stall | Behavior | Pre-condition / trigger | Mitigation |
|-------|----------|--------------------------|------------|
| **COMMENTED-stall** (PR #10) | Won't re-review already-reviewed commits; won't auto-approve | `request_changes_workflow: true` was NOT set before CR's first review | Add root `.coderabbit.yaml` with `request_changes_workflow: true` *before the first PR push* |
| **Perpetual-nitpick treadmill** (PR #16) | Re-reviews each new head but files fresh `CHANGES_REQUESTED` with new nitpicks every pass; never auto-dismisses, never flips to `APPROVED` | none — happens even with CI + local suite green | Admin squash-merge once actionable items + CI + suite are green |

## Resolution rule (covers both)

Once **(a)** every *actionable/substantive* CodeRabbit item is fixed and
individually verified, **(b)** CI is green, and **(c)** the local test suite is
green → **stop chasing APPROVED** and admin squash-merge per **explicit operator
authorization**:

```bash
gh pr merge <N> --admin --squash --delete-branch
```

Do NOT keep pushing nitpick fixes hoping CR will approve. Surface the
stale-review state, offer admin-merge, and only override on the operator's
explicit "merge it."

### Mandatory pre-merge re-check (even when overriding)

```bash
gh pr view <N> --json headRefOid,mergeable,reviewDecision
```

Confirm `mergeable=MERGEABLE` and that local HEAD == remote branch HEAD before
merging (a concurrent push can change the head between the verdict and the merge).
Verify each CR "fix" with a local suite run *before* pushing — PR #16 was **226
passed** at each of `415c77f` and `dcd5810`. No branch protection on dark-factory
(re-confirmed 2026-06-06), so `--admin` works.

## Resolution for PR #16

Fixed all CR actionable items across `415c77f`/`dcd5810` (verified 226 green each
push) → `gh pr merge 16 --admin --squash --delete-branch` → squash commit
`d010cf6` on main (`4b8b921 → d010cf6`); local main synced, branch deleted, suite
226 green on merged main. Merged 2026-06-06T22:30:57Z.

## References

- PR: <https://github.com/jleechanorg/dark-factory/pull/16>
- Merge commit: `d010cf6` (parent `4b8b921`)
- Bead: `jleechan-xpv` (CLOSED)
- Concept: [[CodeRabbitDismissedPattern]] (Stall variants section)
- Related: PR #10 COMMENTED-stall (same memory file), PR #13 NEUTRAL-without-root-`.coderabbit.yaml`

## Does this affect [[jeffrey-oracle]]?

No — this is a technical code-review/process learning, not a fact about Jeffrey.
