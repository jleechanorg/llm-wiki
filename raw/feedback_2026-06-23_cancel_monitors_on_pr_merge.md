---
name: cancel-monitors-on-pr-merge
description: Cancel all active CI/smoke/Skeptic monitors immediately when user confirms PR is merged; they become stale noise generators
type: feedback
bead: none
---

When the user confirms a PR is merged, immediately stop all active monitors related to that PR's CI/smoke/Skeptic/Green Gate sequence. Stale monitors continue polling and dispatching workflows (e.g., Skeptic on a merged branch) that are harmless but wasteful and generate notification noise.

**Why:** PR #7802 session had 5+ active monitors still running after the user said "i merged this PR". They continued polling for ~20+ minutes, dispatching a redundant Skeptic run, and generating dozens of empty notifications.

**How to apply:**
- When user says "I merged" / "it's merged" / confirms merge: immediately call `TaskStop` for each active monitor task ID before proceeding with `/integrate` or `/learn`.
- Pattern: `TaskStop(task_id)` for each monitor in the session.
- If TaskStop API fails (wrong param), note the IDs and inform user they can be ignored (they'll timeout).

**References:**
- PR #7802 session 2026-06-23; monitors bvpnn4hzd, bfizasthb, b0p9ct86a, byu4t7go3, bao07agl6 all ran stale after merge confirmation
