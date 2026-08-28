---
title: "BeadsRedirectConvergence"
type: concept
tags: [beads, issue-tracking, redirect, safety-contract, verification]
sources: [project-2026-08-27-safe-beads-redirect-convergence]
last_updated: 2026-08-27
---

## Overview
Beads Redirect Convergence is the safety pattern for a tool that consolidates
multiple Beads worktree `.beads` redirects onto one canonical directory
without ever mutating the canonical DB/WAL/SHM/JSONL store. It generalizes a
2026-08-27 canonical-recovery investigation that built
`apply_redirect_convergence.py`, certified its real `--apply` path only
against disposable fixtures, and ran only dry-run against the actual
worldarchitect.ai topology.

## The Five-Part Safety Contract
A redirect-convergence tool is safe only when all five hold at once:
1. **Dry-run default, gated apply** — real writes require explicit `--apply`
   plus the exact dry-run plan SHA-256, so an apply can't silently diverge
   from the plan it was reviewed against.
2. **Operator-supplied authorization** — the expected manifest SHA-256 and
   canonical directory come from the operator, never from the manifest
   itself; a manifest can't authorize its own trust.
3. **Redirect-file-only mutation** — DB, WAL, SHM, and JSONL members are
   fingerprinted before and after and are never moved, deleted, rewritten,
   or chmodded. The blast radius is the redirect pointer, not the store.
4. **Atomic, provable, reversible writes** — redirect state is backed up,
   writes use no-follow directory descriptors and atomic replacement,
   `br where --json --no-auto-flush --no-auto-import` proves resolution, and
   any failure rolls back every changed redirect.
5. **Fixture-isolated apply testing** — real-store certification uses
   repeated dry-runs plus pre/post hashes only; actual `--apply` testing is
   confined to disposable fixtures. Multiple reviewers may inspect the same
   real state in parallel, but only one writer may touch shared canonical
   state.

## Cross-Repository Portability Boundary
The tool has no hardcoded `worldarchitect.ai` path, but "no hardcoded path"
is not the same as "portable." It still depends on Beads-specific contract
elements: a physical `<worktree>/.beads` directory per worktree, `br where`
as the sole redirect-resolution authority, the `beads.db` /
`beads.db-wal` / `beads.db-shm` / `issues.jsonl` naming family, and a trusted
producer emitting the `beads.canonical-recovery.topology-audit.v1` schema.
Porting to a repository with a different tracker or `.beads` layout requires
a new manifest adapter/schema and its own fixtures — the parser must not be
weakened to accept ambiguous shapes to fit a second repo.

**Portability is proven only by repetition, not architecture match**: a
second repository counts as validated only after it passes the fixture
suite *and* a real read-only dry-run with unchanged before/after hashes.
Matching topology alone is an untested hypothesis.

## Evidence Pattern
The 2026-08-27 certification combined four independent verification layers:
compile-check, a fixture suite (11/11 PASS across apply gating, symlink
rejection, nonregular-member rejection, lock contention, rollback, and
source immutability), two real dry-runs on the live topology that produced
an *identical* plan SHA-256 (`1d015ccb...`, `applied=false`, 25 targets, 4
vanished worktrees skipped fail-closed), and an independent reproduction
(Luna) confirming 72 relevant real paths unchanged. Tracker (bead) creation
was withheld because `br sync --status --json` showed
`workspace_health=degraded` at the time — mutations wait for a reconciled
canonical export state.

## Related Concepts
- [[Beads]] — the underlying issue-tracking system and its operational
  patterns (executable follow-up beads, priority conventions).
