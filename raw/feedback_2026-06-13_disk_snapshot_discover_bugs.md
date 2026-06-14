---
name: disk_snapshot.sh discover subshell + glob-tracking bugs
description: Two bugs in scripts/disk_snapshot.sh made `./disk_magician.sh discover` silently lie about which >5GB dirs were tracked vs UNTRACKED. Both fixed in commit f129f2d (PR #4, merged 5975589).
type: feedback
bead: none
---

# Context

The `disk_magician.sh discover` subcommand is meant to scan `~/$HOME` for >5GiB
directories and report each as either **tracked** (already in `monitored_dirs`
or matched by a glob) or **UNTRACKED** (audit gap that should be added). The
command is what tells the user which big dirs the snapshot is *not* measuring,
so false positives there directly inflate the regrowth-prevention backlog.

Two bugs combined to make discover useless on this host before 2026-06-13:

# Bug 1 — `local` in a subshell-pipeline body (scripts/disk_snapshot.sh:155)

```bash
# BEFORE (crashed with: "local: can only be used in a function"):
printf '%s\n' "${candidates[@]}" | while read -r dir; do
  local kb=""
  ...
done
```

The `| while read` opens a subshell. `local` is only legal inside a `function`
body, so bash aborts the entire subshell with exit 1 and the discover process
dies silently after printing the header. Caller sees a 0-line result and
assumes everything is fine.

**Fix:** drop `local` (the loop is in a subshell, scope is per-iteration anyway).
Mirrored in the package copy at `src/disk_magician/scripts/disk_snapshot.sh`.

# Bug 2 — discover only read `monitored_dirs`, ignored globs

```python
# BEFORE:
for item in data.get("monitored_dirs", []):
    print(item["path"])
```

`MONITORED_PATHS` (the set used to mark a candidate as "tracked") was populated
*only* from `monitored_dirs`. Any directory matched by `monitored_globs` (e.g.
`~/actions-runner*` matching `~/actions-runner`, `~/actions-runner-2`, …) was
reported as **UNTRACKED** by discover, even though `disk_snapshot.sh`'s main
`# Run glob checks` loop below correctly measured it.

**Fix:** also feed `monitored_globs` and `monitored_file_globs` into
`MONITORED_PATHS` after shell-glob expansion.

# Verification

```bash
DISK_MAGICIAN_CONFIG=$PWD/config.json.template ./disk_magician.sh discover
# 19 candidates scanned, 0 UNTRACKED (was 3 before fix)
```

# Files changed

- `scripts/disk_snapshot.sh` — both fixes
- `src/disk_magician/scripts/disk_snapshot.sh` — mirror (this is the package
  copy installed by `pip install -e .`; both must stay in sync)
- `config.json.template` — added 2 new monitored_dirs (`~/.colima`, `~/.hermes`)
  and 2 new monitored_globs (`~/project_*`, `~/.cache/huggingface/hub/models--*`)
  that the discover scan surfaced as audit gaps

# References

- Commit: `f129f2d feat(regrowth-prevention): track colima, hermes, project siblings; fix discover bug`
- PR: https://github.com/jleechanorg/disk_magician/pull/4 (merged as 5975589)
- Skill: `disk_magician` (the `discover` subcommand)

# Reusable pattern

Any time a bash script has a `printf | while read` loop that needs to *write*
into a hash/array visible in the parent shell, two things are wrong at once:
(1) `local` is illegal in that body, and (2) variable writes don't escape the
subshell anyway. Correct pattern: read into a temp file with `mapfile`/`readarray`,
or use process substitution `while read; do …; done < <(printf …)` which runs in
the parent shell and makes `local` legal.
