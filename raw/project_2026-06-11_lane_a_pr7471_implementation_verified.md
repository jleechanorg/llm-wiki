---
name: project-2026-06-11-lane-a-pr7471-implementation-verified
description: Lane A /api/constants/models public opt-in implementation verified — PR
metadata: 
  node_type: memory
  type: project
  originSessionId: 7363e54e-ee90-4c19-98d8-cc18d403051b
---

The lane-A worktree `/Users/jleechan/projects/worktree_auth_clear_fix7465` (branch `fix/constants-fetchapi-public`, HEAD `1cccf3fc59`) is **fully implemented** as of 2026-06-11 23:13Z and the deliverable is **PR #7471** (OPEN, MERGEABLE, base=main, head=fix/constants-fetchapi-public, exact title + body per the plan).

**8 commits ahead of main** (97e9148662 → 1cccf3fc59):
1. `97e9148662` — fix(constants): make /api/constants/models public via fetchApi {public: true} opt-in
2. `8b3222c45d` — fix(api): skip 401-retry on public requests
3. `cf1b3b2caa` — test(constants): pin 4-key response contract
4. `c50bbff57c` — test(constants): pin 401-retry gating + single call site
5. `2c036ab59f` — test(constants): link evidence gist from test docstring
6. `2c8ef4ada8` — fix(api): strip public flag from fetch init to align code with plan invariant
7. `4f9338eeaa` — chore(constants): no-op to refresh Green Gate (PR #7471 head 2c8ef4ada87)
8. `596b648d6c` + `1cccf3fc59` — docs(constants): refresh evidence pointer to 7/7 GREEN at current head

**Files changed (284 +, 29 -):**
- `mvp_site/frontend_v1/api.js` — `fetchApi` reads `options.public === true`; gates the auth-required block on `!isTestMode && !isPublicRequest`; skips Bearer header construction; gates 401-retry on `!isPublicRequest`; destructures `public` to `_strippedPublic` so it does NOT spread into the outgoing fetch init
- `mvp_site/frontend_v1/app.js:4022` — `loadModelConstants()` is the **only** call site passing `{ method: 'GET', public: true }`
- `mvp_site/main.py:4506-4507` — `@check_token` removed from `/api/constants/models`; only `@app.route` + `@limiter.limit` remain; 4-key static response unchanged
- `mvp_site/tests/test_model_constants_endpoint_public.py` — 7 RED→GREEN tests (all passing locally)

**Why:** re-implementing the lane would re-do work that is already done and contaminate the PR with redundant commits. When a fresh session picks up "implement Lane A" via `.dark-factory/plan_a.md`, the correct action is to **verify state** (tests + diff + PR + CI) — not to redo the TDD cycle. The plan's status note says "POST-FIX on the lane worktree."

**How to apply:** when asked to "implement" this lane, first run `cd <worktree> && python -m pytest mvp_site/tests/test_model_constants_endpoint_public.py -v` to confirm 7/7 GREEN, then `gh pr view 7471` to confirm the PR is OPEN with the right title/body, then `gh pr checks 7471` to check CI status. Skip the "RED test first" step because the test file is already on disk and the 4 backend behavioral tests pin the original 6/6-FAIL → 6/6-PASS transition on the pre-fix `c96eeb7846` parent. Any new task against this lane is about post-merge follow-up (CodeRabbit review of new commits, or human MERGE APPROVED), not re-implementation. **Do NOT push fresh commits just to satisfy a "commit + push" template** — see also [[feedback-2026-06-11-fix-a-no-review-issue-state]] for the no-op rule.

**Status as of 2026-06-11 21:30Z:** 22/24 CI checks SUCCESS, 1 transient FAILURE (self-hosted core-tests gitconfig auth-placeholder error at 20:59:58Z — checkout-time infra issue, not a test failure; per [[feedback-2026-06-10-green-gate-first-run-after-push-false-negative]] the Green Gate first-run-after-push is unreliable), 1 QUEUED (Green Gate re-run from 21:24:49Z waiting on self-hosted runner). Earlier Green Gate from 19:49:23Z was SUCCESS per [[project-2026-06-11-lane-a-pr7471-evidence-fix]].

Related: [[project-2026-06-11-lane-a-pr7471-evidence-fix]], [[feedback-2026-06-11-fix-a-no-review-issue-state]], [[feedback-2026-06-11-pr7440-iphone-dev-unauth-drop-cdiag-proof]]
