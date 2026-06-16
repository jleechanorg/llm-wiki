---
title: "Drive 2 PRs to /green + merge in 2h (admin override 3rd field instance, post-merge propagation discipline)"
type: source
tags: [pr-merge, admin-override, post-merge-propagation, slack-misroute, learning]
date: 2026-06-16
source_file: project_2026-06-16_drive_to_merge_2h.md
sources:
  - /Users/jleechan/.claude/projects/-Users-jleechan--hermes/memory/project_2026-06-16_drive_to_merge_2h.md
last_updated: 2026-06-16
---

## Summary

On 2026-06-16, two PRs ([#624](https://github.com/jleechanorg/jleechanclaw/pull/624) and [#625](https://github.com/jleechanorg/jleechanclaw/pull/625)) were driven to /green and merged in a single 2-hour window under a user-set `/goal` that explicitly waived the skeptic gate. The admin-override pattern (substance 5/6-green + literal `MERGE APPROVED` from user) was field-proven a 3rd time after CodeRabbit's incremental-review-system bug refused to re-review already-reviewed commits. Post-merge, the propagation sequence (cp CLAUDE.md + re-render plist + launchctl bootstrap/kickstart + re-test) is now the durable shape for any PR touching policy files or launchd templates.

## Key Claims

- Admin override pattern (substance-green + literal `MERGE APPROVED`) is the 3rd-time field-proven resolution for the CodeRabbit incremental-review-system stall (variants 1 + 2 in [[feedback_2026-06-12_coderabbit_dismissed_stuck]]).
- A user-set `/goal` with explicit skeptic waiver is a valid green mode — 6-gate (gates 1-6) + admin override for gate 3 = merge-eligible, no skeptic required.
- The 4-layer 5b-leak defense: 5a code fix (PR #29) + 5b LLM-judgment rule (PR #624) + watchdog channel fix (PR #625) + deploy drift warning (`scripts/deploy.sh` Stage 5.5) + regression test (`test_claudemd_policy_contains_5b.sh`).
- Post-merge propagation MUST be atomic: `cp CLAUDE.md` to prod + re-render installed plists from templates + `launchctl bootstrap + kickstart` + re-run tests. Skipping any step leaves the system in half-fixed state.
- Anti-pattern caught: force-push to clear stale CR review state without explicit in-thread human approval. Even when user has authorized the merge, force-push still needs separate explicit OK.

## Key Quotes

> "After a CodeRabbit CHANGES_REQUESTED → fix → push cycle, CR's formal review object can get stuck at `DISMISSED` and never flip to `APPROVED`... Resolution = admin override merge, but ONLY when ALL hold..."

> "Test PASS in staging does not mean fix is live. Required sequence after PR #624 + #625 merged: cp CLAUDE.md to prod, re-render plist templates, launchctl bootstrap + kickstart, re-run tests post-propagation."

> "Anti-pattern caught: force-push to clear stale review state requires explicit in-thread human approval naming target branch — this was violated once; do not repeat without explicit OK."

## Connections

- [[feedback-2026-06-12-coderabbit-dismissed-stuck]] — The precedent for admin override (variants 1 + 2). This drive is the 3rd field instance.
- [[pr-624-5bcl]] — Sub-class 5b anti-misroute rule in CLAUDE.md (sub-class 5b skill rule layer).
- [[pr-625-ops-chan]] — Umbrella pattern: empty-default `HERMES_OPS_SLACK_CHANNEL` in launchd wrapper + watchdog plist re-render.
- [[pr-29-send-message-tool]] — 5a code-level fix (gateway `send_message_tool.py` thread_ts drop).
- [[umbrella-pattern-empty-default]] — Architectural rule that PR #625 enforces.
- [[DriveToGreen2h]] — Reusable operational pattern for "drive N PRs to green in T hours" goals.
- [[PostMergePropagation]] — Atomic post-merge sequence: cp + re-render + bootstrap + kickstart + re-test.
- [[AdminOverride]] — Substance-green + literal `MERGE APPROVED` resolution for CR-stuck.

## Lessons

1. The 2h drive pattern is reusable: classify each PR up front (lite-green vs 6-gate), set up per-PR worktrees, drive independently, follow admin-override path on CR-stuck, and ALWAYS do the post-merge propagation sequence as a single atomic step.
2. CR-stuck recovery should NOT spend >30min on CR pings before asking the user for `MERGE APPROVED`. The incremental-review-system bug is permanent, not transient.
3. The `MERGE APPROVED` literal phrase is the only valid trigger per `~/.claude/CLAUDE.md` "Merge safety" rule. "Looks good" / "go ahead" / "ship it" / "fine merge it" are NOT merge authorization.
4. Force-push to a PR branch (even to clear stale review state) requires separate explicit OK. "User has authorized the merge" does not extend to "user has authorized force-push."
