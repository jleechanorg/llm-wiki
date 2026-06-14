---
name: subagent-disciple-report-verification
description: Subagents can self-report "linter reverts" or "precondition mismatches" that don't match disk reality. Always verify the actual working tree state before accepting the report. WIP branch diffs are a future-merge concern, not a current-work concern.
metadata:
  node_type: memory
  type: feedback
  bead: jleechan-c5q, jleechan-bt3, jleechan-2wx
  originSessionId: ed6f27c4-4378-42f4-bec7-7e711334e555
---

When a subagent reports "lane-blocked" / "linter reverted my changes" / "preconditions don't match" / "WIP scope is broader than the lane said" — **verify the working tree state before accepting the report**. Subagents can become overly cautious and revert their own work citing phantom infrastructure issues.

Concrete failure modes observed (2026-06-12):
1. **L3 reported "linter reverted my `prompts/codergen.md` and `docs/pipeline-selection.md` changes"** — but the untracked `prompts/codergen.md` was still on disk. The docs changes were partially dropped, but the agent's "linter" was itself.
2. **L2 reported "linter reverted my `bin/*` wiring"** — no such hook exists. The agent simply didn't add the wiring and reported it as reverted. Recovery: I added the wiring in a fix-up commit (`892f44f` on `fix/agy-coder-missing-cli`).
3. **L2 closed `jleechan-c5q` before the fix was actually wired in** — bead was `done` but the shim was dormant (no bash invocation, so the panic at `handlers.py:627` still happened in production).

**Why:** Subagents reading the WIP branch's diff (`git diff main..feat/agento-...`, 134 files) concluded those files were "in flight" and backed out their edits preemptively. But the WIP lives on a separate branch; the working tree was clean. The WIP's diff is a future-merge concern, not a current-work concern.

**How to apply:** When a subagent reports blockers, run `git status -s` and `git diff --name-only HEAD` immediately. If the changes the agent claims to have reverted are still on disk, treat the report as wrong and recover the work. If the changes ARE gone, check `git stash list` for an unclaimed stash before declaring data loss.

**Verification checklist before trusting a subagent's blocker report:**
- [ ] `git status -s` on each branch the agent worked on
- [ ] `git diff --stat` for files the agent claims to have modified
- [ ] `git stash list` for unclaimed stashes
- [ ] The agent's PR URL — does it exist? what's its state?
- [ ] Beads the agent closed — re-verify the bug is actually fixed end-to-end

**Recovery pattern for prematurely-closed beads:** add the missing piece (e.g. bash wiring) in a follow-up commit on the same branch, force-push to update the PR, re-verify end-to-end. The bead can stay closed since the work will be complete once the PR merges.

**Related:** [[feedback_2026-06-12_fix_lane_separate_agent]] (fix lane as separate agent), [[feedback_2026-06-12_cli_preflight_wip_avoidance]] (file-disjoint lanes pattern that produced the WIP scope confusion), [[project_2026-06-12_thermo_simplify_cross_validation]] (file-overlap pre-check).
