---
title: "Level-Up Integrated Fix TDD Implementation Plan 2026-04-17"
type: source
tags: [worldarchitect-ai, level-up, tdd, evidence, ao-workers, real-llm, video-evidence]
date: 2026-04-17
source_file: raw/level-up-tdd-implementation-plan-2026-04-17.md
sources:
  - level-up-centralization-learning-2026-04-17.md
  - level-up-pr-drift-root-cause-harness-2026-04-17.md
  - level-up-atomicity-root-cause-2026-04-17.md
  - level-up-engine-single-responsibility-design-2026-04-14.md
last_updated: 2026-04-17
---

## Summary

The integrated level-up fix must be implemented as one clean `origin/main` replacement PR, not by reopening PR https://github.com/jleechanorg/worldarchitect.ai/pull/6339 or merging PR https://github.com/jleechanorg/worldarchitect.ai/pull/6351 as-is. The plan converts the prior learning into a TDD work contract: separate RED test commits, GREEN production-code commits, and evidence-only commits; prove behavior across four layers; and split AO workers by non-overlapping write scopes.

## Key Claims

- The v4 single-responsibility architecture remains the target direction, but `world_logic.py` full stripping was tombstoned as written after behavioral-equivalence failure.
- `world_logic.py` changes are allowed only as narrow modal/state recovery exceptions and must be documented as such.
- Before deleting or redirecting old logic, workers must provide a behavioral-equivalence table across representative states.
- The PR must prove XP-driven threshold crossing, explicit false stale guards, stuck completion synthesis, atomic rewards/planning pairs, stale choice scrubbing, gold/loot/progress-only visibility, malformed rewards normalization, and stream/non-stream persistence parity.
- Tests, code, and evidence must be in separate commits.
- Layer 3 proof requires a real local server and real LLM `testing_mcp` runs with no mock toggles.
- Layer 4 proof requires real browser/UI video evidence for UI claims; screenshots alone are insufficient.

## Worker Split

- Worker A: RED unit/backend tests only.
- Worker B: production fix port only.
- Worker C: Layer 3 real MCP harness and evidence only.
- Worker D: Layer 4 browser/UI video evidence only.
- Worker E: skeptic/drift guard, read-only by default.

## Key Commands

Real server bootstrap:

```bash
cd /Users/jleechan/worldarchitect.ai
env -u MCP_TEST_MODE -u MOCK_SERVICES_MODE -u USE_MOCK_SERVICES \
  TESTING_AUTH_BYPASS=true \
  GOOGLE_APPLICATION_CREDENTIALS=/Users/jleechan/serviceAccountKey.json \
  ./vpython mvp_site/main.py serve
```

Layer 3 canonical runs:

```bash
cd /Users/jleechan/worldarchitect.ai/testing_mcp
../vpython test_levelup_strict_repro.py --server http://127.0.0.1:8001
../vpython test_stale_level_up_pending_repro.py --server http://127.0.0.1:8001
../vpython streaming/test_level_up_streaming_e2e.py --server http://127.0.0.1:8001
```

## Connections

- [[BehavioralEquivalenceAudit]] - required before replacement/deletion claims.
- [[LevelUpVerificationStatus]] - evidence expectations for strict/stale/streaming proof.
- [[LevelUpCodeArchitecture]] - architecture target and responsibility split.
- [[PR6339]] - reference implementation/evidence branch only.
- [[PR6351]] - current WIP port attempt, not merge-ready as-is.
