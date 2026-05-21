---
name: skeptic-cron-deployed-hermes-agent
description: "Skeptic-cron.yml deployed to hermes-agent; auto-merge verified on PR #11; SKEPTIC_NO_VERDICT auto-posts verdict"
metadata:
  type: project
  bead: none
  originSessionId: 3dc1a846-12b5-462e-80b4-5f73dfdf1172
---

Skeptic-cron.yml and green-gate.yml deployed to `jleechanorg/hermes-agent` and verified operational. PR #11 auto-merged by skeptic-cron at 00:23 UTC with VERDICT: PASS comment posted.

**Why:** Needed automated 7-green merge gate for hermes-agent PRs matching the AO core merge-gate.js logic.

**How to apply:**
- Skeptic-cron runs every 30 min on self-hosted runners (`SELF_HOSTED_RUNNER_LABELS` var)
- When `SKEPTIC_NO_VERDICT` (no prior VERDICT comment exists), skeptic-cron IS the skeptic — evaluates gates 1-6, posts VERDICT: PASS, and merges in same run
- Gate 1 is repo-agnostic: excludes "Green Gate", "Skeptic Gate", "Staging Canary Gate" by name; evaluates ALL other check-runs
- Gate 3 has CR incremental stall fallback: matches verdict comment patterns ("AUTOMATION COMPLETE.*READY FOR MERGE|FINAL VERDICT.*APPROVE|Comments resolved and changes approved")
- Gate 4 Bugbot: only counts cursor[bot] HIGH/CRITICAL severity where `original_commit_id` matches PR head SHA or is null
- Stale cursor[bot] in_progress (>15min) treated as neutral in Gate 1

**GitHub mergeable field:** Can be empty string (not just null) when queried too soon after PR creation. Gate 2 treats empty/null/UNKNOWN as non-passing. Resolves on subsequent cron runs.

**Deployed workflow IDs:** Green Gate: 277040104, Skeptic Cron: 277039266
