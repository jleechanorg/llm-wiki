# EINTR Diagnostic Pattern

Distinguishes two failure signatures that look similar (a directory read/delete that
keeps failing) but have opposite root causes and opposite fixes.

## Pattern

| Signature | Behavior | Root cause class | Fix |
|---|---|---|---|
| `Interrupted system call` (EINTR) | Varies — sometimes clears between attempts, across load levels, across apps | Signal-delivery / Endpoint-Security AUTH-event race | Retry-with-backoff or reboot may genuinely help |
| `File name too long` (ENAMETOOLONG) | 100% reproducible on the exact same path, every attempt, regardless of load/reboot/permissions | Path-length bug in a path-string-constructing tool (`du`, `removefile()`) | Switch to an fd-relative tool (`find -delete`, `os.scandir`) — retrying the same tool never helps |

## Why it matters

Both signatures present as "this directory won't let me read/delete it," which
tempts the same response (grant more permissions, retry harder, reboot). Only
the EINTR class actually responds to those. Treating an ENAMETOOLONG failure
as a permissions/load problem burns effort chasing TCC/FDA grants and load
theories that can never fix a hardcoded path-length limit.

## 2026-08-02 example

[[dirs-cleaner-225gib-root-cause-and-fix]] — Apple's own `nuke_dir`
(`removefile()`) hit ENAMETOOLONG on one pathological filename inside
`/private/var/dirs_cleaner` and aborted every purge pass, forever, until
`find -delete` (fd-relative `unlinkat()`) was used instead. In the same
session, a genuinely separate Mail/Messages/MobileSync EINTR block *did*
resolve on its own after a reboot — correctly diagnosed as a different
failure class.

## Diagnostic test

Before concluding "permanently blocked" (reach for FDA grants) or "just a
transient race" (retry longer): check whether the failing tool builds
absolute path strings per item (fails deterministically at `PATH_MAX`) or
traverses fd-relative (never hits the limit at all).
