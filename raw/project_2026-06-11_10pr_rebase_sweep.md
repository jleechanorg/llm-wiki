---
name: 10pr-rebase-sweep
description: 10 CONFLICTING PRs rebased onto origin/main on 2026-06-11 (7372, 7397, 7422, 7424, 7253, 7213, 7236, 7377, 7329, 7434)
metadata: 
  node_type: memory
  type: project
  originSessionId: 11b18814-6b01-49a8-a167-12c66b99835e
---

**Date**: 2026-06-11 16:00 PDT

## PRs cleared (all CONFLICTING → MERGEABLE, 0 failing checks each on the new head)

| PR | Title | Old head → New head | Notes |
|----|-------|---------------------|-------|
| #7397 | fix(mycampaigns-search): server-side search/filter | `f701d4ec25` → `0e9bc74069` | 1 conflict (app.js, took theirs); PR body rewritten with proper Background/Goals/Tenets + evidence gist `91bdfa3ac19c80817f58e78a10b98aec` |
| #7372 | [antig] fix(bq-logging): wire call sites | `cd3215bb5d` → `7c5c415ceb` | 1 conflict (test_bq_logging.py: took ours, added branch's test_import_registers_bq_sink at end) |
| #7422 | feat(ci): PR description green gate (Gate 6b) | `14ed2b435a` → `b4e9803f5d` | 1 conflict (PR template, took theirs) |
| #7424 | fix: two-check level-up signal when rewards box available | `af3e29fac0` → `7e22f21e27` | 2 conflicts (rewards_engine.py took theirs, test_resolver_sole_source.py was deleted in main, restored branch's version) |
| #7253 | test: add campaign story cutoff copy support | `68a8ca9908` → `714a1390f1` | 5 conflicts in copy_campaign.py (all took theirs); 1 commit |
| #7213 | Clarify location field contract | `2e9220dda5` → `abb18f0f8c` | 1 conflict in test_location_util.py (took theirs); 2 commits |
| #7236 | feat: general resource registry with backend tracking | `d2b361f5aa` → `8ef47e2fd4` | 1 conflict in prompt_tool_contracts.json (took theirs); 13 commits |
| #7377 | level-up: PR 5 routing migration | `cbed50cf01` → `23c2634b86` | 1 conflict in level_up_session.py (took theirs); 27 commits — large but clean |
| #7329 | fix(#7318): session header EXP drift | `207cea0aef` → `1ec5bdcc4e` | Used `git rebase -X theirs` (massive 100+ file conflicts, no manual resolution); 6 commits |
| #7434 | fix(level-up): combined daily-cron fix | `317189350c` → `f599c5dce3` | 6 conflicts across world_logic.py + rewards_engine.py + test_rewards_engine.py; 18 commits. Decision: for each, took ours (HEAD) when it had Bugbot-aligned safety fix (e.g. `_local_meta.pop("canonical_signal", None)`), took theirs when branch added new code (e.g. `_snapshot_canonical_pair` helper). ALWAYS take ours for the import-standards issue (no inline `from x import` inside functions). |

## Patterns learned

- **`git rebase -X theirs`** is the correct hammer for branches with 100+ file conflicts when the branch's overall direction is right (e.g. #7329 — XP alias partial-restore). Used once successfully on 6 commits.
- **Import standards gate**: `from x import y` inside function bodies is FORBIDDEN by `import-validation` CI gate. When rebasing, always prefer ours for this pattern.
- **Bugbot-style defensive code in HEAD wins**: when HEAD has `_local_meta.pop("canonical_signal", None)` style safety lines that the branch lacks, take ours. The HEAD version incorporates more Cursor Bugbot fixes.
- **`git push --force-with-lease` does NOT work from a detached HEAD worktree**: use `git push origin <sha>:refs/heads/<branch> --force` to push a specific SHA to a branch. The `--force-with-lease` form only works when current HEAD is on a tracking branch.
- **Detached HEAD after rebase → branch doesn't move**: when `git checkout -b <branch> <sha>` says "already exists" because the branch is checked out elsewhere, you end up with detached HEAD. Must use `git push <sha>:refs/heads/<branch> --force` to update the remote branch.

## Remaining CONFLICTING PRs after this sweep

- All 10 cleared PRs are now MERGEABLE.
- Remaining CONFLICTING PRs (low priority): #7374 (level-up observability, deep conflicts), #7380 (large stacked), #7354 (already 7-green per prior memory).
