---
name: feedback-2026-06-13-claw-pre-dispatch-pr-open-check
description: "Before any /claw \"drive PR"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 33b6218a-1fc0-42b9-b4f8-1814474904eb
---

# /claw dispatch gotcha — pre-dispatch PR-open check

**Date:** 2026-06-13
**Context:** I dispatched a /claw task to "drive [#7200](https://github.com/jleechanorg/worldarchitect.ai/pull/7200) to 7-green" for the per-agent system-instruction ratchet work. The user (jleechan2015) had **already closed #7200 at 08:47Z** (3 hours before my dispatch) and superseded it with [#7518](https://github.com/jleechanorg/worldarchitect.ai/pull/7518) — a clean rebase (4 files / +301/-6) onto origin/main. The closure comment said: *"The old branch's Green Gate kept CANCELLED without ever posting a Skeptic verdict, so a clean rebase was the only path forward."* I did not catch this; my dispatch was based on stale state. The user had to surface the closed-PR with "make sure those PRs are still open."

**Lesson:** before any /claw dispatch that names a PR number, re-verify in the same turn:
1. `gh pr view <N> --json state` — must be OPEN
2. `gh pr list --state all --search "<scope> in:title"` — check for superseder/successor PRs the user may have created
3. If user mentioned "cleaner rebase" / "I closed X" / "rebased" in any recent thread — look for the new PR

**What to do if PR is closed:**
- DO NOT silently re-target to the new PR without confirming with the user. The rebase may have changed scope, removed files, or split the work.
- Surface: "PR #N was closed at <time>. Closest open PR: #M (<title>). Pivot Hermes to #M, or wait for your call?" Then post the pivot in the existing thread.
- The dispatch thread is durable; just post a new message with the redirect. Hermes will see it in context and switch.

**Why this matters:** the "drive to 7-green" task assumes a live PR. If the PR is closed, Hermes will:
- Try to push to a deleted head ref → fail
- Try to read reviews on a closed PR → "no reviews found" (confusing)
- Possibly create a NEW PR duplicating the work
- Burn ~5 min of Hermes time + token budget before realizing

**What I did right:** I posted the pivot in the same Slack thread (parent_ts `1781339993.457279`, pivot msg `1781345649879199`) so Hermes has the redirect in context, not a new dispatch.

**Related:** [[feedback-2026-06-13-claw-slack-dispatch]] — the /claw Slack dispatch architecture this builds on.
