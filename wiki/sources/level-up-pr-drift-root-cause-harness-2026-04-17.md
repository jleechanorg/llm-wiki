---
title: "Level-Up PR Drift Root Cause and Harness Analysis 2026-04-17"
type: source
tags: [worldarchitect-ai, level-up, rewards-engine, world-logic, harness, pr-drift]
date: 2026-04-17
source_file: raw/level-up-pr-drift-root-cause-harness-2026-04-17.md
sources:
  - level-up-engine-single-responsibility-design-2026-04-14.md
  - level-up-pr6339-verification-status-2026-04-17.md
  - level-up-atomicity-root-cause-2026-04-17.md
last_updated: 2026-04-17
---

## Summary

The non-autor level-up PR line drifted because the v4 centralization plan assumed `world_logic.py` functions could be replaced by similarly named `rewards_engine.py` functions, but a later behavioral audit found the pairs were not equivalent. `rewards_engine.py` handled XP-threshold and causal rewards decisions; `world_logic.py` still handled stateful modal recovery, stale flags, persisted-story projection, and planning-block injection. Later agents therefore fixed failures where they still lived, mostly in `world_logic.py`, while the architecture language still described centralization as the goal.

## Key Claims

- PR https://github.com/jleechanorg/worldarchitect.ai/pull/6273 merged the v4 rewards-engine pipeline foundation.
- PR https://github.com/jleechanorg/worldarchitect.ai/pull/6276 merged a pragmatic Layer 3 cleanup, but not the full "thin modal wrapper only" target.
- The post-merge audit found 0/3 tested `world_logic.py` versus `rewards_engine.py` function pairs behaviorally equivalent.
- PR https://github.com/jleechanorg/worldarchitect.ai/pull/6339 is the best evidence/reference branch for XP-driven atomicity behavior, but it is closed, dirty, CHANGES_REQUESTED, and targets `feat/world-logic-clean-layer3`, so it should not be reopened as-is.
- PR https://github.com/jleechanorg/worldarchitect.ai/pull/6351 is the current main-target port attempt, but it remains blocked by review and should be cleaned or replaced before merge consideration.
- Autor-tagged/titled PRs are ignored for this decision path; they are a separate experiment stream, not the source of truth for the level-up fix line.

## Key Quotes

> "Centralization was gated by structural conformance instead of behavioral equivalence and real stream/non-stream proof."

> "Agents treated the roadmap as a target state and the current code as an implementation detail, instead of reconciling the two through behavioral evidence before changing or reviewing PRs."

## Harness Analysis

Failure class: missing validation plus LLM path error.

### 5 Whys - Technical Failure

1. The PR line drifted because the centralization PR did not fully move behavioral ownership into `rewards_engine.py`; `world_logic.py` still owned stateful recovery behavior.
2. That happened because the design assumed function pairs were equivalent based on names and call shapes.
3. The wrong assumption was not caught before merge because gates checked structural properties, not side-by-side semantic output.
4. Post-merge PRs kept patching `world_logic.py` because the real failures surfaced in modal injection, stale flags, and persisted story projection.
5. The architecture allowed that because ownership was defined aspirationally instead of by enforced behavior contracts and real integration evidence.

Root cause: centralization was gated by structural conformance instead of behavioral equivalence and real stream/non-stream proof.

### 5 Whys - Agent Path

1. Agents did not prevent the drift because they optimized for local PR review comments and nearest failing functions.
2. They reasoned that way because the roadmap said `world_logic.py` should become thin, but the code and tests still made `world_logic.py` the live recovery surface.
3. Instructions did not redirect them because there was no mandatory rule requiring semantic equivalence before replacing or deleting level-up/rewards behavior.
4. Wiki/roadmap did not stop it because they recorded intent and later partial completion, but PR workers did not have a hard preflight binding each fix back to the updated design truth.
5. The harness was incomplete because it had design-doc gates, but not behavior-contract gates or a forced "centralize or explicitly document exception" decision point.

Agent root cause: agents treated the roadmap as target-state truth and the current code as incidental, instead of reconciling the two through behavioral evidence.

## Proposed Harness Fixes

- Instructions: any PR touching `world_logic.py`, `rewards_engine.py`, `llm_parser.py`, or `game_state.py` for level-up work must state module ownership and whether a `world_logic.py` change is a temporary stateful-wrapper exception.
- Skill: update the level-up/code-centralization workflow to require a behavioral-equivalence table before call-site redirects, function deletion, or "logic replaced" claims.
- Tests: add semantic equivalence coverage for pre-level, XP-driven, stale-pending, stuck-completion, loot/gold, and streaming-passthrough states before centralizing or deleting functions.
- CI: design-doc gates should require semantic proof artifacts for PRs claiming centralization completion; grep success alone is insufficient.
- PR workflow: require real-server real-LLM `testing_mcp` strict/stale/streaming evidence before claiming all level-up bugs are fixed.

## Current Recommendation

Do not merge PR https://github.com/jleechanorg/worldarchitect.ai/pull/6351 as-is. Create one clean `origin/main` integration PR that ports the proven XP-driven atomicity behavior from PR https://github.com/jleechanorg/worldarchitect.ai/pull/6339, folds in valid engine-side visibility behavior from PR https://github.com/jleechanorg/worldarchitect.ai/pull/6336, keeps `world_logic.py` recovery logic narrow and explicitly documented, and proves the result with targeted unit tests plus real-server real-LLM `testing_mcp` strict/stale/streaming runs.

## Connections

- [[BehavioralEquivalenceAudit]] - root guardrail that should have blocked the false replacement assumption.
- [[LevelUpCodeArchitecture]] - architecture target and current-vs-target responsibility split.
- [[LevelUpVerificationStatus]] - real-server real-LLM evidence expectations.
- [[PR-6276-Worldarchitect]] - merged partial centralization PR.
- [[PR6339]] - reference branch for XP-driven atomicity evidence.
- [[PR6351]] - current main-target port attempt.
