"title: "Lifecycle Reactions"
type: concept
tags: ["orchestration", "lifecycle", "events"]
sources: ["smartclaw-ao-exhaustive-audit-findings-file-level-sweep.md"]
last_updated: 2026-04-07
---

System for handling lifecycle events and reactions in orchestration.

## AO Implementation
- `packages/core/src/lifecycle-manager.ts`

## Current Stack
Lifecycle logic exists in `jleechanclaw/src/orchestration/lifecycle_reactions.py` but narrower on parity behaviors.

## Gap Closure
Bead ORCH-twf: Lifecycle reaction parity hardening (retry/escalation/all-complete)

## Connections
- [[AgentOrchestrator]] — reference
- [[jleechanclaw]] — existing implementation
