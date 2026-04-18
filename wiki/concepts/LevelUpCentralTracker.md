---
title: "LevelUpCentralTracker"
type: concept
tags: [worldarchitect-ai, level-up, rewards-box, streaming, evidence, beads, pr-triage]
sources: [2026-04-18-level-up-central-tracker]
last_updated: 2026-04-18
---

## Summary

`LevelUpCentralTracker` is the coordination rule for the April 2026
level-up/rewards-box/streaming fix family: new work should point at bead
`rev-7vyc` and the central roadmap source instead of creating another
branch-local handoff.

## Current Landing Rule

PR https://github.com/jleechanorg/worldarchitect.ai/pull/6358 is the preferred
implementation vehicle unless an explicit newer decision promotes
https://github.com/jleechanorg/worldarchitect.ai/pull/6361 or another successor.
Evidence PRs remain useful, but they should feed the selected implementation
track instead of becoming competing landing targets.

## Operational Notes

- The central roadmap source lives at `/Users/jleechan/roadmap/2026-04-18-level-up-central-tracker.md`.
- The wiki source page is `sources/2026-04-18-level-up-central-tracker.md`.
- The canonical bead is `rev-7vyc`.
- Do not trust stale local `origin/*` refs in `/Users/jleechan/worldarchitect.ai` until `remote.origin.fetch` is repaired.
- Merge readiness still requires CI, review, hosted evidence links, and 7-green gate-log verification.

## Connections

- [[RewardsBoxAtomicity]] - rewards_box and planning_block must stay consistent.
- [[StreamingPassthroughNormalization]] - streaming canonicalization must not bypass normalization.
- [[LevelUpBugInvestigation]] - broader history of level-up regressions and root causes.
- [[MinimalReproLadder]] - evidence structure for keeping fixes testable.
