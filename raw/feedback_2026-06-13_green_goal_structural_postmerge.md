---
name: green-goal-structural-postmerge
description: "User \"override safety and merge anyway\" merges the PRs but does NOT satisfy a \"/green them all and merge when safe\" goal — /green is a pre-merge gate and is structurally unsatisfiable for already-merged PRs."
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 4de5b569-b51b-4a12-9a41-45eee5ee760f
---

When a Stop hook goal is "/green them all and merge when safe" and the user explicitly says "merge Skeptic-FAIL PRs anyway (override safety)":

- The override authorizes the merge despite 7-green not being met
- It does NOT (and CANNOT) make /green retroactively satisfied
- For merged PRs: `mergeable` becomes `UNKNOWN` (GitHub stops computing it) and `reviewDecision` was never set if no human ever approved
- A "merge done" report is therefore honest about the merge but MUST disclose that the /green clause is unmet
- A future "I'll run /green now" attempt on already-merged PRs is structurally impossible — the gate is pre-merge only

**Why**: 2026-06-13 merge_train session — 4 PRs (#29, #30, #31, #32) merged via override; assistant's final report acknowledged /green was unmet; Stop hook feedback correctly flagged that "merge done" ≠ "goal met."

**How to apply**:
- When the user picks "override safety" in a `/green`-gated workflow, state upfront: "this will merge without 7-green; the /green clause will remain unmet and unrecoverable post-merge."
- Do not promise or attempt a post-merge /green verification as a path to goal completion.
- If the user wants the goal truly met, the path is: revert merges → re-establish green on each PR head → re-merge when 7-green. The override is a one-way door; closing the loop requires undoing it.
- See also [[over-correction-guard]] — explicit overrides are binding, but do not extend to clauses the user did not address.
