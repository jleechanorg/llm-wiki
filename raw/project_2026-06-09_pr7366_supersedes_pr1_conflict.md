---
name: pr-7366-supersedes-pr1-conflict
description: PR
metadata: 
  node_type: memory
  type: project
  originSessionId: 54224e21-8040-4407-a0e1-209703cd5b39
---

# PR #7366 vs PR #7368 (PR 1) — competing level_up_session reducer PRs

**Date**: 2026-06-09
**Status**: OPEN conflict, requires user decision

## The conflict

PR #7366 (head 261b706900, jleechan2015) opened 2026-06-08T19:58Z — "Level-up: add canonical session schema guard"

Touches (overlapping with my PR 1 #7368):
- `mvp_site/level_up_session.py` (+389 lines) — NEW FILE, same path as my PR 1's reducer
- `mvp_site/tests/test_level_up_session.py` (+341 lines) — NEW FILE, same path as my PR 1's test
- `mvp_site/prompts/god_mode_instruction.md` (+32/-13) — both modify
- `mvp_site/schemas/game_state.schema.json` (+132/-7) — adds level_up_session to schema
- `mvp_site/schemas/field_ownership_registry.json` (+52) — new field ownership registry
- `mvp_site/schemas/typed_dicts.py` (+140/-45) — typed dict for level_up_session
- `mvp_site/schemas/field_constants.py` (+24) — field constants
- `mvp_site/tests/test_schema_strictness.py` (+159/-12) — schema strictness tests
- `scripts/check_schema_coverage.py` (+24/-12) — schema coverage script
- `roadmap/level-up-session-state-machine-design-2026-06-08.md` (+410) — the user's design doc
- `roadmap/level-up-session-implementation-roadmap-2026-06-08.md` (+577) — the user's implementation roadmap
- `.github/workflows/presubmit.yml` (+8/-4) — CI gate

PR #7368 (PR 1 of the 6-PR chain, head 95d1a0e29a):
- `mvp_site/level_up_session.py` (12 public reducer functions, all pure, no I/O)
- `mvp_site/tests/test_level_up_session.py` (12-invariants test suite)
- Plus PR 2/3/4/5.5 all depend on PR 1

## Strategic decision required

Per memory `feedback_2026-06-07_competing_pr_subsumption_close_subset.md`:
> "two OPEN PRs overlapping same prod files + one strict superset → CLOSE the subset as subsumed"
> "Migrate unique caveats to a comment on superset, NEVER merge subset alone"

**PR 7366 is the strict superset** (reducer + schema + roadmap + CI gate).
**PR 1 #7368 is the subset** (reducer only).

If we close PR 1, the 6-PR chain (1→2→3→4→5.5→5→6) becomes orphaned because PRs 2-5.5 all depend on PR 1's reducer.

## Why both exist

- PR 7366 was opened 2026-06-08T19:58Z, by jleechan2015
- PR 1 #7368 was opened earlier (head 4dd994597b per memory `project_2026-06-08_level_up_session_pr1to3_shipped.md`)
- The user pivoted from "single mega-PR with schema guard" to "6-PR chain" per memory `project_2026-06-08_level_up_session_state_machine_pivot.md`
- The pivot was documented in the design doc (which is IN PR 7366 — chicken/egg)

**Why**: The user's pivot to 6-PR chain (rev-pctz8.1-6 + 5.5) predates PR 7366, but PR 7366 was opened in parallel and reintroduces the same file. The 6-PR chain's PR 1 was the pivot's foundation, but PR 7366 also claims that foundation + adds schema.

**How to apply**: Do NOT close either PR without user approval. Surface the conflict in the loop's next status report. The realistic resolution paths are:
1. Close PR 1 as subsumed by PR 7366 (clean) but break the chain (PRs 2-5.5 need rebasing onto PR 7366 head)
2. Rebase PR 7366 to base on PR 1's head (preserves the chain) — this is the cleanest path if user wants the 6-PR chain
3. Keep both, deconflict manually (high risk of merge conflicts)
4. Close PR 7366 (preserves chain), keep the schema infra as a separate follow-up PR

The user's "make your own decisions" mandate is for tactical execution, not strategic PR lifecycle. Strategic PR closure = user decision. Pause the chain work for the user's call.

## What I CAN do unblock-decision

- Continue pushing code quality fixes on the chain (PR 2, 3, 4, 5.5) — those don't depend on the PR 1 vs PR 7366 decision
- Continue waiting for the skeptic worker (Gate 7 fleet-wide down)
- Wait for the user's decision on PR 1 vs PR 7366

## What I should NOT do unblock-decision

- Close PR 1 or PR 7366
- Force-push any branch
- Open a new PR that re-derives either side
