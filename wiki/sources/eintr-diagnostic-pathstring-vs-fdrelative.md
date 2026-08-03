---
title: "EINTR diagnostic: path-string vs fd-relative tools"
type: source
tags: [macos, disk, debugging, diagnostics]
date: 2026-08-02
source_file: raw/feedback_2026-08-02_eintr_diagnostic_pathstring_vs_fdrelative.md
---

## Summary
A session chased a "permanent EINTR" on `~/Library/Mail`/`~/Library/Messages`
across every load level, FDA-granted and not, through two different apps —
all identical, and it turned out to be an Endpoint Security AUTH-event race
that cleared on its own after a reboot. Separately, in the same session, a
truly-permanent 225 GiB stuck in `/private/var/dirs_cleaner` looked like the
same class of problem but was a different, permanently-broken case: Apple's
`removefile()`-based `nuke_dir` hit `ENAMETOOLONG` on one pathological
filename and aborted every pass, forever — not a race, and not fixed by
retry/reboot/permissions.

## Key Claims
- The distinguishing test: does the failing tool build an absolute path
  STRING per item (`du`, `removefile()`/`nuke_dir`) or traverse fd-relative
  (`find -delete`'s `unlinkat()`, `os.scandir`)? Path-string tools hit
  `ENAMETOOLONG`/`PATH_MAX` deterministically on pathological descendants;
  fd-relative tools never construct the full path and sidestep the bug.
- `Interrupted system call` (EINTR) that varies between attempts → plausibly
  a genuine race (signal-delivery / Endpoint-Security AUTH-event class);
  reboot or retry-with-backoff may genuinely help.
- `File name too long` (ENAMETOOLONG) that is 100% reproducible on the exact
  same path regardless of load/reboot/permissions → a path-length bug in a
  path-string tool; switch tools instead of retrying harder.
- Before spending more effort on permissions/load/reboot theories for a
  directory-read/delete failure, try a different tool with a different
  traversal strategy as a cheap diagnostic step.

## Key Quotes
> "the distinguishing test, in hindsight: does the failing tool build an absolute path STRING for each item... or does it traverse fd-relative / chdir-based"

## Connections
- [[eintr-diagnostic-pattern]] — the generalized concept page for this diagnostic
- [[dirs-cleaner-225gib-root-cause-and-fix]] — the concrete incident that surfaced this distinction
