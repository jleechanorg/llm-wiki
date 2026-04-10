---
title: "Durable Session Metadata and Archive/Restore"
type: concept
tags: ["orchestration", "session", "persistence"]
sources: ["smartclaw-ao-exhaustive-audit-findings-file-level-sweep.md"]
last_updated: 2026-04-07
---

Architecture for persistent session state with archive and restore capabilities.

## AO Implementation
- `packages/core/src/session-manager.ts`
- `packages/core/src/metadata.ts`

## Gap
Current stack: partial session persistence and heartbeat tracking, but no AO-grade archive/restore path.

## Gap Closure
Bead ORCH-4yy: Session metadata + archive/restore parity in Python orchestration.

## Connections
- [[AgentOrchestrator]] — reference
- [[jleechanclaw]] — implementation target
