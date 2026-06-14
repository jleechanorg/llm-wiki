---
name: competing-pr-subsumption-close-subset-migrate-followups-to-superset
description: "Two open PRs overlapping the same production files, one a strict superset → close the subset as subsumed, migrate its unique follow-ups to a comment on the superset; do NOT merge the subset alone"
metadata:
  node_type: memory
  type: feedback
  bead: rev-15x97
  originSessionId: 6f4e0216-7a79-412a-a259-d6347e84b0d0
---

When two OPEN PRs implement overlapping fixes that touch the **same production files**, and one is a strict superset of the other, do **not** merge the subset PR. Close the subset as **subsumed** and migrate its unique follow-ups to a comment on the superset.

**Concrete decision (2026-06-07):** PR #7330 (`investigate-codeexec-failopen-7262`, 4 files) only did step 1 of the streaming code-execution fix — attach `types.Tool(code_execution={})` — but never set `debug_info["code_execution_used"]`, so the persistence gate (`mvp_site/dice_integrity.py:634`) never fires. PR #7280 (`worktree_dice3854`, 38 files) is a strict superset: attaches the tool **and** sets `code_execution_used` **and** adds the new `mvp_site/dice_code_execution_audit.py`. Both touch `gemini_provider.py` + `test_streaming_orchestrator.py`, so they would textually conflict. Resolution: **close #7330 as subsumed, keep #7280**, and post #7330's carry-over caveats (e.g. confirm `require_total=False` at the dice-audit call site; canonicalizer still requires notation + non-empty `rolls[]` + total) as a follow-up comment on #7280 (#7280 comment 4643996220) so nothing is lost.

**Why:** Merging the incomplete subset first creates guaranteed merge conflicts against the superset on the shared files, duplicates review effort, and can land a half-fix that looks done (tool attached) but is inert (gate never fires). One canonical PR per logical fix keeps the review pipeline and merge graph clean (mirrors the "PR quantity control — iterate, don't proliferate" rule: ≤3 open PRs per scope).

**How to apply:** When you find two open PRs in the same scope: (1) diff their file sets (`gh pr diff <A> --name-only` vs `<B>`) and confirm overlap; (2) determine if one is a strict behavioral superset by reading the production hunks (NOT a raw `gh pr diff | grep` — see [[grep-on-gh-pr-diff-gives-false-positives-beads-jsonl-prose-hunk-isolate-the-source-file]]); (3) close the subset with `gh pr close <subset> --comment "Subsumed by #<superset>: <reason>"`; (4) migrate any unique follow-ups/caveats from the subset to a comment on the superset before closing; (5) never merge the subset alone. Closing/merging stays under the human MERGE-APPROVED gate — closing-as-subsumed is allowed, merging is not.

**References:**
- PR #7330 https://github.com/jleechanorg/worldarchitect.ai/pull/7330 (CLOSED as subsumed, closedAt 2026-06-07T20:22:50Z).
- PR #7280 https://github.com/jleechanorg/worldarchitect.ai/pull/7280 (OPEN, superset) — follow-up comment https://github.com/jleechanorg/worldarchitect.ai/pull/7280#issuecomment-4643996220.
- Gate `mvp_site/dice_integrity.py:634`; producer `mvp_site/llm_providers/gemini_provider.py`; root-cause bead rev-ncugf.
- Related memory: [[grep-on-gh-pr-diff-gives-false-positives-beads-jsonl-prose-hunk-isolate-the-source-file]] (the verification method that confirmed #7330 was the strict subset).
