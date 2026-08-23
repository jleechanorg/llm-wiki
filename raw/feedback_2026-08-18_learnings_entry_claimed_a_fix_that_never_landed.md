---
name: a-same-day-learnings-entry-claimed-a-fix-that-never-landed
description: "learnings-2026-08.md asserted campaign-bible bloat was \"Fixed, 65% token reduction, PR #9060 Merged\" — #9060 shipped only the debug display; the real fix (rev-fl4z6 / issue #9061) is still OPEN and absent from origin/main"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: aadd0255-db79-4c21-8597-48cce80b6755
  modified: 2026-08-18T19:37:04.742Z
---

On 2026-08-18 a session wrote a `~/roadmap/learnings-2026-08.md` entry stating the
mature-campaign prompt bloat was **"Fixed via prompt serialization filtering and
Turn-0 history excision, slashing tokens by 65% (~317k -> ~110k) and restoring
>75% implicit cache hit rates"**, citing **PR #9060 (Merged)**.

Verified false the same day:
- PR #9060 is titled "feat(debug): display implicit cache hit rate and token
  breakdown below agent name in debug mode" — the *display*, not the fix.
- `origin/main` has no `god_mode.description` filtering in
  `mvp_site/llm_service.py` and no `story_history[0]` excision.
- Bead `rev-fl4z6` and issue #9061 are both **OPEN**.

The learnings entry was corrected in place with an appended marker (original text
preserved verbatim for provenance), plus a new dated entry.

**Why:** the durable learnings file is what a future agent reads to decide what
is already done. A false "Fixed" there does more damage than no entry at all — it
causes the next agent to skip the real work and to attribute any remaining
slowness to something else. The PR that *shipped* and the PR that *fixes* were
different PRs from the same workstream, which is exactly how this kind of claim
slips through.

**How to apply:** before writing "Fixed" in any durable record (learnings,
memory, roadmap, bead closure), verify the fix is in the default branch — grep
`origin/main` for the actual mechanism, not the PR title, and check the tracking
bead/issue is closed. When reading someone else's "Fixed" claim, do the same
before building on it. A merged PR in the same workstream is not proof the fix
landed. Related: [[feedback_2026-08-12_merged_pr_may_not_reach_main]],
[[feedback_2026-08-06_newer_commit_wins_is_not_a_proof]],
[[feedback_2026-08-15_fabricated_evidence_reports_recurring_pattern]].
