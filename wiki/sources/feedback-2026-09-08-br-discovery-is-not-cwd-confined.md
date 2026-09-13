---
title: "br discovery is not cwd-confined (2026-09-08, updated 2026-09-13)"
type: source
tags: [beads, br-cli, worktree, database-discovery, anti-pattern]
date: 2026-09-13
source_file: feedback_2026-09-08_br_discovery_is_not_cwd_confined.md
---

## Summary
`br`'s (Beads CLI) database discovery does not reliably confine itself to the
current worktree. Original finding (2026-09-08): in a worktree with no local
`.beads/beads.db`, `br update` silently bound to a different checkout's
database and mutated the wrong branch, with no error and a clean local `git
status`. A 2026-09-13 addendum during PR #9842's review found a more severe
variant: even with a valid, present local `.beads/beads.db` and
`.beads/config.yaml`, plain `br` (no `--db` flag) can still resolve a
registered "Project config" entry pointing at the *main checkout's* database
instead — a different physical SQLite file, confirmed by differing inodes.

## Key Claims
- Silent wrong-database writes are the default hazard, not an edge case, when running many worktrees of one repo concurrently.
- `br config path` reveals the actual resolved config chain (user config, legacy user config, project config) — worth running before trusting any `br` command's target.
- A present, valid local `.beads/beads.db` + `.beads/config.yaml` does NOT guarantee default discovery uses it; a project-config registry entry can outrank it.
- `br --db <worktree>/.beads/beads.db <cmd>` (explicit relative path) reliably targets the worktree's own database; plain `br` does not.
- The usual sanity check (`git status`/`git diff` in the worktree showing clean) reads as "no changes needed" when the real answer is "changes went elsewhere" — this failure mode defeats the normal verification instinct.

## Key Quotes
> "Nothing failed. It was caught only because the lane ran `br info` on its own initiative before pushing, then `git restore`d the other checkout and redid the work." — 2026-09-08 incident

> "Default discovery isn't just 'walk outward and find nothing local, so fall back' — a registered project config can outrank a present, valid local one." — 2026-09-13 addendum

## Connections
- [[BeadsRedirectConvergence]] — a related, more general safety pattern for consolidating/repairing multiple `.beads` redirects onto one canonical directory without corrupting the store; this source is the narrower "why default discovery itself can't be trusted" precursor problem.
- [[BrProjectConfigRegistryShadowing]] — the specific mechanism (project-config registry entry shadowing a valid local DB) documented in the 2026-09-13 addendum.
