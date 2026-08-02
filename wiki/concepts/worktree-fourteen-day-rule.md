---
title: WorktreeFourteenDayRule
type: concept
tags: [disk_magician, worktree, safety, recency, fail-closed]
sources: [sources/feedback-2026-07-27-worktree-recency-proxies-wrong.md]
last_updated: 2026-07-27
---

A git worktree touched within the last 14 days is PROTECTED. No script, sweeper, launchd job,
or agent in `disk_magician` may delete, archive, strip (`venv/` included), or `git worktree
remove` it — regardless of merged PR status, ahead count, or disk pressure. The 14-day figure
is a floor, not a target; `safety_min_stale_days` may raise it but never lower it.

The rule was previously written in human prose and implemented via two `stat`-based proxies
(`stat <wt>/.git`, `stat <wt>`), both of which **measured creation age**, not use. Live
measurement on 2026-07-26 against the 340-worktree worldarchitect.ai registry: 2 of 30 sampled
worktrees read 20.4 days old from both proxies while their newest file was 12.8 days old —
inside the protected window.

## Canonical implementation

The single sanctioned implementation lives at
`scripts/lib/worktree_recency.sh` in `jleechanorg/disk_magician`. It exposes:

- `worktree_last_activity_epoch <path>` — max of non-pruned content mtime, falls closed to `now`
- `worktree_age_days <path>` — whole days since last activity
- `worktree_is_recently_active <path> <min_days>` — returns 0=protected, 1=eligible

`cleanup_worktrees.sh`, `cleanup_worktree_venvs.sh`, and `worktree_hygiene.sh` all source it.
No other recency computation is permitted on disk_magician worktrees.

## Why it matters

Three call sites independently re-derived the rule before the helper existed, and each
re-derivation was a `stat` against `.git` or the parent dir. All three systematically over-stated
staleness; two of them ran in production launchd jobs. Under the right environmental pressure
(9 GB free, emergency-reclaim mode), the per-script failure would have classified actively-edited
worktrees as eligible.

## Related invariants

- The 14-day floor is a **floor**, not a target. `safety_min_stale_days` in
  `~/.config/disk-magician/safety.local.json` may raise it.
- `/--execute` on `worktree_hygiene.sh` still requires `WORKTREE_APPROVED=1` in the environment.
- Any new "is this X stale?" check on the codebase should follow the same pattern: a single
  dedicated helper with a fail-closed default and a regression test that asserts the
  unmeasurable case is protected.

## Forwarded gaps

- Open bead `disk_magician-si1`: this rule does NOT bind machine-wide. The `host-disk-guardian`
  job (`org.jleechanorg.host-disk-guardian`) deletes merged-PR worktrees with NO min-age check.
  Safe today only because its `WORKTREE_GLOB` is `/private/tmp/wa-*`; widening that env var
  would re-introduce the same defect on a different repo.
- `disk_magician-fo6`: `pyproject.toml` version regression was the reason this fix silently
  failed to deploy — `uv` caches by version. A CI/pre-commit check is the durable answer.

See `sources/feedback-2026-07-27-worktree-recency-proxies-wrong.md` for the live evidence.
