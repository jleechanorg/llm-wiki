---
name: integrate-global-script-fallback
description: /integrate can use the maintained global integrate.sh when a repository has no local copy
type: feedback
bead: none
---

## Context

The dark-factory checkout had no repository-local `./integrate.sh`. The
`/integrate` workflow therefore needed to resolve the maintained global
implementation instead of treating the missing local file as a terminal
failure.

## Technical detail

The maintained script is
`/Users/jleechan/.claude/plugins/marketplaces/claude-commands-marketplace/scripts/integrate.sh`.
The top-level marketplace copy is
`/Users/jleechan/.claude/plugins/marketplaces/claude-commands-marketplace/integrate.sh`.
The scripts have the same filesystem mtime in this installation, so
"newer" must be established by content rather than mtime: the maintained
script is 900 lines / 40,252 bytes versus 657 lines / 28,988 bytes, and the
unified diff is 307 additions and 64 deletions. Its added logic includes
absolute hook-path handling, beads-daemon-aware stashing, and checkout-blocker
cleanup. SHA-256 values at verification were respectively
`470b57b12a245980518ee619b091c8cd3e1fed5b5a559b0265be65e607a5f9da` and
`3fe1b7019eedbae8150cb4f17c4846f551e335d3b4351809b407557a481ec47e`.

## Solution / rule

When `./integrate.sh` is absent, `/integrate` should point to the maintained
global script under `.../scripts/integrate.sh`, after comparing it with the
top-level marketplace copy. Run without `--force` first. If an
unsynchronized/no-upstream backup branch hard-stops because it has local
commits, use the script's built-in `--new-branch` mode to preserve that branch
and create a fresh development branch from `origin/main`; do not discard the
backup or jump directly to `--force`.

## Verification

The initial global-script run returned rc=1 on a backup branch with three
non-main commits. The safe retry with `--new-branch` succeeded, creating
`dev1787937579` from `origin/main` at `422e86bc5e2c04df3af23c27ebbece5b2d000c31`.
At capture time `HEAD`, `origin/main`, and the new branch all resolved to that
SHA, with zero local commits ahead and a clean repository. Both candidate
scripts pass `bash -n`.

## Reusable pattern

Treat the repository-local script as an optional project override and the
maintained global script as the fallback implementation. Verify the selected
script by absolute path, content/hash, and syntax; verify the new branch's
base SHA and clean status after recovery.

## References

- `/Users/jleechan/.claude/plugins/marketplaces/claude-commands-marketplace/scripts/integrate.sh`
- `/Users/jleechan/.claude/plugins/marketplaces/claude-commands-marketplace/integrate.sh`
- `git reflog` at 2026-08-28 10:19:39 -0700 (branch creation and base fast-forward)
