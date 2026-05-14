---
title: "Pre-Modal State Gap in rewards_box Postcondition Enforcement"
type: source
tags: [worldarchitect-ai, rewards-box, level-up, test-coverage, harness, pre-modal]
raw: raw/feedback-2026-05-13-postcondition-pre-modal-state-gap.md
date: 2026-05-13
bead: rev-cl195
---

## Summary

`_enforce_primary_rewards_box_postcondition` tests with `rewards_pending.level_up_available=True`
must cover all three modal states. The pre-modal state (all flags=None) was the missing gap
that allowed a stale-suppression regression to ship and burn `rewards_box=null` into the story
entry for campaign iDDyaHbevKSqQHoMUHnu turn 8.

## Modal State Test Matrix

| State | `level_up_pending` | `level_up_in_progress` | Must synthesize? |
|-------|--------------------|------------------------|-----------------|
| pre-modal | None | None | YES |
| active-modal | True | True | YES |
| post-modal/stale | False | False | Only if XP above threshold |

## Concepts

- [[RewardsBoxAtomicity]] — extended with pre-modal gap note
- [[ZFCLevelingRoadmap]] — modal state matrix added to SKILL.md

## References

- Commit: `f289b8782fb2393ee11847db4b9dbf956aeaa39d`
- PR: https://github.com/jleechanorg/worldarchitect.ai/pull/6908
- Bug campaign: iDDyaHbevKSqQHoMUHnu
