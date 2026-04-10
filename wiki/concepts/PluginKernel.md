---
title: "Plugin Kernel and Registry Model"
type: concept
tags: ["orchestration", "architecture", "plugin"]
sources: ["smartclaw-ao-exhaustive-audit-findings-file-level-sweep.md"]
last_updated: 2026-04-07
---

Architecture pattern for runtime plugin loading and registration. AO has typed runtime registry; Python orchestration lacks equivalent.

## AO Implementation
- `packages/core/src/plugin-registry.ts`
- `packages/core/src/types.ts`

## Gap
Current stack: no equivalent typed runtime registry in Python orchestration.

## Gap Closure
Bead ORCH-ozi: AO-lite plugin kernel with typed contracts + runtime plugin loader.

## Connections
- [[AgentOrchestrator]] — reference
- [[mctrl]] — implementation target
