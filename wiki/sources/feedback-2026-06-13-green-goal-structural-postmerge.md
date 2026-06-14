---
title: "green-goal-structural-postmerge (2026-06-13)"
type: source
tags: [feedback, merge-train, /green, override, postmerge]
date: 2026-06-13
source_file: raw/feedback_2026-06-13_green_goal_structural_postmerge.md
---

## Summary
A Stop hook goal like "/green them all and merge when safe" is structurally unsatisfiable for PRs that the user has already merged via "override safety" — the override authorizes the merge but cannot retroactively satisfy the pre-merge /green gate. The override is a one-way door: closing the loop requires reverting merges and re-establishing green, not post-merge verification.

## Key Claims
- `/green` is a **pre-merge gate**: it operates on `mergeable=true` + `reviewDecision=APPROVED` + Skeptic PASS on the current head SHA. None of these are computable on an already-merged PR.
- Override-authorized merges: `mergeable` becomes `UNKNOWN` (GitHub stops computing it) and `reviewDecision` was never set if no human ever approved.
- A "merge done" report must disclose that the /green clause is unmet and unrecoverable post-merge.
- This rule exists because on 2026-06-13 in the merge_train session, 4 PRs (#29, #30, #31, #32) were merged via override; the assistant's final report acknowledged /green was unmet, and Stop hook feedback correctly flagged that "merge done" != "goal met".

## Key Quotes
> The override authorizes the merge despite 7-green not being met. It does NOT (and CANNOT) make /green retroactively satisfied.

> If the user wants the goal truly met, the path is: revert merges → re-establish green on each PR head → re-merge when 7-green. The override is a one-way door; closing the loop requires undoing it.

## Connections
- [[GreenGateWorkflow]] — pre-merge 7-green gate that becomes unsatisfiable after override merge
- [[AdminOverrideContract]] — override mechanics and the "what the override does NOT cover" rule
- [[PostMergeDuplicatePRLoop]] — post-merge follow-up patterns that apply when an override-merges PR
- [[AOSkepticGateOps]] — Skeptic Gate verification that stops being computable on merged PRs
- [[over-correction-guard]] — explicit overrides are binding but do not extend to clauses the user did not address
