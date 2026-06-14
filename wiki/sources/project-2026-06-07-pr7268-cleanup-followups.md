---
title: "PR #7268 level-up clean-flags cleanup followups"
type: source
tags: [pr-7268, level-up, followups, clean-flags, worldarchitect-ai]
date: 2026-06-07
source_file: raw/project_2026-06-07_pr7268_cleanup_followups.md
---

## Summary
PR #7268 (level-up clean-flags refactor, branch delete-stale-level-flags, head ddfd4f10). Deletes stale level_up_pending/level_up_in_progress/level_up_complete/level_up_cancelled lifecycle flags; routes modal from derived state (canonical level_up_signal, target_level > current_level). Net production LOC +553 (additive refactor, not pure deletion). CodeRabbit APPROVED (22:38Z), mergeable=MERGEABLE, reviewDecision empty. Remaining hard blocker: 2 Directory tests failing (core-mvp-1/2 self-hosted) → Green Gate (rev-jyeff). 4 queued followup beads: rev-1c98x (HP-alias scope creep), rev-x2sja (level_up_now choice text), rev-15i5c (in-place cleanups), rev-naxbs (Bugbot GameState.__init__ strip).

## Key Claims
- PR #7268 deletes 4 stale lifecycle flags; routes modal from derived state (canonical level_up_signal, target_level > current_level). Net +553 LOC (additive, not pure deletion)
- Status 2026-06-07: CodeRabbit APPROVED (22:38Z), mergeable=MERGEABLE, reviewDecision empty; 2 Directory tests failing (core-mvp-1/2 self-hosted) → Green Gate (rev-jyeff)
- Rewrote PR body template-compliant with per-file Before→Now→Why for all 19 non-test files; net-additions audit = no new boolean lifecycle flags (new level_up_in_progress/level_up_pending are read-only derived @property shims); no tenet violations (XP is display-only hydration, never primary)
- Followup beads: rev-1c98x (HP-alias scope creep, RCF violation, 90 LOC), rev-x2sja (level_up_now text 'Meditate on your Oath' violates 'text must begin with Level Up' rule), rev-15i5c (in-place cleanups), rev-naxbs (Bugbot GameState.__init__ strip level_up_stage/pending_level_up_selections)
- PR #7337 separate: DO NOT MERGE — skeptic VERDICT FAIL on _resolve_level_up_from_rewards_box accepts stale prior-level thresholds

## Connections
- [[project_2026-06-07_pr7268_final_review_4lane_synthesis]]
- [[feedback_2026-06-07_copy_campaign_dest_default_footgun]]
- [[Pr7268]]
