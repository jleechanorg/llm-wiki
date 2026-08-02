---
title: FailClosedSafety
type: concept
tags: [safety, recency, disk_magician, worktree, harness-engineering]
sources: [sources/feedback-2026-07-27-worktree-recency-proxies-wrong.md]
last_updated: 2026-07-27
---

The default in safety gates is "unknown ⇒ protected". Any "is this X stale?" computation that
cannot produce a deterministic answer must return age 0 (or its equivalent "protected") and not
fall through to a stale-biased fallback.

## Why the inverse happens

The natural implementation order — when a fallback path is needed to keep the script
deterministic — is to fall through to "the most readily-available number". That number is
almost always the one representing the most-stale moment we have data for, which is exactly
the opposite of what a safety check should do on its failure path.

`worktree_hygiene.sh`'s old fallback when its `find | sort -rn | head -1` pipeline returned
empty was `stat -f '%m' "$path"` against the worktree root. That directory's mtime only moves
when a top-level entry is added/removed; deep edits never touch it. The fallback was therefore
the most stale-biased number the script could produce, and it was the path that fired whenever
SIGPIPE under `pipefail` killed `sort`. The failure mode of the safety check was: mark protected
things deletable.

## Test pattern

`tests/test_worktree_recency.sh` case 5 (and the canonical comment in `CLAUDE.md` for the
disk_magician repo): assert the "unmeasurable" input is protected.

```bash
assert_eq "$(worktree_age_days "$TMPROOT/does-not-exist")" "0" \
    "nonexistent path fails closed to age 0"
if worktree_is_recently_active "$TMPROOT/does-not-exist" 14; then
    ok "unmeasurable path is treated as PROTECTED"
else
    bad "unmeasurable path was treated as deletable — fails open"
fi
```

A sweeper that cannot prove a worktree is old must not touch it.

## Related concepts

- [[WorktreeFourteenDayRule]] — concrete instance of the fail-closed pattern on this repo
- [[HarnessEngineering]] — higher-level: safety contract belongs in tests, not docs
