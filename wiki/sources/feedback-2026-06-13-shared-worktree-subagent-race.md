---
title: "Shared worktree subagent race: suite bleed + phantom PR diffs (2026-06-13)"
type: source
tags: [subagent, worktree, pytest, scope-verification, parallel-fanout, phantom-files, dark-factory]
date: 2026-06-13
source_file: raw/feedback_2026-06-13_shared_worktree_subagent_race.md
---

## Summary
When 3+ subagents run concurrently from the same git worktree (dark-factory default), they share untracked files and each other's in-progress branches, causing two failure modes: (1) pytest count bleed-through — subagent B picks up subagent A's untracked test file in its collection, inflating reported counts; (2) phantom files in PR diff from stale base SHA, where `gh pr diff <N> --name-only` lists files that exist in the worktree but were never in the actual commit.

## Key Claims
- Failure mode 1 (suite count bleed): Lane A reported "398 passed" but the real delta was 15+3 = 18, with +1 from Lane B's `tests/test_perf_log_path_drift.py` being collected in Lane A's run
- Failure mode 2 (phantom PR diff): PRs #53 and #55 had `roadmap/README.md` listed as "changed" because PR base was `85d50e7` (stale) and main had advanced to `bffac64` — 3-way merge display artifact
- Use `git diff --name-only main..<branch>` NOT `gh pr diff --name-only`; verify with `git show <head_sha> --stat`
- Per-branch isolation suite run: `git stash --include-untracked && git checkout <branch> && pytest --ignore=tests/test_other_lane.py`

## Key Quotes
> "Lane A reported '398 passed' but the real delta was 15+3 = 18, with the +1 being overlap from Lane B's `tests/test_perf_log_path_drift.py` being collected in Lane A's run."

> "Use this, NOT `gh pr diff --name-only`: `git diff --name-only main..<branch>` — AND verify the actual commit: `git show <head_sha> --stat`."

## Connections
- [[SubagentDiscipline]] — subagent verification checklist
- [[WorktreeWorkflow]] — git worktree + parallel dispatch
- [[AOSkepticGateOps]] — related dark-factory run
- [[PhantomFileDiff]] — 3-way merge display artifact
- [[AOBeads]] — jleechan-cv3, jleechan-g06, jleechan-ua8
