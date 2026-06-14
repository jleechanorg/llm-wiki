---
title: "disk_snapshot.sh discover subshell + glob-tracking bugs"
type: source
tags: [feedback, bug-fix, bash, disk-magician]
date: 2026-06-13
source_file: feedback_2026-06-13_disk_snapshot_discover_bugs.md
last_updated: 2026-06-13
---

## Summary
Two latent bugs in `scripts/disk_snapshot.sh` made `./disk_magician.sh discover`
silently lie about which >5GB dirs were tracked vs UNTRACKED. Bug 1: a
`local` declaration inside a `printf | while read` subshell pipeline crashed
bash with "local: can only be used in a function". Bug 2: the discover
subcommand populated `MONITORED_PATHS` only from `monitored_dirs`, so any
glob-matched directory (e.g. `~/actions-runner*`) was wrongly reported as
UNTRACKED even though the snapshot measurement honored it.

## Key Claims
- The `| while read` pipeline body in bash runs in a subshell, where `local`
  is illegal and the entire subshell dies on the first iteration. The caller
  sees a 0-line result and assumes the discover scan found nothing — a
  silent failure mode far worse than a loud crash.
- `discover` must mirror the snapshot's own coverage rules; if the
  measurement loop honors `monitored_globs` and `monitored_file_globs`, the
  "is this candidate tracked?" check must too. Otherwise the report
  diverges from reality and inflates the regrowth-prevention audit backlog.
- The `disk_magician` package has two copies of `disk_snapshot.sh`
  (`scripts/` and `src/disk_magician/scripts/`); both must stay in sync.
  `pip install -e .` reads the second.
- A config-template expansion that surfaces audit gaps is the right way
  to close a discover gap: add the discovered dirs/globs to
  `config.json.template` so every host's snapshot sees them.

## Key Quotes
> "The `| while read` opens a subshell. `local` is only legal inside a
> `function` body, so bash aborts the entire subshell with exit 1 and the
> discover process dies silently after printing the header. Caller sees a
> 0-line result and assumes everything is fine."

> "Any directory matched by a glob pattern (e.g. `~/actions-runner*`) was
> reported as **UNTRACKED** by discover, even though `disk_snapshot.sh`'s
> main `# Run glob checks` loop below correctly measured it."

> "Any time a bash script has a `printf | while read` loop that needs to
> *write* into a hash/array visible in the parent shell, two things are
> wrong at once: (1) `local` is illegal in that body, and (2) variable
> writes don't escape the subshell anyway. Correct pattern: read into a
> temp file with `mapfile`/`readarray`, or use process substitution
> `while read; do …; done < <(printf …)` which runs in the parent shell
> and makes `local` legal."

## Connections
- [[DiskCleanupCoverage]] — discover mode is the gap-finder for snapshot coverage
- [[disk-magician]] — the repo that owns this script
- [[DiskMagicianDiscover]] — the subcommand and its measurement contract
- [[SubshellLocalBug]] — the underlying bash semantics that caused Bug 1
- [[MonitoredPathsAssociativeArray]] — the data structure discover and snapshot both populate
- [[RegrowthPrevention]] — the broader effort that depends on accurate discover output
