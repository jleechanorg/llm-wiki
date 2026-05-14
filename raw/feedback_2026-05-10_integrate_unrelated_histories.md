---
name: integrate.sh fails with unrelated histories on diverged main
description: When local main diverges from origin/main, integrate.sh --force merge fails with "refusing to merge unrelated histories"; manual reset required
type: feedback
bead: none
originSessionId: 6dbc678a-b305-4508-bb21-5fe7c8829514
---
## Context

Running `/integrate --force` on branch `dev1778136280`. Local `main` had diverged from `origin/main` (8858 local-only + 2 remote-only commits). The script's force mode tried `git merge origin/main` which hit "refusing to merge unrelated histories" and failed.

## Technical Detail

The divergence was caused by local main being stale — all 8858 "local-only" commits were actually in main's ancestry (the merge-base was `5b4dcf29c`). The 2 remote-only commits were:
- `73b1761be` Revert PR 6847
- `43160924b` Fix: map world_data.location to current_location_name

The `integrate.sh` script does not have a `--reset` or `--hard-reset` option. Its force mode attempts merge, which fails on unrelated histories.

## Rule

When `integrate.sh` fails with "unrelated histories" or "divergence detected":
1. `git checkout main`
2. `git reset --hard origin/main`
3. `git checkout -b dev$(date +%s)` (or custom branch name)
4. Delete old branch: `git branch -D <old-branch>`

**Why:** The script's force-merge path is insufficient for diverged histories. Manual reset is the safe resolution when the local branch has no unique work.

**How to apply:** If integrate.sh exits with "refusing to merge unrelated histories", bypass the script entirely with manual reset + new branch creation.

## Verification

- `git log --oneline -3` after reset confirmed HEAD matches `origin/main`
- New branch `dev1778453118` created successfully from latest main
- Old branch deleted cleanly

## References

- Old branch: `dev1778136280`
- New branch: `dev1778453118`
- Remote-only commits: `73b1761be`, `43160924b`
