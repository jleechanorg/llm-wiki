---
title: "Gap Closure Program"
type: concept
tags: ["orchestration", "roadmap", "beads"]
sources: ["smartclaw-ao-exhaustive-audit-findings-file-level-sweep.md"]
last_updated: 2026-04-07
---

Systematic program to close capability gaps between current stack and AO reference.

## Epic Bead
- ORCH-a68: AO gap-closure program from exhaustive file audit

## Implementation Beads
- ORCH-ozi: AO-lite plugin kernel
- ORCH-4yy: Session metadata + archive/restore parity
- ORCH-zzd: Unified preflight gate
- ORCH-twf: Lifecycle reaction parity hardening
- ORCH-y7b: Integration test matrix
- ORCH-a68.1: Reconcile architecture docs

## TDD Beads
- ORCH-xoi: Plugin kernel contract tests
- ORCH-bvk: Session metadata/archive tests
- ORCH-4vi: Preflight matrix tests
- ORCH-czz: Lifecycle transition tests

## Dependency Wiring
- Each TDD bead blocks corresponding implementation bead
- ORCH-y7b depends on all implementation tracks
- ORCH-a68.1 blocks ORCH-orl

## Connections
- [[AgentOrchestrator]] — gap target
- [[mctrl]] — implementation target
- [[jleechanclaw]] — implementation target
