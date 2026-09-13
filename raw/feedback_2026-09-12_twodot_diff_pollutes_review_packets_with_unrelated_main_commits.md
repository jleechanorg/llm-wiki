---
name: twodot-diff-pollutes-review-packets-with-unrelated-main-commits
description: "git diff origin/main <branch> (two-dot) silently pulls in unrelated commits that landed on main after the branch forked, producing a false blocking finding in external review"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: db345e42-7a34-4442-abdf-1b7c95eca3ab
  modified: 2026-09-13T02:42:24.396Z
---

Building a review packet for PR #9846 with `git diff origin/main docs/rtk-truncation-research-20260911` (two-dot) showed `mvp_site/llm_service.py`, `mvp_site/tests/test_provider_tool_requests.py`, and `mvp_site/faction/tools.py` as changed — none of which the PR actually touched. An external Gemini `/web-advice` review, given that polluted packet, correctly and reasonably returned `VERDICT: CHANGES REQUESTED`, citing a deleted function (`should_single_infer_faction_tools`) as an undisclosed application-code change.

**Root cause:** two-dot `git diff A B` shows every difference between the two tips, including commits that landed on `A` (main) after `B` (the feature branch) forked from it — they appear as reversed/phantom "deletions" in the PR's diff even though the PR's own branch never touched them. The correct comparison is the three-dot form or an explicit merge-base diff: `git diff $(git merge-base origin/main <branch>) <branch>`.

**Verification:** re-ran with the merge-base diff — output shrank from 6 files/290+229 lines to the true 3 files/254 insertions (the actual PR content: one research doc, one roadmap activity file, one README line). Gemini approved on the corrected packet.

**Why:** the diff-truncation bug tracked in [[rtk-diff-truncation]] (bead rev-mdl72) means `gh pr diff` output can't be trusted at face value either, so it's tempting to build packets from raw `git diff` directly — but the *comparison base*, not just the truncation, needs to be right.

**How to apply:** always compute `MB=$(/usr/bin/git merge-base origin/main <branch>)` and diff against `$MB`, never against `origin/main`/`main` directly, when building any review packet, evidence bundle, or /wa attachment for a PR whose base may have moved since the branch forked — which is any long-lived branch. A reviewer (human or model) flagging unrelated code in your diff is itself a signal to re-check the diff's base before assuming the PR is broken.
