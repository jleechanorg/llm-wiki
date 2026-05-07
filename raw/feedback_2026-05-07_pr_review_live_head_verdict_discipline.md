---
name: PR review live-head verdict discipline
description: Verify live PR head, evidence SHA, and Skeptic state before accepting pasted review output; separate code blockers from strict green process gaps.
type: feedback
bead: rev-awmxd
---

# PR Review Live-Head Verdict Discipline

During review of https://github.com/jleechanorg/worldarchitect.ai/pull/6818,
the user pasted a handoff claiming the evidence and review blockers were fixed.
The durable lesson is to re-check live GitHub state before answering.

Fresh review showed the PR head had advanced to
`2edcdabe3c7fa975ad69082eda9e988dd36cc533`. The behavioral evidence bundle at
`/tmp/worldarchitect.ai/worktree_core_bugs/character_creation_three_flows/iteration_019/`
was tied to `64d4fa40ab94f96ae2519b5c3ef95bc007559543`, and the delta from
`64d4fa40` to `2edcdabe` touched generated PR design docs only.

The correct verdict was: no serious production-code issue found on live PR head;
remaining items were strict 7-green/process cleanup because Green Gate had
skipped same-SHA Skeptic verdict extraction and the PR body still cited stale
evidence text.

Reusable rule: verify live PR head, evidence bundle `git_head`, post-evidence
runtime deltas, and Green Gate logs before accepting pasted review output.
Separate serious code/product blockers from provenance or gate-status cleanup.

