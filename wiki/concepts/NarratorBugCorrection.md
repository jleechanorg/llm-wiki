---
title: "Narrator Bug Correction"
type: concept
tags: [llm-dm, platform-pattern, bug-recovery, ux]
sources: [2026-08-04-bg3-voyage-campaign-summary]
last_updated: 2026-08-04
---

# Narrator Bug Correction

Recovery pattern reported in [[2026-08-04-bg3-voyage-campaign-summary]]: when the [[Voyage]] engine produced bugs — leveling-up errors, ability-point mistakes, "weird combat or narrative misses" — the player found them "easily fixable with the narrator," i.e. by asking the DM/narrator layer in-conversation to correct the state.

## Why this matters

- It's a distinctive property of LLM-DM platforms: the narrator doubles as a live GM-override / state-repair channel, so mechanical bugs degrade to minor friction instead of run-enders.
- It shifts the platform-quality bar: engine correctness bugs are tolerable **if** the narrator has authority to repair state; tooling opacity (the [[Worldsmith]] complaint) is not similarly self-healing.
- Related worldarchitect.ai patterns: [[PlayerDirectedExpGrant]] and [[DestinyRulebookOverrides]] are player-directed state mutations through the same conversational channel — the difference is intent (bug repair vs. rule bending), which a platform must distinguish.