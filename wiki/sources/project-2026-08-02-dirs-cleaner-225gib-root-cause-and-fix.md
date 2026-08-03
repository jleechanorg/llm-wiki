---
title: "dirs_cleaner 225GiB root cause + fix"
type: source
tags: [macos, disk, debugging, apfs]
date: 2026-08-02
source_file: raw/project_2026-08-02_dirs_cleaner_225gib_root_cause_and_fix.md
---

## Summary
On a MacBook Pro, 225.3 GiB was invisibly stuck in `/private/var/dirs_cleaner`
— macOS's own `deleted_helper` daemon (CacheDelete.framework) stages orphaned
`/tmp` scratch there for background deletion, but its `removefile()`-based
`nuke_dir` routine kept aborting every purge pass with `ENAMETOOLONG` on a
pathological filename (86 failures in one afternoon, confirmed via `log
show`). Fixed with `find -delete` (fd-relative `unlinkat`, sidesteps the
path-string bug), batch-by-batch, zero errors, reclaiming the full 225.3 GiB.

## Key Claims
- `/private/var/dirs_cleaner` is Apple's own standard staging root for
  `deleted_helper`'s orphan-purge mechanism, not a third-party or bespoke
  path — confirmed via the literal string compiled into both
  `/usr/libexec/dirs_cleaner` and `CacheDelete.framework/deleted_helper`.
- The accumulation is a live, repeating Apple-side bug: `nuke_dir` fails
  identically every single purge attempt with `File name too long`
  (ENAMETOOLONG), so nothing ever gets deleted and each new orphaned batch
  piles on top of the last (9 batches found, oldest from 2026-07-11).
- `find -delete` succeeds where Apple's own tool fails because it traverses
  fd-relative (`unlinkat()`) rather than constructing absolute path strings
  the way `removefile()` does — verified by successfully deleting the exact
  batch containing the pathological filename with zero errors.
- Generalizable diagnostic: a 100%-reproducible `ENAMETOOLONG` on the same
  path, unaffected by load/reboot/permission changes, is a tool-class bug
  (switch to an fd-relative tool) — distinct from variable `EINTR` failures
  (which can be a genuine race that retries or a reboot fix).

## Key Quotes
> "nuke_dir: removefile error for /private/var/dirs_cleaner/ : File name too long" — macOS unified log, 86 occurrences in one afternoon

## Connections
- [[macos-disk-accounting]] — this incident explains a large, otherwise-unattributable portion of a `df`-vs-`du` residual gap
- [[eintr-diagnostic-pattern]] — the path-string vs fd-relative distinction generalizes beyond this one incident
