---
name: level-up-chain-worked-on-wrong-base-2026-06-09
description: Built 4 chain PRs on parallel worktree branches forked from PR 1 base, not from the user's review branch (PR #7366 base). The local 6-unpushed-commits line and the 2-unpulled-commits remote line are divergent, neither is a superset. Force-push either direction destroys unique work.
metadata:
  type: project
  originSessionId: 54224e21-8040-4407-a0e1-209703cd5b39
---

# Lesson: chain PRs branched from PR 1 base, not from user's review branch

**Date**: 2026-06-09
**Status**: OPEN; user-gated decision required

## What I did

Built a 14-fn reducer (`mvp_site/level_up_session.py`, 40/40 tests pass) plus PR 2 fail-closed (`52fa2278d7`) plus a partial PR 3 `canonicalize_rewards` graft in `rewards_engine.py` (`8f6986019e`). Pushed 4 PRs on parallel worktree branches:
- #7374 (PR 5.5) on `feature/level-up-session-pr5-5` @ 55782df35b
- #7376 (PR 4) on `feature/level-up-session-pr4` @ 0a3390d098
- #7377 (PR 5) on `feature/level-up-session-pr5` @ ecf279618b (rebased onto PR 5.5)
- #7378 (PR 6 v2) on `feature/level-up-session-pr6-r2` @ dc632f8f0c

## What went wrong

All 4 PRs branched from `codex-pr-7268-sync` / `codex-pr-7374` style forks (PR 1 / PR 5.5 base), NOT from `fix/level-up-session-reducer` (PR #7366 base). The 6 unpushed commits on `fix/level-up-session-reducer` are a different line from the 2 unpulled commits on `origin/fix/level-up-session-reducer` (PR #7366). Force-pushing either direction destroys unique work:
- Push local over #7366: loses schema ownership registry + CI gate + god-mode prompt + in-repo docs
- Push #7366 over local: loses the 14-fn reducer depth + PR 2 fail-closed + PR 3 graft

The user reviewed `fix/level-up-session-reducer` (this worktree) and concluded "sounds like you got nothing done" — because from their branch's perspective, the reducer is a well-tested island wired into exactly one call site (`rewards_engine.canonicalize_rewards`), and `agents.py` / `world_logic.py` / `llm_parser.py` / `game_state.py` are unchanged on the main branch the user reviews.

## What I should have done

The moment I sat in `worktree_lvl_clean_flags` on `fix/level-up-session-reducer`, I should have surfaced the divergence as the lead item. The chain work I was pushing on parallel worktrees was real but did not reconcile with the canonical branch the user is auditing.

**Why**: Pushing "completed" PRs onto diverged lines is performative progress. The user sees `6 unpushed / 2 unpulled / diverged` on their review branch and correctly infers the chain is unresolved.

**How to apply**:
- Before spawning /f teammates or writing chain code, run `git -C <worktree> log --oneline origin/<branch>..HEAD` and `git -C <worktree> log --oneline HEAD..origin/<branch>` from the worktree where the user will review.
- If the worktree's branch has diverged from `origin/<branch>`, treat that as the lead blocker, not as a side note.
- If chain work needs to be pushed on parallel worktree branches (PR 4/5/5.5/6 each on its own branch), make sure those branches are reachable from the user's review branch via cherry-pick or merge, not just from PR 1's base.
- Document which base each chain PR branched from, in the nextsteps doc and the bead, so the user can reconstruct the topology.
