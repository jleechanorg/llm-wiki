---
name: Safe Beads redirect convergence is manifest-bound
description: Reuse the redirect-only transaction across Beads repositories only when the topology contract, canonical target, and immutable source proof are independently bound.
type: project
bead: none
---

# Safe Beads redirect convergence is manifest-bound

## Context

The canonical-recovery investigation produced a standalone redirect tool at
`/Users/jleechan/evidence/beads-canonical-recovery-20260827/apply_redirect_convergence.py`.
The task deliberately certified fixture apply behavior while running only dry-run
against the real topology. The canonical Beads store was not mutated.

## Rule

A redirect-convergence tool is safe only when all of these remain simultaneous:

1. Dry-run is the default; real writes require explicit `--apply` plus the exact
   dry-run plan SHA-256.
2. The operator independently supplies the expected manifest SHA-256 and expected
   canonical directory; the manifest cannot authorize itself.
3. Apply changes redirect files only. DB, WAL, SHM, and JSONL members are
   fingerprinted before and after and are never moved, deleted, rewritten, or
   chmodded.
4. Redirect state is backed up, writes use no-follow directory descriptors and
   atomic replacement, `br where --json --no-auto-flush --no-auto-import` proves
   resolution, and any failure rolls back every changed redirect.
5. Real-store certification uses repeated dry-runs and pre/post hashes. Apply
   testing is restricted to disposable fixtures. Multiple reviewers may inspect
   in parallel, but only one writer may touch shared canonical state.

## Cross-repository applicability

The current tool is reusable unchanged in another repository only when that
repository uses the same Beads contract:

- each worktree has a physical `<worktree>/.beads` directory;
- `br where` is the redirect-resolution authority;
- DB-family members use `beads.db`, `beads.db-wal`, `beads.db-shm`, and
  `issues.jsonl`;
- a trusted producer emits schema
  `beads.canonical-recovery.topology-audit.v1` with the supported classifications;
- the operator supplies that repository's exact canonical path and manifest hash.

No `worldarchitect.ai` path is hardcoded in the implementation. However, the
schema name, `.beads` layout, source filenames, eligible classifications, and
`br where` verification are Beads-specific. A different tracker or layout needs
a separate manifest adapter/schema and its own fixtures; do not weaken the
existing parser to accept ambiguous shapes. Cross-repository capability remains
unproven until a second repository passes fixture tests plus a real read-only
dry-run with unchanged hashes.

## Verification

- `python3 -m py_compile apply_redirect_convergence.py test_apply_redirect_convergence.py`: PASS.
- Fixture suite: 11/11 PASS, including explicit apply gating, source and redirect
  symlink rejection, nonregular-member rejection, lock contention, rollback, and
  source immutability.
- Two real dry-runs: identical plan SHA
  `1d015ccb262a07d746c3fc3e4c39a15890a76a7da2953fc85e51cf4e64e405aa`,
  `applied=false`, 25 targets, four vanished worktrees skipped fail-closed.
- Primary before/after snapshot: 151 real paths unchanged. Independent Luna
  reproduction: 72 relevant paths unchanged and no real `--apply`.
- Tool SHA-256:
  `bcf65f4cc8866c637887999d6f50fcda7557bfb555c65777a69c473a1aaf95f3`.
- Test SHA-256:
  `666243dd9d327b1a8213dab11a2e37167fbe100a1fd037f49ea14f34a06a035d`.

## Tracker status

Bead creation was intentionally withheld because `br sync --status --json`
reported `workspace_health=degraded`, `dirty_count=3`, and `db_newer=true` on
2026-08-27. Do not add tracker mutations until that canonical export state is
reconciled.
