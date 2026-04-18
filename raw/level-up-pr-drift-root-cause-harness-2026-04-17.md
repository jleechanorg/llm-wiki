# Level-Up PR Drift Root Cause and Harness Analysis 2026-04-17

This note captures what happened across the non-autor WorldArchitect.AI level-up PR line after the v4 rewards-engine centralization plan. It compares the original roadmap design, merged/open PR state, sparse agent history, and the current active PR line.

## Summary

The original centralization plan was sound as a target, but it assumed old `world_logic.py` behavior could be replaced by `rewards_engine.py` behavior mechanically. That assumption failed. The post-merge behavioral audit found that the claimed replacement functions were not equivalent, so later agents patched the failing live surfaces in `world_logic.py` while still trying to describe the work as centralization.

The current forward path is not to reopen PR #6339 as-is and not to blindly merge PR #6351. The correct path is one clean origin/main integration PR that ports proven XP-driven atomicity behavior, keeps necessary stateful modal recovery narrow, and proves the result with real-server real-LLM `testing_mcp` strict/stale/streaming tests.

## Non-Autor PR Timeline

- PR #6273: Merged the first v4 `rewards_engine.py` single-responsibility pipeline.
- PR #6275: Merged stuck-completion rewards_box synthesis.
- PR #6276: Merged "Layer 3 CLEAN" but explicitly achieved only pragmatic cleanup, not the full thin-wrapper target.
- PR #6336: Open, CHANGES_REQUESTED; useful engine-side ideas for gold/loot/stale cleanup, but not merge-ready.
- PR #6339: Closed, CHANGES_REQUESTED, dirty, and based on `feat/world-logic-clean-layer3`; best reference/evidence for XP-driven atomicity but not suitable to reopen as-is.
- PR #6351: Open current port attempt against main; still blocked by review, contaminated with helper work, and should be cleaned/replaced before merge consideration.
- PR #6277: Open schema groundwork; low risk and useful, but not sufficient to fix behavior.

## Root Cause

The root cause was a false equivalence claim: the v4 design treated `world_logic.py` wrappers as removable once `rewards_engine.py` had similarly named functions, but those functions did not implement the same stateful behavior.

`rewards_engine.py` was mostly XP-threshold and causal. `world_logic.py` still contained flag-driven recovery, stale-modal cleanup, planning-block injection, stuck-completion fallback, and persisted-story projection behavior. When agents saw bugs in the live path, they fixed `world_logic.py` because that was where the missing behavior still lived.

## Harness Analysis

Failure class: missing validation plus LLM path error.

### 5 Whys - Technical Failure

1. Why did the PR line drift? The centralization PR did not fully move behavioral ownership into `rewards_engine.py`; `world_logic.py` still owned stateful recovery behavior.
2. Why did that happen? The design assumed function pairs were equivalent because names and call shapes looked close.
3. Why was the wrong assumption not caught before merge? The gate was mostly structural: imports, grep counts, call-site counts, and CI status. It did not require side-by-side semantic output checks.
4. Why did post-merge PRs keep patching `world_logic.py`? The real failures surfaced in modal injection, stale flags, and persisted story projection, where no engine equivalent existed.
5. Why did the architecture allow that? Ownership was defined aspirationally instead of by enforced behavior contracts and real integration evidence.

Root cause: centralization was gated by structural conformance instead of behavioral equivalence and real stream/non-stream proof.

### 5 Whys - Agent Path

1. Why did agents not prevent the drift? They optimized for the local PR under review and the nearest failing function.
2. Why did they reason that way? The roadmap said `world_logic.py` should become thin, but the code and tests still made `world_logic.py` the live recovery surface.
3. Why did instructions not redirect them? There was no mandatory rule requiring "prove semantic equivalence before replacing or deleting a rewards/level-up function."
4. Why did wiki/roadmap not stop it? They recorded the intended architecture, then later recorded partial completion, but PR workers did not have a hard preflight tying every fix back to the updated design truth.
5. Why was the harness incomplete? It had design-doc gates, but not behavior-contract gates or a forced "centralize or explicitly document exception" decision point.

Agent root cause: agents treated the roadmap as a target state and the current code as an implementation detail, instead of reconciling the two through behavioral evidence before changing or reviewing PRs.

## Harness Fixes Proposed

1. Instructions: add a level-up/rewards centralization rule that any PR touching `world_logic.py`, `rewards_engine.py`, `llm_parser.py`, or `game_state.py` must state which module owns each behavior and whether the change is a temporary stateful-wrapper exception.
2. Skill: update the level-up/code-centralization workflow to require a behavioral-equivalence table before call-site redirects, function deletion, or claims that old logic is replaced.
3. Tests: add a small semantic equivalence suite that runs representative pre-level, XP-driven, stale-pending, stuck-completion, loot/gold, and streaming-passthrough states through old/new candidate functions before migration.
4. CI: design-doc gates should read semantic proof artifacts or fail closed for PRs claiming centralization completion. Grep success alone is insufficient.
5. PR workflow: require real-server real-LLM `testing_mcp` strict/stale/streaming evidence for any level-up PR before "fixes all bugs" claims.

## Current Recommendation

Do not merge PR #6351 as-is. Make one clean origin/main integration PR that:

- ports the proven XP-driven atomicity fix from PR #6339;
- fixes or folds in the valid engine-side visibility behavior from PR #6336;
- keeps `world_logic.py` recovery logic narrow and explicitly marked as modal/state recovery;
- avoids autor recreation branches as inputs for this decision;
- proves behavior with targeted units plus real-server real-LLM `testing_mcp` strict, stale-pending, and streaming tests.

## Links

- https://github.com/jleechanorg/worldarchitect.ai/pull/6273
- https://github.com/jleechanorg/worldarchitect.ai/pull/6275
- https://github.com/jleechanorg/worldarchitect.ai/pull/6276
- https://github.com/jleechanorg/worldarchitect.ai/pull/6336
- https://github.com/jleechanorg/worldarchitect.ai/pull/6339
- https://github.com/jleechanorg/worldarchitect.ai/pull/6351
- https://github.com/jleechanorg/worldarchitect.ai/pull/6277
