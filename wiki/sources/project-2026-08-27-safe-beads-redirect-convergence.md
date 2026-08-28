---
title: "Safe Beads redirect convergence is manifest-bound"
type: source
tags: [beads, issue-tracking, redirect, evidence, verification]
date: 2026-08-27
source_file: raw/project_2026-08-27_safe_beads_redirect_convergence.md
---

## Summary
A canonical-recovery investigation built a standalone redirect-convergence tool
(`apply_redirect_convergence.py`) that consolidates Beads worktree `.beads`
redirects onto a canonical target. The tool was certified against disposable
fixtures for real `--apply` behavior, but only ever ran dry-run against the
actual worldarchitect.ai topology — the canonical Beads store itself was never
mutated. The memory records the exact safety contract that makes such a
redirect tool safe to reuse, and the conditions under which it can (or cannot)
be ported to another repository.

## Key Claims
- A redirect-convergence tool is safe only when five conditions hold simultaneously: dry-run-by-default with `--apply` gated on the exact dry-run plan SHA-256; operator-supplied (not self-authorizing) manifest SHA-256 and canonical directory; redirect-file-only mutation with before/after fingerprinting of DB/WAL/SHM/JSONL members; backed-up redirect state with no-follow atomic writes, `br where --json --no-auto-flush --no-auto-import` as the resolution proof, and full rollback on failure; and real-store certification restricted to repeated dry-runs plus pre/post hashes, with actual `--apply` testing confined to fixtures.
- The tool has no hardcoded `worldarchitect.ai` path, but it is still Beads-specific: it depends on the `.beads` worktree layout, `beads.db`/`beads.db-wal`/`beads.db-shm`/`issues.jsonl` naming, the `beads.canonical-recovery.topology-audit.v1` schema, and `br where` as the verification authority.
- Cross-repository reuse is unproven until a second repository passes the fixture suite plus a real read-only dry-run with unchanged hashes — matching topology alone is not sufficient evidence.
- Verification evidence: fixture suite 11/11 PASS (covering apply gating, symlink rejection, nonregular-member rejection, lock contention, rollback, source immutability); two real dry-runs produced an identical plan SHA (`1d015ccb...`) with `applied=false`, 25 targets, 4 vanished worktrees skipped fail-closed; before/after snapshots showed 151 real paths unchanged (primary) and 72 relevant paths unchanged (independent Luna reproduction, no real `--apply`).
- Bead creation was deliberately withheld because `br sync --status --json` reported `workspace_health=degraded`, `dirty_count=3`, `db_newer=true` on 2026-08-27 — tracker mutations wait until that canonical export state is reconciled.

## Key Quotes
> "the manifest cannot authorize itself" — the operator, not the tool, must independently supply the expected manifest SHA-256 and canonical directory.
> "Cross-repository capability remains unproven until a second repository passes fixture tests plus a real read-only dry-run with unchanged hashes." — reuse claims require repeated independent proof, not architectural similarity.

## Connections
- [[Beads]] — the issue-tracking system this redirect tool operates on; extends Beads' operational-pattern notes with a redirect-safety contract.
- [[BeadsRedirectConvergence]] — new concept page capturing the generalized manifest-bound redirect-safety pattern.
