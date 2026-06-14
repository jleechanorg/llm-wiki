---
title: "Feedback 2026 06 11 Cr Incremental After Mention Takes 15Min"
type: source
tags: [memory, ao-worker, codex-worker, 2026-06]
date: 2026-06-11
source_file: .claude/projects/-Users-jleechan-projects-worldarchitect-ai/memory/feedback_2026-06-11_cr_incremental_after_mention_takes_15min.md
---

## Summary

When CodeRabbit has a stale `CHANGES_REQUESTED` on an old SHA and the head has moved, the only ways to get a fresh review are:
1. Push a new commit to trigger `coderabbit-ping-on-push.yml` (auto)
2. Post a comment with `@coderabbitai` mention (manual)
3.

## Original

# CodeRabbit incremental review after @-mention ping takes 5-15 minutes

When CodeRabbit has a stale `CHANGES_REQUESTED` on an old SHA and the head has moved, the only ways to get a fresh review are:
1. Push a new commit to trigger `coderabbit-ping-on-push.yml` (auto)
2. Post a comment with `@coderabbitai` mention (manual)
3. Post a comment with `@coderabbitai review` (explicit command)

After the trigger fires, CR's full incremental review takes **5-15 minutes** to land. During that time the PR is still `mergeStateStatus: BLOCKED` (stale review on old SHA) but the Skeptic verdict stays PASS (gate-3 filters by head SHA).

## Observed timing on PR #7439 (2026-06-11)
- 04:07:43Z — push to e1f527422b triggers `coderabbit-ping-on-push.yml` (success at 04:07:52Z)
- 04:25:10Z — `@coderabbitai` mention posted
- 04:31:12Z — CR auto-reply "Full review triggered" posted (this is NOT the review, just the trigger ack)
- 04:40:55Z — CR incremental review lands (state=CHANGES_REQUESTED on e1f527422b, 34083 chars, 12 actionable items)

Total wall clock from push to fresh review: 33 minutes (5 min ping + 15 min wait + 13 min incremental).

## What "incremental review" finds
CR reviews against the **diff between PR base and current head**, not just the latest commit. So a fix commit can introduce NEW issues that weren't in the prior review. On PR #7439 e1f527422b:
- 3 new Major: cache-hit logged as live cost (corrupts BQ), missing `raw_request_payload` in stream no-op
- 1 Critical: `llm_parser.py` still missing `finally` block (out of diff range comment — applied to a file CR couldn't see in this PR's diff but the file exists in the repo)
- 1 Minor: openclaw_provider.py return type concern

## Skeptic / Green Gate vs stale CR review
- Skeptic Gate 3 filters by head SHA → PASSES even with stale CR review on old SHA
- Green Gate Gate 7 (Skeptic) also PASSES
- BUT `mergeStateStatus: BLOCKED` stays until fresh CR review lands on the current head
- The Skeptic verdict body explicitly marks Gate 3 as "PASS(status-only)" when no fresh CR review exists

## How to plan
When you know a CR review will need to clear a stale CHANGES_REQUESTED, budget **15+ minutes** of wall clock between the trigger and the fresh review landing. Don't treat the auto-reply "Full review triggered" as the review — it's just the ack. The actual review arrives 5-15 min later.

**Why**: A 33-min cycle (push → ack → review) caught me off-guard at the end of a 2h budget; I would have started the next fix cycle earlier if I'd known the wall clock.
**How to apply**: When the stop condition depends on `mergeStateStatus: CLEAN`, after pushing the fix: (1) wait for `coderabbit-ping-on-push.yml` success, (2) wait for CR auto-reply "Full review triggered", (3) poll for the actual review state change for up to 15 min, (4) do NOT trust Skeptic PASS as a substitute for a fresh CR review.
