---
title: "/integrate global-script fallback when no local integrate.sh exists"
type: source
tags: [integrate, git, fallback, script-resolution, dark-factory]
date: 2026-08-28
source_file: memory/feedback_2026-08-28_integrate_global_script_fallback.md
---

## Summary

The dark-factory checkout had no repository-local `./integrate.sh`. `/integrate` resolved the maintained global script at `~/.claude/plugins/marketplaces/claude-commands-marketplace/scripts/integrate.sh` instead of treating the missing local file as a terminal failure, verified it by content/hash against the top-level marketplace copy (mtimes were identical, so mtime couldn't be used to pick the newer one), ran without `--force` first, then used `--new-branch` to recover cleanly after a backup-branch hard-stop.

## Key Claims

- Filesystem mtimes can match between two candidate scripts even when their content differs — "newer" must be established by diffing content/hashes, not by `ls -la` / mtime comparison.
- The maintained global script (900 lines / 40,252 bytes, SHA-256 `470b57b1...` ) is a superset of the top-level marketplace copy (657 lines / 28,988 bytes, SHA-256 `3fe1b701...`): +307/-64 lines adding absolute hook-path handling, beads-daemon-aware stashing, and checkout-blocker cleanup.
- A repo with no local `integrate.sh` should treat the maintained global script as a fallback implementation, not a hard stop.
- When the initial run hard-stops on a backup branch with local (non-main) commits, the correct recovery is `--new-branch` (preserves the backup, branches fresh from `origin/main`) — not `--force` (which would discard it). This mirrors [[IntegrateHardStopPattern]]'s "never `--force` without explicit approval" rule.
- Verified outcome: `dev1787937579` created from `origin/main` at `422e86bc5e2c04df3af23c27ebbece5b2d000c31`; HEAD, `origin/main`, and the new branch all resolved to that SHA with zero commits ahead and a clean tree. Both candidate scripts pass `bash -n`.

## Key Quotes

> "Treat the repository-local script as an optional project override and the maintained global script as the fallback implementation. Verify the selected script by absolute path, content/hash, and syntax; verify the new branch's base SHA and clean status after recovery." — reusable pattern from the memory record

## Connections

- [[IntegrateSh]] — the entity this fallback resolution logic applies to; add the global-script fallback path as a known behavior
- [[IntegrateHardStopPattern]] — same "don't `--force` past a hard-stop" discipline; this case is the `--new-branch` recovery arm of that decision matrix, applied when the local script is absent so the maintained global script is used instead
- [[IntegrateScriptResetGuard]] — sibling concept on integrate.sh safety; this source doesn't hit the reset-guard bug but shares the "verify by SHA/branch-state, not by assumption" discipline
