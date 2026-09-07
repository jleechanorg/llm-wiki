---
name: advice-runner-lfs-smudge-and-concurrent-merge-race
description: "run_primary_pair.py removed origin before checkout, breaking LFS smudge on any commit reaching an LFS blob; also a concurrent session can merge a PR mid-/ready"
metadata: 
  node_type: memory
  type: feedback
  bead: rev-ot94l
  originSessionId: 6f785d60-3856-40d7-b876-ebbf4fa02852
  modified: 2026-09-07T06:09:03.457Z
---

**FIX: `create_clone()` in `~/.claude/skills/advice/scripts/run_primary_pair.py` now sets `GIT_LFS_SKIP_SMUDGE=1` for both the clone and checkout subprocess calls**, applied 2026-09-06 while driving PR #9743 through `/ready`.

## The bug

`create_clone()` clones the target repo (`git clone --no-local --no-checkout`), then runs `git remote remove origin` for review isolation, then `git checkout --detach <sha>`. If the checked-out tree reaches any Git-LFS-tracked blob, the smudge filter needs a remote to fetch the real content from — but `origin` was just removed, so LFS's batch request has an empty URL and fails with `Smudge error: ... missing protocol: ""`, and `git checkout` exits 128. This was **100% reproducible** whenever the reviewed SHA's tree included an LFS pointer (e.g. `docs/user-stories-ui/videos/*.mp4` in this repo) — not a race, not flaky infra. Confirmed by manually replaying `clone → remote remove origin → checkout` outside the runner and capturing real stderr (the runner's own `CalledProcessError.__str__` swallows stderr, which is why this looked like an opaque exit-128 failure for three retries before the real cause surfaced).

**Why it looked like a race at first**: `git clone --no-local` on this specific repo (large history + binaries) can take 5-10+ minutes under load via a real `pack-objects`/`index-pack` cycle — genuinely slow, not hung. A red herring along the way: a week-old stale `objects/maintenance.lock` (no owning process) in the shared `.git` dir was also blocking clones; removing it was correct but didn't fix this bug — the LFS smudge failure was the actual, separate, deterministic cause.

**Fix**: reviewers need the code, not the binary media, so skip the LFS smudge filter entirely in these disposable review clones via `env = dict(os.environ, GIT_LFS_SKIP_SMUDGE="1")` passed to both the clone and checkout subprocess calls.

## Verification

Isolated repro (bypassing the runner) captured the exact stderr:
```
Error downloading object: docs/user-stories-ui/videos/....mp4: Smudge error: ... missing protocol: ""
error: external filter 'git-lfs filter-process' failed
fatal: ...: smudge filter lfs failed
```
After the fix, `create_clone()` run standalone against the same SHA completed cleanly (`HEAD == <sha>`, no error) — verified via a background Python invocation.

## Separate, unrelated finding from the same session: concurrent-session merge race

While this fix was being proven out (multiple `/advice` runner launches, each taking many minutes to clone), **a different concurrent session on the same account** (git-attributed "Claude Fable 5.1") independently squash-merged the exact PR (#9743) I was still running `/ready` gates on — I never called `gh pr merge`. Detected via `gh api repos/.../pulls/<n> --jq '.state'` suddenly returning `MERGED` mid-session, and via `git merge-base --is-ancestor <mycommit> origin/main` returning false even though `git ls-remote` showed my branch's tip was pushed. **Lesson: on a shared account with multiple concurrent agent sessions, always re-check `gh pr view --json state,mergedAt` before continuing a long `/ready` cycle** — a PR can be merged out from under you by a sibling session, and any commit you push *after* that merge point needs its own new PR (cherry-pick onto fresh `origin/main`), since the original PR is closed.

## Pattern to reuse

When a subprocess step fails with a bare `CalledProcessError` and the message doesn't explain why, don't trust the exception string — re-run the exact command sequence standalone with `stderr` actually captured and printed; `subprocess.CalledProcessError.__str__()` never includes stderr text even when it was captured.

## References

- PR #9743 (harness-policy consolidation, merged by a concurrent session): https://github.com/jleechanorg/worldarchitect.ai/pull/9743
- Follow-up PR #9768 (symlink-guard test flagged by the same `/advice` review): https://github.com/jleechanorg/worldarchitect.ai/pull/9768, merged as `71d6544a292`
- Fixed file: `~/.claude/skills/advice/scripts/run_primary_pair.py` (`create_clone()`)
- Bead: rev-ot94l (closed)

See also [[feedback_2026-08-25_selfhosted_runner_cross_pr_contention_confirmed]] and [[feedback_2026-08-17_severe_shared_worktree_collision_ci_deletion_and_fabrication]] for related shared-environment contention patterns.
