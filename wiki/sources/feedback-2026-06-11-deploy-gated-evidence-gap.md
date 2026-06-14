---
title: "Deploy gated evidence gap (2026-06-11)"
type: source
tags: [evidence-gap, deploy-gated, organic-traffic, is_test_user, bq, pr-description]
date: 2026-06-11
source_file: /Users/jleechan/.claude/projects/-Users-jleechan-projects-worldarchitect-ai/memory/feedback_2026-06-11_deploy_gated_evidence_gap.md
---

## Summary
When the user conditions "real user BQ results" on merge+deploy+organic traffic, the 2-hour autonomous iteration budget cannot close that gap. A test driver that bypasses `is_test_user()` with a fixed 28-char Firebase-UID-shaped user_id produces a structural `is_test=false` BQ row from local worktree code, but it is NOT organic real-user proof because (1) deployed code != PR head, (2) synthetic user_id is structural, not organic, (3) only merge+deploy+observed-traffic is organic. The bead must be marked `BLOCKED ON DEPLOY`, not closed. The user is the only merge authority; do not call `gh pr merge`.

## Key Claims
- Closing a deploy-gated evidence bead with a structural BQ row + honest disclosure does NOT satisfy "everything is proven per /es and /er with real user BQ results." The stop hook caught this twice.
- Three reasons a structural BQ row is not organic proof: deployed code != PR head (Cloud Run runs e.g. `c96eeb7`, not the PR head), synthetic user_id is structural (the `is_test_user(user_id)` predicate on a fixed string), only merge+deploy+observed-traffic is organic.
- The only path to a 100%-organic real-user BQ row is human "MERGE APPROVED" + Cloud Run auto-deploy + at least one real Firebase UID hitting the fixed path post-deploy.
- The user is the only merge authority. `gh pr merge` must not be called by an agent. The gap closes when they merge and the next organic row lands.

## Key Quotes
> "A test driver that bypasses `is_test_user()` with a fixed 28-char Firebase-UID-shaped user_id produces a structural `is_test=false` BQ row from the LOCAL worktree code, but this is NOT organic real-user proof" — pattern

> "I closed `rev-jmv1r` 'evidence gap closed' with structural BQ row + honest disclosure, but the user's 2-hour budget condition 'everything is proven per /es and /er with real user BQ results' was NOT met. Stop hook feedback caught this twice. I re-opened the bead as `BLOCKED ON DEPLOY`" — lesson

> "The user is the only merge authority. Do not call `gh pr merge`. The gap closes when they merge and the next organic row lands." — protocol

## Connections
- [[EvidenceStandards]] — the /es and /er gates being satisfied
- [[IsTestUserPredicate]] — the predicate being bypassed
- [[BQForensicLogging]] — the BQ table that holds the rows
- [[CloudRunDeployment]] — the deploy step that closes the gap
- [[MergeAuthority]] — the user is the only merge authority
- [[StopHookFeedback]] — the safety net that caught the false-close
