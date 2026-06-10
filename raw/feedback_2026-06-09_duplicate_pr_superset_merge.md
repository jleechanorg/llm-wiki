---
name: duplicate-pr-superset-merge
description: "When an agent's WIP was recovered into one PR and the agent later opens its own PR of the same edits, merge the green superset first, then merge main into the duplicate so identical hunks fall away — reducing it to its unique contribution."
metadata: 
  node_type: memory
  type: feedback
  bead: see below (dark-factory learning bead)
  originSessionId: 3841c15c-39a4-4af3-bca9-6c051dff9052
---

# Duplicate PR resolution — merge superset, then deflate the duplicate

**Context (2026-06-09, jleechanorg/dark-factory):** An Antigravity worker's
uncommitted working-tree edits were recovered into
[PR #40](https://github.com/jleechanorg/dark-factory/pull/40)
(`feat/add-pr-holdout-research`). The same worker then committed its own copy of
those edits and opened [PR #41](https://github.com/jleechanorg/dark-factory/pull/41)
(`feat/pr-holdout-and-research`) — a duplicate work stream: 3 of #41's 4 files
were a strict subset of #40 (byte-identical `research.md`, subset hunks in
`minimal_pr.dot` / `test_slim.py`); only `minimal_research.dot` + its test were
unique.

**Resolution pattern that worked:**

1. Review and rank: identify which PR is the superset and further along
   (#40: green, APPROVED, research wired + docs). Post the overlap analysis as
   a PR review comment naming the shared files (single-writer evidence table).
2. Merge the superset first (`gh pr merge 40 --squash --admin` → `bf694ad`).
3. In the duplicate's branch, `git merge origin/main --no-edit`. Because the
   duplicated content was byte-identical, the merge was conflict-free and the
   shared hunks became no-ops — the PR diff deflated to only its unique files
   automatically (verified via `gh pr view 41 --json files`).
4. Apply the review fixes to the unique remnant in one commit (drop unrouted
   `class=` attr, strip `//` headers from the markdown prompt, register the
   lane in docs + skill short names), then merge (`fee8f01`).

**Why:** Rewriting/force-pushing the duplicate branch would have required
force-push approval and discarded the worker's authorship trail; rebasing
invites conflict churn. A plain merge-from-main exploits identical content to
do the subtraction for free, no force-push needed.

**How to apply:** Whenever two open PRs share files (single-writer violation),
diff the branches directly (`git diff brA brB --stat`) to prove subset vs
divergence *before* deciding. Byte-identical overlap → merge superset, then
merge main into the duplicate. Divergent overlap → that's the
[[stacked-pr-single-writer]] stop-the-line case instead.

Related: ownership handoff — once the superset merged, the duplicate PR became
the legitimate owner of follow-up cleanups to the shared file (the `//` header
strip in `research.md` moved from a "#40 nit" to a #41 deliverable).

**Provenance:** PRs #40 (`bf694ad`) / #41 (`fee8f01`) on jleechanorg/dark-factory,
2026-06-09; suite 315/315 on merged main.
