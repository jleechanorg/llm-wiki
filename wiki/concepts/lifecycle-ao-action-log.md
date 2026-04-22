---
title: "lifecycle-ao-action-log"
type: concept
tags: [agent-orchestrator, plugin, lifecycle, action-logging]
date: 2026-04-22
---

## Overview

`lifecycle-ao-action-log` is the proposed Phase 2 plugin for extracting all `logAoAction` calls from `lifecycle-manager.ts` (~200 LOC) into a dedicated plugin. The plugin logs AO actions (session kills, PR merges, session absorptions) keyed by status transitions, providing an audit trail for fork operations.

## Key Properties

- **What**: Plugin that calls `logAoAction()` on lifecycle status transitions (killed, merged, absorbed, etc.)
- **Why it matters**: `logAoAction` calls are scattered throughout lifecycle transitions but are purely fork-instrumentation — not upstream-compatible. Extracting them to a plugin keeps them out of core while preserving functionality.
- **Slot**: `lifecycle-extension` (new slot type)
- **Interface**: `onSessionStatusChange` hook — calls `logAoAction` when status transitions to key states

## Related Systems

| System | Type | Relevance |
|--------|------|-----------|
| [[lifecycle-manager]] | Core file | Source of ~200 LOC logAoAction calls this plugin extracts |
| [[lifecycle-skeptic]] | Plugin | Phase 1 companion — extract skeptic before action-log |
| [[agent-orchestrator-fork]] | Repo | The fork this plugin lives in |

## See Also

- [[lifecycle-skeptic]] — Phase 1 (higher priority)
- [[fork-plugin-refactor-design]] — Full design document
