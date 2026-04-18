---
title: "Central Level-Up / Rewards-Box / Streaming Tracker 2026-04-18"
type: source
tags: [worldarchitect-ai, level-up, rewards-box, streaming, evidence, beads, pr-triage]
date: 2026-04-18
source_file: raw/2026-04-18-level-up-central-tracker.md
sources:
  - level-up-tdd-implementation-plan-2026-04-17.md
  - level-up-centralization-learning-2026-04-17.md
  - level-up-pr-drift-root-cause-harness-2026-04-17.md
  - level-up-atomicity-root-cause-2026-04-17.md
last_updated: 2026-04-18
---

## Summary

This source is the canonical coordination record for the active level-up,
rewards-box, and streaming fix family as of 2026-04-18. It ties the central bead
`rev-7vyc`, active PRs https://github.com/jleechanorg/worldarchitect.ai/pull/6352
through https://github.com/jleechanorg/worldarchitect.ai/pull/6361, the hosted
evidence release plan, local worktree drift, and merge-readiness blockers into
one handoff target.

## Key Claims

- `rev-7vyc` is the single coordination bead for new level-up/rewards-box/streaming handoffs.
- The work is on track for repro coverage and planning, but not merge-ready.
- PR https://github.com/jleechanorg/worldarchitect.ai/pull/6358 remains the strongest implementation candidate unless a later decision explicitly promotes https://github.com/jleechanorg/worldarchitect.ai/pull/6361; it is still blocked by CodeRabbit `CHANGES_REQUESTED`.
- PR https://github.com/jleechanorg/worldarchitect.ai/pull/6361 is a streaming-default process_action and rewards_box canonicalization follow-on, not yet proven as the landing vehicle; it now mixes production rewards changes, `testing_mcp` harness behavior, and Green Gate workflow changes.
- The current checkout has a narrowed `remote.origin.fetch`, so local `origin/*` refs cannot be trusted for broad PR truth.
- `br` was repaired by remapping structural `bd-*` JSON IDs to the configured `rev-*` prefix and rebuilding from `.beads/issues.jsonl`.
- Remaining acceptance requires hosted evidence publication, updated PR evidence links, green CI/review, 7-green log verification, and an explicit landing/supersession decision for PRs #6358 and #6361.

## Drift Assessment

The current work is drifting from the clean single-responsibility design. Both
PR #6358 and PR #6361 move canonical pair resolution back into `world_logic.py`.
That can be legitimate only as a narrow modal/story recovery exception, but the
current patches are broad enough to risk a second rewards engine. PR #6361 also
bundles harness defaults and Green Gate workflow changes with production logic,
which breaks the intended separation between fix, evidence harness, and gate
policy.

## Latest REST Snapshot

- PR https://github.com/jleechanorg/worldarchitect.ai/pull/6358 remote head: `1d1c8824da1d46988845304aaaf27dcb70ec5ec8`; local worktree head: `65a8113b8055bb132f5a9d5355bec1cb46d120d6`.
- PR https://github.com/jleechanorg/worldarchitect.ai/pull/6361 remote head: `bf9be175e80f1529f94de0529610734a14ae8997`; current checkout local head: `03fc62835e99507d5b521917b2108afd963439ea`.
- PR https://github.com/jleechanorg/worldarchitect.ai/pull/6361 remains blocked by CodeRabbit `CHANGES_REQUESTED`; the earlier MCP mock smoke failure no longer appears in current check-runs.
- PR https://github.com/jleechanorg/worldarchitect.ai/pull/6358 has CodeRabbit `CHANGES_REQUESTED` and Cursor Bugbot in progress.

## Key Quotes

- "We are on track at the repro/evidence/planning layer, but not merge-ready."
- "This is now the single coordination bead for the active level-up bug family."
- "For remote truth, use `gh api` or `git ls-remote` until the fetchspec is repaired."

## Connections

- [[LevelUpCentralTracker]] - central coordination concept for this bug family.
- [[LevelUpBugInvestigation]] - historical root-cause and evidence context.
- [[RewardsBoxAtomicity]] - invariant behind badge/choice consistency.
- [[StreamingPassthroughNormalization]] - streaming path normalization issue tied to PR #6361.
- [[MinimalReproLadder]] - repro ladder used to keep evidence grounded.
- [[FrontendRewardsBoxGate]] - browser/UI evidence target for rewards box behavior.
