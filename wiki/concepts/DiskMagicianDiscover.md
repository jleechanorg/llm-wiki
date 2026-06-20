---
title: "DiskMagicianDiscover"
type: concept
tags: [bash, subcommand, audit, disk-magician]
date: 2026-06-13
last_updated: 2026-06-13
---

# DiskMagicianDiscover

The `discover` subcommand of `disk_magician.sh`. Scans `~/$HOME` for
directories over 5 GB and reports each as either **tracked** (already in
the monitored config) or **UNTRACKED** (audit gap that should be added).

## Contract
A candidate dir is **tracked** if it appears in any of:
- `monitored_dirs[].path` (after `~` / `$HOME` expansion)
- The shell-glob expansion of any `monitored_globs[].pattern` entry
- The shell-glob expansion of any `monitored_file_globs[].pattern` entry

Anything else over 5 GB is UNTRACKED and should be added to the config.

## Latent bugs (fixed 2026-06-13)

**Bug 1 — `local` in a subshell-pipeline body.** The `printf | while read`
loop that classifies each candidate ran in a subshell. `local kb=""` inside
that body is illegal (`local: can only be used in a function`), so bash
aborted the entire subshell and the process died silently after printing
the header. Caller saw a 0-line result.

**Bug 2 — discover only read `monitored_dirs`.** The `MONITORED_PATHS`
associative array was populated only from `monitored_dirs[].path`.
Glob-matched dirs (e.g. `~/actions-runner*`) were reported as UNTRACKED
even though the snapshot measurement honored the glob. Fixed by also
expanding `monitored_globs` and `monitored_file_globs` into
`MONITORED_PATHS`.

## Verification
```bash
DISK_MAGICIAN_CONFIG=$PWD/config.json.template ./disk_magician.sh discover
# 19 candidates scanned, 0 UNTRACKED (was 3 before fix)
```

## References
- PR: https://github.com/jleechanorg/disk_magician/pull/4 (merged as 5975589)
- Memory: [feedback-2026-06-13-disk-snapshot-discover-bugs](../sources/feedback-2026-06-13-disk-snapshot-discover-bugs.md)
- Source: [feedback-2026-06-13-disk-snapshot-discover-bugs](../sources/feedback-2026-06-13-disk-snapshot-discover-bugs.md)
