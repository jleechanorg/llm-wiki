---
name: worktree-recency-proxies-are-unsafe-measure-do-not-proxy
description: "`stat <wt>/.git` and `stat <wt>` measured CREATION age, not use — both over-stated staleness on this machine; fail-closed canonical helper now exists"
metadata: 
  node_type: memory
  type: feedback
  bead: "disk_magician-y7t (sweep forensics, OPEN — different incident)"
  originSessionId: d1c16e37-c03b-4f8d-bf7d-57d09005a2a4
  modified: 2026-07-27T09:46:03.668Z
---

Context: the 14-day worktree protection rule in disk_magician's `CLAUDE.md` was implemented
in three independent scripts as `stat <wt>/.git` and `stat <wt>`. Both over-stated staleness on
the live 340-worktree worldarchitect.ai registry, measured 2026-07-26:

- `worldarchitect-5-pr8116` and `worldarchitect-4` both reported 20.4 days old from both proxies
  while their newest file was 12.8 days old — inside the 14-day protected window. Under the old
  proxies they were eligible for deletion/strip; under the rule they were protected.
- Both proxies are durable defects, not race conditions.

Why each proxy is wrong:

| Proxy | Reality on a linked worktree | What you wanted |
| --- | --- | --- |
| `stat <wt>/.git` | `.git` is a one-line `gitdir:` pointer written once by `git worktree add` | when content was last edited |
| `stat <wt>` (parent dir mtime) | only moves when a *top-level* entry is added/removed; deep edits never touch it | when content was last edited |
| `sort -rn \| head -1` (worktree_hygiene.sh's old find pipeline) | `head -1` closing the pipe early raises SIGPIPE in sort under `set -o pipefail`; healthy scan returns EMPTY | healthy recency output |

A **fail-open** third defect: the old `worktree_hygiene.sh` had a fallback `stat -f '%m' "$path"`
when its find pipeline returned empty. That was the most stale-biased number available, exactly
the opposite of what a safety check should do on its failure path.

Fix (shipped in disk_magician PR #50, merged 2026-07-27, commit `9d702c6`):
- New `scripts/lib/worktree_recency.sh` is the single sanctioned implementation; it computes
  the maximum non-pruned content mtime in a single-pass awk (avoiding SIGPIPE), fails closed to
  `now` (age 0 = protected) when unmeasurable, and deliberately ignores git admin-dir activity
  (because `git status --porcelain` rewrites the index and worktree_hygiene.sh runs it on every
  candidate — counting it would self-poison).
- `cleanup_worktrees.sh`, `cleanup_worktree_venvs.sh`, `worktree_hygiene.sh` source it; their
  inline mtime/find blocks are removed.
- 11 regression cases in `tests/test_worktree_recency.sh`, including explicit failure-of-the-old
  proxies and a fail-closed assertion.
- Test case 4: venv/node_modules/`__pycache__` are pruned from the mtime walk — so this script's
  own `rm -rf venv` (cleanup_worktree_venvs.sh) does not bump the worktree's apparent activity
  and re-classify the dormant pool as "too young" next pass.
- Test cases 1 and 5 lock in: (a) deep edits today are protected even when `.git` and parent dir
  are 30d stale, (b) unmeasurable → age 0 → protected.

**Why:** reproduction path is in commit `9d702c6`'s messages and in the PR body ("Live false-old
proof" row). Landed after rebasing onto `fdb41ae fix: retire unsafe Gemini dedup` and fixing the
Evidence Gate schema (the validator at `.github/scripts/validate_evidence.py` requires
`**Claim class:**`, `**Verdict:**`, `**Commands and results:**`, `**What this proves:**`, `**What
this does not prove:**` — table cells alone do not satisfy it). 173 tests pass.

**How to apply:** treat any new "is this X stale?" check the same way: measure it, do not proxy
it. For worktrees specifically, source `scripts/lib/worktree_recency.sh`; never reintroduce a
standalone `stat <wt>/.git` or `stat <wt>` block. For other "stale" judgments, prefer the same
pattern — a dedicated helper that fails closed, with a regression test that asserts the
unmeasurable case is protected.

See also: related open bead `disk_magician-si1` (the 14-day floor still does not bind
machine-wide — `host-disk-guardian` deletes merged-PR worktrees with no min-age check, safe
today only because its glob is `/private/tmp/wa-*`).
