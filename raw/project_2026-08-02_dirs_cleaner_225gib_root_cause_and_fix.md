---
name: dirs-cleaner-225gib-root-cause-and-fix
description: "macOS deleted_helper (CacheDelete.framework) can silently accumulate 100+ GiB of orphaned staging content in /private/var/dirs_cleaner due to an Apple-side ENAMETOOLONG bug in removefile()/nuke_dir — diagnosed via unified log, fixed via find -delete"
metadata: 
  node_type: memory
  type: project
  bead: disk_magician-b1c (closed)
  originSessionId: 59cb5847-ffee-401b-aaea-11f259e16a92
  modified: 2026-08-03T02:18:53.049Z
---

On jeffreys-macbook-pro, 225.3 GiB was sitting in `/private/var/dirs_cleaner`
— invisible to every normal `du`/`ls`/frontier-scan pass all session (looked
like "unmeasured residual" in disk accounting) because the directory is
root-owned and non-privileged tools can't even list it.

**Root cause (confirmed via unified log, not inference):** Apple's own
`deleted_helper` daemon (`/System/Library/PrivateFrameworks/
CacheDelete.framework/deleted_helper`, parent daemon `deleted`) is macOS's
built-in low-disk-space / purgeable-cache reclaimer. It stages orphaned
`/tmp`-scratch content (ssh-agent sockets, ios-simulator-mcp temp dirs, PR/CI
test artifacts, launchd temp sockets — recognizable, disposable scratch, not
user data) into `/private/var/dirs_cleaner/<random-2-char-batch>/` via an
atomic rename (so the original location appears instantly clean), then
deletes the staged batch in the background. `log show --predicate 'process
== "deleted_helper" AND eventMessage CONTAINS "removefile error"'` showed 86
identical failures in a single afternoon: `nuke_dir: removefile error for
/private/var/dirs_cleaner/ : File name too long` (ENAMETOOLONG) — one
pathological long/corrupted filename inside one batch aborts the ENTIRE
purge pass every single time, so nothing ever gets deleted, and new batches
keep piling up on top (9 batches found, oldest mtime 2026-07-11).

**Fix (workaround — third-party/Apple-OS-bug, no code we can patch):**
`sudo -n find /private/var/dirs_cleaner/<batch> -mindepth 1 -delete`,
batch-by-batch, oldest first. `find -delete` uses fd-relative `unlinkat()`
during traversal rather than building absolute path strings the way
`nuke_dir`/`removefile()` does — it is not affected by the same
ENAMETOOLONG bug. Verified: all 10 batches deleted cleanly (zero errors,
including the exact batch containing the pathological filename), confirmed
via `sudo -n du -sh` (0B after) and `df` (271.8 GiB free, up from 99.4 GiB
before). This machine's passwordless sudo scope (`/etc/sudoers.d/
disk_magician*`) already covers `du, diskutil, rm, rsync, disktool, apfs,
find, mv, ln` — no password/general sudo needed to execute this fix.

**Why this matters beyond this one incident:** `deleted_helper` is
event-triggered by VFS low-disk-space signals (not just a daily timer), so
it WILL stage new content into the same directory again in the future. If
the same or a similarly pathological filename gets staged again, the same
backlog will reaccumulate. The fix is not permanent (it's Apple's bug, not
ours) — but the recovery procedure is fully reusable: check `/private/var/
dirs_cleaner` size with `sudo -n du -sh`, and if large, re-run the same
batch-by-batch `find -delete` (never a single `rm -rf` — isolate failures
per-batch in case a NEW pathological path breaks a specific batch).

**Full writeup with exact commands, log evidence, and remediation
transcript:** `roadmap/2026-08-02-research-dirs-cleaner-os-mechanism.md` in
the disk_magician repo (commit `6c11cc4`).

**Why:** This was the actual answer to "why does the disk always feel full"
for 91% of the previously-unexplained residual — not the Colima fstrim
sawtooth (self-correcting amplitude) and not Mail/Messages/TCC (ruled out at
only 4.4 GiB combined after a reboot cleared an unrelated Endpoint-Security
EINTR block).

**How to apply:** On this machine (or any Mac showing a large, growing,
unexplained `df`-vs-`du` gap with no obvious hidden directory), check
`sudo -n du -sh /private/var/dirs_cleaner` early — before chasing TCC
permissions, load theories, or Spotlight/snapshot explanations. See
[[eintr-path-string-vs-fd-relative-diagnostic]] for the general diagnostic
pattern this incident is an instance of.
