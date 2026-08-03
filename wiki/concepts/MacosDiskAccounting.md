# macOS Disk Accounting

Notes on why `df` used-space can exceed everything a normal `du`/frontier-scan
pass can attribute, and where the gap tends to actually live on this machine.

## Known contributors to an unattributed df-vs-du residual

- **Colima sparse-disk fstrim sawtooth** — VM-internal free blocks not yet
  trimmed back to the host; amplitude self-corrects, not a real leak.
- **`/private/var/dirs_cleaner`** — root-owned staging area for Apple's
  `deleted_helper` daemon; invisible to unprivileged `du`/`ls`; can silently
  accumulate 100+ GiB if a purge pass keeps failing. See
  [[dirs-cleaner-225gib-root-cause-and-fix]].
- **TCC/Endpoint-Security-gated paths** (`~/Library/Mail`, `~/Library/Messages`,
  `~/Library/Application Support/MobileSync`) — can appear "unmeasurable" due
  to an EINTR race, not necessarily due to actual size; see
  [[eintr-diagnostic-pattern]] before assuming these hold the missing space.
- **APFS snapshots / local Time Machine snapshots** — space reserved but not
  attributable to any single directory walk.

## Rule

Before reporting a large df-vs-du residual as "unmeasured" or "unexplained,"
check root-owned staging/purge directories and TCC-gated paths directly
(with sudo where available) rather than defaulting to "opaque protected
space." The 2026-08-02 investigation found the dominant contributor
(225.3 GiB) was a checkable, fixable Apple-side bug, not opaque OS reserve.
