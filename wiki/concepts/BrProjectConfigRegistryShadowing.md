---
title: "BrProjectConfigRegistryShadowing"
type: concept
tags: [beads, br-cli, worktree, database-discovery, anti-pattern]
sources: [feedback-2026-09-08-br-discovery-is-not-cwd-confined]
last_updated: 2026-09-13
---

## Overview
`br` (the Beads issue-tracker CLI) can resolve a **registered "Project
config"** entry (visible via `br config path`) that points at a different
checkout's `.beads/config.yaml` than the one physically present in the
current worktree — even when the current worktree has its own valid,
non-empty `.beads/beads.db` and `.beads/config.yaml`. This is stronger than
the simpler "no local DB, falls back to a parent" failure: a present local DB
does not guarantee default (no `--db` flag) discovery actually uses it.

## Mechanism
1. `br` maintains config resolution layers: user config
   (`~/.config/bd/config.yaml`), legacy user config (`~/.beads/config.yaml`),
   and a **project config** keyed by project identity rather than a strict
   cwd walk.
2. When a project identity (e.g. a repo name like "worldarchitect.ai") is
   already registered against the main checkout's `.beads/` directory, `br`
   invocations from a *different* worktree of the same repo can resolve that
   registered entry instead of the worktree's own local `.beads/`.
3. The two `.beads/beads.db` files are physically distinct SQLite databases
   (confirmed by differing inodes) with potentially divergent issue sets —
   writes/reads silently land on the wrong one with no error.

## Symptom
`br show <id>` / `br close <id>` intermittently returns `Issue not found` for
an issue that demonstrably exists (confirmable via `grep '"id":"<id>"'
.beads/issues.jsonl` in the worktree), because the command actually queried
the other checkout's database.

## Fix / Mitigation
Always pin `--db <path>` explicitly, resolved relative to the current
worktree (e.g. `br --db .beads/beads.db show <id>` or `br --db
"$(pwd)/.beads/beads.db" show <id>`), for every `br` invocation run inside
any worktree other than the primary checkout. Never trust default/no-flag
discovery just because a local `.beads/` directory is present. Run `br config
path` first when in doubt — it prints exactly which config layer (and
therefore which database) a bare `br` command will resolve to.

## Related
- [[BeadsRedirectConvergence]] — a more general safety-contract pattern for consolidating multiple `.beads` redirects onto one canonical directory without corrupting the underlying store; this concept is the narrower "why you can't trust default discovery in the first place" precursor.
