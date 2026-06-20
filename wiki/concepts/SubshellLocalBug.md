---
title: "SubshellLocalBug"
type: concept
tags: [bash, anti-pattern, subshell, scoping]
date: 2026-06-13
last_updated: 2026-06-13
---

# SubshellLocalBug

A bash anti-pattern where a script declares `local` inside a pipeline body
that runs in a subshell. The `local` keyword is only legal inside a
`function`, so bash aborts the entire subshell with
`local: can only be used in a function`. The failure is silent if the
subshell was launched from a script that doesn't propagate the exit code
to the caller.

## Trigger
Any of these constructs opens a subshell:
- `printf … | while read; do …; done`
- `cmd | while read; do …; done`
- `cmd | for x in …; do …; done`
- Any loop body that is the *right* side of a pipe

Inside the body, `local`, `declare`, `typeset`, and `readonly` all fail.

## Why it is worse than a loud crash
The subshell dying prints an error to stderr that is easy to miss in a
cron job or a script that redirects 2>/dev/null. The rest of the script
continues with empty / unset variables. The user sees "the script
finished successfully" but the work was never done.

## Correct patterns
Pick one of these — they are not interchangeable:

**1. Read into the parent shell with process substitution** (writes
persist in the parent scope, `local` is legal):
```bash
while read -r line; do
  local kb=""
  …
done < <(printf '%s\n' "${candidates[@]}")
```

**2. Read into a temp file with `mapfile` / `readarray`** (no subshell
involved at all):
```bash
mapfile -t candidates < <(printf '%s\n' "$HOME"/.[!.]* "$HOME"/*)
for dir in "${candidates[@]}"; do
  …
done
```

**3. Accept that you're in a subshell and drop `local`** (the simplest
fix when the loop is short and doesn't need to mutate a parent variable).

## Anti-pattern
```bash
# WRONG — `local` is illegal here and silently kills the subshell
printf '%s\n' "${candidates[@]}" | while read -r dir; do
  local kb=$(du -sk "$dir" | awk '{print $1}')
  echo "$kb $dir"
done | sort -rn | head
```

## See also
- [MonitoredPathsAssociativeArray](MonitoredPathsAssociativeArray.md) — the data structure that revealed
  this bug in `disk_snapshot.sh`
- [feedback-2026-06-13-disk-snapshot-discover-bugs](../sources/feedback-2026-06-13-disk-snapshot-discover-bugs.md) — the original incident
