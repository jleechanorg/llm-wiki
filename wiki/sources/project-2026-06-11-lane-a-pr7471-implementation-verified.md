---
title: "Lane A PR 7471 implementation verified (2026-06-11)"
type: source
tags: [pr-7471, lane-a, worktree, api-constants, public-opt-in, verification]
date: 2026-06-11
source_file: /Users/jleechan/.claude/projects/-Users-jleechan-projects-worldarchitect-ai/memory/project_2026-06-11_lane_a_pr7471_implementation_verified.md
---

## Summary
The lane-A worktree `/Users/jleechan/projects/worktree_auth_clear_fix7465` (branch `fix/constants-fetchapi-public`, HEAD `1cccf3fc59`) is **fully implemented** as of 2026-06-11 23:13Z; deliverable is PR #7471 (OPEN, MERGEABLE, base=main, head=fix/constants-fetchapi-public, 8 commits ahead of main). 284+ lines / 29- across 4 files implementing the `/api/constants/models` public opt-in via `fetchApi {public: true}`. When a fresh session picks up "implement Lane A" via `.dark-factory/plan_a.md`, the correct action is to **verify state** (tests + diff + PR + CI) — not to redo the TDD cycle.

## Key Claims
- Files changed: `mvp_site/frontend_v1/api.js` — `fetchApi` reads `options.public === true`, gates auth-required block on `!isTestMode && !isPublicRequest`, skips Bearer header, gates 401-retry on `!isPublicRequest`, destructures `public` to `_strippedPublic` so it does not spread into outgoing fetch init.
- `mvp_site/frontend_v1/app.js:4022` — `loadModelConstants()` is the **only** call site passing `{ method: 'GET', public: true }`.
- `mvp_site/main.py:4506-4507` — `@check_token` removed from `/api/constants/models`; only `@app.route` + `@limiter.limit` remain; 4-key static response unchanged.
- `mvp_site/tests/test_model_constants_endpoint_public.py` — 7 RED→GREEN tests (all passing locally).
- 8-commit chain: `97e9148662` (make public) → `8b3222c45d` (skip 401-retry) → `cf1b3b2caa` (4-key contract) → `c50bbff57c` (401-retry gating + single call site) → `2c036ab59f` (link evidence gist) → `2c8ef4ada8` (strip public flag) → `4f9338eeaa` (no-op) → `596b648d6c` + `1cccf3fc59` (refresh evidence pointer).
- Status 2026-06-11 21:30Z: 22/24 CI SUCCESS, 1 transient FAILURE (self-hosted core-tests gitconfig auth-placeholder error at 20:59:58Z — checkout-time infra issue, not a test failure), 1 QUEUED (Green Gate re-run from 21:24:49Z waiting on self-hosted runner). Earlier Green Gate from 19:49:23Z was SUCCESS.
- Operational rule: do NOT push fresh commits just to satisfy a "commit + push" template — see [[feedback-2026-06-11-fix-a-no-review-issue-state]] for the no-op rule.

## Key Quotes
> "When a fresh session picks up 'implement Lane A' via `.dark-factory/plan_a.md`, the correct action is to **verify state** (tests + diff + PR + CI) — not to redo the TDD cycle." — protocol

> "The plan's status note says 'POST-FIX on the lane worktree.'" — lane state

## Connections
- [[PR7471]] — driving PR
- [[WorktreeWorkflow]] — lane-A worktree pattern (`worktree_auth_clear_fix7465`)
- [[FetchApiPublicOptIn]] — the architectural pattern being introduced
- [[LaneAConstantsFix]] — lane-A state
- [[GreenGateFirstRunFalseNegative]] — why the 20:59:58Z transient FAILURE is non-blocking
- [[NoOpRefreshSweep]] — cross-cutting sweep that touches the same PR
