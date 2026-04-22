---
title: "spawn-queue"
type: concept
tags: [agent-orchestrator, plugin, spawn, queue]
date: 2026-04-22
---

## Overview

`spawn-queue` is the proposed Phase 4 plugin for extracting spawn queue logic from `spawn.ts` (~100 LOC). Upstream has no spawn queue at all — the fork added queue management for spawn request throttling. This plugin preserves that functionality without embedding it in `spawn.ts`.

## Key Properties

- **What**: Plugin encapsulating spawn queue: `enqueueSpawnRequest()`, `resolveSpawnProjectId()`, queue management with configurable limits
- **Why it matters**: Spawn queue is purely fork-specific (upstream doesn't have queues). Extracting to plugin means upstream's `spawn.ts` changes never conflict with queue logic.
- **Slot**: `spawn-extension` (new slot type)
- **Interface**: `beforeSpawn`, `afterSpawn`, `queueRequest` hooks

## See Also

- [[lifecycle-skeptic]] — Phase 1 (extract before spawn)
- [[fork-plugin-refactor-design]] — Full design document
