---
title: "PR #6565 — ZFC M0 Stabilization Bridge"
type: source
tags: [zfc, level-up, m0, stabilization, atomic-persistence, streaming, rewards-engine]
date: 2026-04-23
source_file: https://github.com/jleechanorg/worldarchitect.ai/pull/6565
---

## Summary

PR #6565 is the M0 stabilization baseline for the ZFC level-up stack, implementing atomic persistence of level-up rewards, UI reconciliation for the level-up modal, and streaming normalization for the rewards pipeline. It touches 21 files across runtime (`firestore_service.py`, `llm_parser.py`, `main.py`, `rewards_engine.py`, `world_logic.py`), unit/integration tests, and MCP/browser evidence harness. The PR is +3694/-551 LOC.

## Key Claims

- Level-up rewards persistence is now atomic: `rewards_box` and `rewards_pending` are written together in a single Firestore transaction
- Streaming normalization ensures `rewards_box` passes through `normalize_rewards_box_for_ui()` on all code paths including passthrough
- MCP-layer atomicity is proven via `test_level_up_rewards_planning_atomicity.py` evidence bundle (iteration_004)
- Streaming path was NOT exercised in evidence (0 streaming scenarios in `streaming_evidence.json`) — this is a known gap
- CI passes all 24 core checks; Skeptic Gate-1 race condition (CI=pending at scan time)

## Key Quotes

> "This PR is the active M0 stabilization baseline for the ZFC level-up stack"

## Connections

- [[ZFC-Level-Up-Architecture]] — this PR implements the M0 stage of the ZFC architecture where model computes level-up signal and backend formats
- [[RewardsBoxAtomicity]] — core concept: rewards_box and rewards_pending must be atomically persisted
- [[StreamingPassthroughNormalization]] — the passthrough path now calls normalize_rewards_box_for_ui() before persistence
- [[NormalizationAtomicity]] — architectural principle that all persisted data must be canonicalized
- [[ZFCNorthStar]] — PR aligns with north-star: model outputs structured level-up signal, backend is pure formatter
- [[zfc-level-up-pr-tracking]] — tracks this PR in the broader ZFC PR stack (#6565 is lane 0, merge first)

## Files Changed

### Runtime
- `mvp_site/firestore_service.py` — atomic persistence transaction
- `mvp_site/llm_parser.py` — streaming normalization
- `mvp_site/main.py` — state helper integration
- `mvp_site/narrative_response_schema.py` — schema updates
- `mvp_site/rewards_engine.py` — canonicalization on all paths
- `mvp_site/schemas/prompt_tool_contracts.json` — tool contract updates
- `mvp_site/world_logic.py` — level-up signal handling

### Tests
- `mvp_site/tests/test_streaming_orchestrator.py` — 76 passed, 9 skipped
- `mvp_site/tests/test_firestore_mock_mode_persistence.py` — 14 passed
- `mvp_site/tests/test_rewards_engine.py` — rewards engine unit tests
- `testing_mcp/test_level_up_rewards_planning_atomicity.py` — MCP atomicity proof
- `testing_ui/test_level_up_rewards_planning_atomicity_browser.py` — browser evidence

## CI Status (2026-04-23)

| Gate | Status |
|------|--------|
| Gate-1 (CI) | FAIL (race: CI=pending) |
| Gate-2 (Conflicts) | PASS |
| Gate-3 (CodeRabbit) | FAIL (detection lag) |
| Gate-4 (Bugbot) | FAIL (pending) |
| Gate-5 (Comments) | FAIL (2 unresolved) |

## Known Gaps

1. Streaming path not exercised in evidence bundle (0 streaming scenarios)
2. `collection_log.txt` missing from evidence artifacts
3. Gate-5: 2 unresolved review comments need addressing
