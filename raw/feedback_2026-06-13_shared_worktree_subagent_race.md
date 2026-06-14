---
name: shared-worktree subagent race
description: Parallel subagents in the same git worktree see each other's untracked files. Run the suite per-branch in isolation before admin-merging; trust `git diff main..branch --stat` over `gh pr diff --name-only` for scope verification.
metadata:
  node_type: memory
  type: feedback
  bead: jleechan-cv3, jleechan-g06, jleechan-ua8
  originSessionId: ed6f27c4-4378-42f4-bec7-7e711334e555
---

When 3+ subagents run concurrently from the same git worktree (the dark-factory default), they share untracked files and each other's in-progress branches. This causes two failure modes:

**Failure mode 1 — suite count bleed-through.** Subagent A writes `tests/test_X.py` to the worktree. Subagent B (in parallel, same worktree) runs pytest, which picks up `tests/test_X.py` as an untracked file in its collection. B's reported suite count is inflated by A's tests. Example: Lane A reported "398 passed" but the real delta was 15+3 = 18, with the +1 being overlap from Lane B's `tests/test_perf_log_path_drift.py` being collected in Lane A's run. Lane A's 15 tests were correct; the 1 extra was bleed-through.

**Failure mode 2 — phantom files in PR diff.** `gh pr diff <N> --name-only` shows files that exist in the worktree but were never in the actual commit. PRs #53 and #55 had `roadmap/README.md` listed as a "changed file" because the PR base was `85d50e7` (stale) and main had advanced to `bffac64` (the roadmap record commit). The 3-way merge produces a phantom file in the API view that doesn't exist in the actual branch head's commit. Confirm with `git show <head_sha> --stat` — if the phantom isn't in the actual commit, it's a stale-base display artifact, not scope creep.

**Discipline fix (apply BEFORE admin-merging):**

```bash
# Per-branch isolation suite run:
git stash --include-untracked
git checkout <branch>
# Run pytest with --ignore for tests owned by other concurrent lanes
.venv/bin/python -m pytest tests/ -q --ignore=tests/test_other_lane.py
git checkout main
git stash pop
```

**Scope check (apply BEFORE admin-merging):**

```bash
# Use this, NOT `gh pr diff --name-only`:
git diff --name-only main..<branch>
# AND verify the actual commit:
git show <head_sha> --stat
```

**Why:** On 2026-06-13, 3 subagents fanned out in parallel all hit this. Lane A's "398 passed" was an honest report (its tests passed) but the count was inflated by Lane B's untracked file. The phantom `roadmap/README.md` in PR #53 and #55 was a 3-way merge display issue that could have been misread as scope creep. Recovery: per-branch isolation suite run + `git show <head_sha> --stat` confirmed all 3 PRs were clean before admin-merge.

**How to apply:** Any time ≥2 subagents are dispatched in parallel from a single worktree (typical for `/claw`-style fanout), add the isolation-suite and `git show` checks to the verification protocol. For a single-subagent dispatch, the issue doesn't apply.
