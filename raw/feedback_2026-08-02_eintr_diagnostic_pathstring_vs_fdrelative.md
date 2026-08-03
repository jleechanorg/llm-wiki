---
name: eintr-path-string-vs-fd-relative-diagnostic
description: "When a directory read fails with EINTR/ENAMETOOLONG-class errors that don't clear with retries, test whether the tool builds absolute path strings (du, macOS removefile/nuke_dir) vs traverses fd-relative (find -delete, os.scandir) before concluding \"permanently broken\" or blaming TCC/load"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 59cb5847-ffee-401b-aaea-11f259e16a92
  modified: 2026-08-03T02:19:31.383Z
---

Spent most of a session chasing a "permanent EINTR" on `~/Library/Mail` /
`~/Library/Messages` across every load level (64 to 1000+), with and without
Full Disk Access granted, through two different apps (this session's cmux
and macOS Terminal.app) — all identical failures. Concluded (correctly, per
later `/research`) it was an Endpoint Security AUTH-event race, unrelated to
TCC/FDA/load. It resolved on its own after a host reboot.

Separately, in the SAME session, found a truly-permanent-looking 225 GiB stuck
in `/private/var/dirs_cleaner` that LOOKED like the same class of problem
(persistent EINTR/ENAMETOOLONG on a directory, un-fixable by retries) but was
actually a *different, permanently-broken* case: Apple's own `nuke_dir`
(via `removefile()`) hit ENAMETOOLONG on one pathological filename and
aborted its ENTIRE pass, every single time, forever — not a race that clears
with time/reboot.

**The distinguishing test, in hindsight:** does the failing tool build an
absolute path STRING for each item (as `du`, and Apple's `removefile()`-based
`nuke_dir`, both do — confirmed via source/binary-string inspection), or
does it traverse fd-relative / chdir-based (as BSD `find -delete`'s
`unlinkat()` and Rust's `std::fs::read_dir` do)? Path-string tools hit
`ENAMETOOLONG`/`PATH_MAX` limits on deeply-nested or pathologically-named
descendants and this failure is DETERMINISTIC per path, not something a
reboot or a permission grant fixes. Fd-relative tools sidestep this because
they never construct the full path at all.

**Why this matters:** before concluding a directory-read failure is
"permanently blocked" (and reaching for FDA grants, app-switching, or
giving up), or conversely before assuming "just keep retrying, it's a
transient race" — check WHICH failure signature you have:
- `Interrupted system call` (EINTR) that varies in whether it clears
  between attempts → plausibly a race (AUTH-event/signal-delivery class);
  reboot or retry-with-backoff may genuinely help.
- `File name too long` (ENAMETOOLONG) that is 100% reproducible on the
  exact same path every single time, regardless of load/reboot/permissions
  → a path-length bug in a path-string-based tool; switch to a fd-relative
  tool (`find -delete`, `os.scandir`-based walk) instead of retrying the
  same tool longer or harder.

**How to apply:** when a size-measurement or deletion tool fails
consistently on a specific subtree, try a DIFFERENT tool with a different
traversal strategy (fd-relative vs path-string) as a diagnostic step before
spending more effort on permissions/load/reboot theories for that specific
failure. Real example + full remediation transcript:
[[dirs-cleaner-225gib-root-cause-and-fix]].
