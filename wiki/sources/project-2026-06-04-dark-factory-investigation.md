---
title: "dark-factory Deletion Investigation (2026-06-04)"
type: source
tags: ["dark-factory", "ao-lifecycle", "prune-stale-worktrees", "agent-orchestrator", "pr-647"]
date: 2026-06-04
source_file: project_2026-06-04_dark_factory_investigation.md
---

## Summary
Investigation of reported dark-factory deletion — repo intact; root cause of May 29 incident confirmed as pruneStaleWorktrees bug in AO lifecycle worker. `worktree=/Users/jleechan/projects/worldarchitect.ai` made the main clone path the same as the worktree path; lifecycle worker treated it as stale worktree and deleted it.

## Key Claims
- Repo confirmed intact (HEAD `49c2276`, clean); no deletion occurred today
- May 29 root cause: AO lifecycle worker's `pruneStaleWorktrees` deleted `~/projects/worldarchitect.ai` because `wa-orchestrator` session had worktree=main clone path
- Fix: PR #647 MERGED 2026-05-29 — added `pruneWorktrees` config flag + main-worktree guard
- Gap: PR #642 CLOSED 2026-06-02 without merge — 'Pass 2' broader directory-skip logic. Verify coverage is complete or re-open
- Bead bd-diq

## Key Quotes
> Before setting up a new AO project, confirm `path != worktreeDir`. Run `ao doctor` after any new project config

## Connections
- [[DarkFactory]] — entity
- [[AOLifecycle]] — pruning concept
