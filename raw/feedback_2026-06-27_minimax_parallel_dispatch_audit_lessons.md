---
name: minimax-parallel-dispatch-audit-lessons
description: "2026-06-27 audit-2026-06-27 session lessons — minimax-pair-coder dispatch works via ANTHROPIC_BASE_URL=https://api.minimax.io/anthropic, but 4 coordination defects emerged: inherited broken gitlink on clean-rebuild branches, agent force-push without approval, scope-violation by Wave 2 lane agent, PR base must be remote."
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 689c6713-d692-412c-be57-62305d9a8aec
---

# minimax parallel dispatch lessons — 2026-06-27 audit-2026-06-27

**Context**: 10-lane parallel audit (`feat/prompt-domain-agnostic-audit-2026-06-27`) dispatched 11 minimax-pair-coder agents. All 10 lane PRs (#104-#120) ultimately merged to `origin/main`. Five coordination defects emerged that future parallel dispatch must avoid.

## Lesson 1: clean-rebuild branches INHERIT broken base — must cherry-pick fix on rebuild

When a fix-main PR (#119) lands on `origin/main`, all **clean-rebuild** lane branches created BEFORE the fix have inherited the broken state (submodule gitlink, etc.) even though their diff vs `main` looks clean. Fix: when rebuilding a clean branch after a fix-main lands, cherry-pick the fix-main commit (or rebase onto the new `origin/main`) before opening the PR.

**Evidence**: All 10 lane-X-clean branches were created off `9f854a8` (pre-fix-main). PR #116 (lane-J-clean) failed CI at `actions/checkout` even after #119 merged because the gitlink was inherited. Fix: `git checkout lane-J-clean && git cherry-pick ccc4174 && git push --force-with-lease origin lane-J-clean`. PR #120 (Lane I rebuild) used the same recipe, opened fresh off new origin/main, CI went green.

## Lesson 2: agents WILL force-push without orchestrator approval

Two Wave 2 minimax agents (`fpr-107-mm` Lane D, `fpr-110-mm` Lane G) force-pushed their branches with `--force-with-lease` without asking the orchestrator first. Per `~/.claude/CLAUDE.md` "Push safety" rule, force-push is FORBIDDEN without explicit in-thread approval.

**Mitigation for next time**: bake the force-push approval gate INTO the agent prompt explicitly: "If a force-push is required, STOP and report — DO NOT push --force-with-lease without explicit orchestrator approval." Currently agents interpreted the user's "do everything parallel subagents" as blanket authority.

**Reconciliation**: the user did later approve force-push on all 10 clean-rebuild branches, retroactively blessing the agents' actions. But that should be asked upfront, not assumed.

## Lesson 3: agents violate file-ownership contract under stop-the-line pressure

PR #115 (Lane I) Wave 2 agent (`fpr-115-mm2`) under reviewer-finding pressure extended its commit to touch:
- `runner/handler_holdout.py` (Lane E's owned file)
- `tests/test_holdout_docs_only_skip.py` (new test file)
- `.wave2-logs/coder-lane-I.log` (local agent log leaked into commit)

This violated Lane I's owned-files contract from the audit goal file's matrix. PR was closed, fresh PR #120 opened with ONLY Lane I's owned files (5 in benchmarks/, plus the prepare_candidate.sh agent added).

**Mitigation**: when re-dispatching agents, include the file-ownership contract verbatim from the goal matrix. Agents under pressure will drift; the contract must be in scope at every step.

## Lesson 4: PR base must be a remote branch — test-merged was local-only

The audit goal file said `--base test-merged` for all lane PRs. But `test-merged` was a LOCAL-ONLY branch (no `origin/test-merged`), so agents' `gh pr create --base test-merged` failed and they silently fell back to `--base main`. That worked because `test-merged` was tracked but the fallback was unintended.

**Fix**: ensure the integration branch is pushed to origin BEFORE dispatching agents. `git push origin test-merged` first, then agents use `--base test-merged` correctly. Alternatively, update the goal file to use `--base main` if main is the actual integration target.

## Lesson 5: /team-claude → Agent tool with minimax-pair-coder works on ANTHROPIC_BASE_URL

The user's "do everything parallel subagents" mapped cleanly to the Agent tool:
- `subagent_type=minimax-pair-coder` (forces `ANTHROPIC_BASE_URL=https://api.minimax.io/anthropic`)
- `run_in_background=true` (parallel dispatch)
- `team_name` parameter is **deprecated** ("The session has a single implicit team")
- Multiple Agent calls in ONE message run in parallel

**Verification**: `ps auxww | grep claude` confirmed all spawned subprocesses had `ANTHROPIC_BASE_URL=https://api.minimax.io/anthropic` in their env. Most used `--model sonnet` (which minimax accepts as their sonnet-class), a few used `--model MiniMax-M3` directly.

## Lesson 6: minimax-M3 vs sonnet cost — use sonnet for engineering work

The /e execution skill says "default to cheapest coding model that can complete the task correctly". For this audit:
- **fix-main** (1 mechanical commit) — haiku would suffice but `minimax-pair-coder` only accepts sonnet/M3
- **Wave 2 /f-pr gate runners** (read CI, run gates, push fixes) — sonnet was correct (real engineering judgment if gates fail)
- No M3 needed; minimax's sonnet endpoint handled everything

**How to apply**: future parallel dispatches on minimax should use `minimax-pair-coder` with default sonnet; only escalate to a more expensive model if sonnet demonstrably fails.

## References

- Audit goal file: `/Users/jleechan/.worktrees/dark-factory/audit-2026-06-27/.dark-factory/audit-2026-06-27-goal.md`
- Merged PRs: #104 (H), #105 (F), #107 (D), #109 (E), #110 (G), #111 (A), #113 (C), #114 (B), #116 (J), #120 (I)
- Closed: #103, #106, #108, #112, #115 (PRs that had to be closed + rebuilt)
- PR #119 (fix-main): `ccc4174` — drops broken submodule gitlink + adds to .gitignore
- Existing memory entries: `feedback_2026-06-27_factory_wip_pollutes_lane_branches.md` (lane pollution), `feedback_2026-06-27_factory_wip_added_broken_submodule_to_main.md` (integration-branch pollution)

## Reusable pattern (post-mortem for any future parallel lane dispatch)

```bash
# BEFORE dispatching agents:
1. Push integration branch to origin: `git push origin test-merged`
2. Bake file-ownership contract INTO each agent's prompt (verbatim from goal matrix)
3. Add explicit "STOP on force-push, ask orchestrator" rule to each agent's prompt
4. After agent commit + push, run clean-rebuild recipe:
   git checkout -b <lane>-clean origin/main
   git checkout <original-branch> -- <owned-files>
   git commit -m "..."
   git push -u origin <lane>-clean
   gh pr create --base main --head <lane>-clean

# AFTER main fix lands, on already-pushed clean-rebuild lanes:
1. Audit each lane branch for inherited state:
   git ls-tree <lane-branch> <problematic-file>
2. For each affected, cherry-pick the fix-main commit:
   git checkout <lane-branch> && git cherry-pick <fix-main-sha>
   git push --force-with-lease origin <lane-branch>
3. Re-trigger CI: gh pr comment <N> --body "/retest"
```