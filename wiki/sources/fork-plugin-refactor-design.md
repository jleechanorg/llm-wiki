---
title: "Fork Plugin Refactor Design — jleechanorg/agent-orchestrator"
type: source
tags: [agent-orchestrator, plugin-architecture, upstream-integration, merge-conflicts]
date: 2026-04-22
source_file: fork-plugin-refactor-design.md
---

## Summary

The fork jleechanorg/agent-orchestrator has accumulated ~3,739 lines of changes in `lifecycle-manager.ts`, ~2,079 lines in `scm-github/src/index.ts`, and ~106 lines in `spawn.ts` that create merge conflicts on every upstream import. This document designs a plugin-based refactor that pushes fork-specific behavior into dedicated plugins, keeping the fork's core as close to upstream as possible. Goal: reduce merge conflicts from ~2,000+ lines per import to under 100 lines (plugin registration only).

## Key Claims

- Fork's `lifecycle-manager.ts` is ~1,000 LOC larger than upstream (~3,032 vs ~2,077), almost entirely fork-specific: skeptic integration (~500 LOC), AO action logging (~200 LOC), session event tracking (~200 LOC), MCP mail (~100 LOC)
- Fork's `scm-github/src/index.ts` is 2.7x larger than upstream (~2,924 vs ~1,065 LOC): GraphQL queries (~400 LOC), skeptic comment retrieval (~150 LOC), comment enrichment with throttling (~300 LOC)
- Fork already uses companion module pattern (`fork-*.ts`) but these are imported and used inline in core files — converting to proper plugin packages eliminates conflict surface
- 8-plugin architecture proposed: lifecycle-skeptic, lifecycle-ao-action-log, lifecycle-agento-prefix, lifecycle-mcp-mail, scm-github-graphql, scm-github-skeptic, scm-github-comments, spawn-queue

## Key Quotes

> "The fork's lifecycle-manager.ts is ~1,000 LOC larger than upstream, but virtually all of that is either Skeptic integration (~500 LOC), AO action logging (~200 LOC), Session event tracking (~200 LOC), MCP mail (~100 LOC)." — fork-plugin-refactor-design.md §1.1

> "Most spawn divergence is queue-related. Upstream doesn't have spawn queues at all." — fork-plugin-refactor-design.md §1.3

## Connections

- [[lifecycle-skeptic]] — Plugin candidate: all skeptic-related code from lifecycle-manager.ts (~500 LOC)
- [[lifecycle-ao-action-log]] — Plugin candidate: logAoAction calls throughout lifecycle transitions (~200 LOC)
- [[scm-github-graphql]] — Plugin candidate: GraphQL-based detectPR() with REST fallback
- [[fork-divergence-analysis]] — Companion analysis: classifies each fork-*.ts module as fork-only, plugin-extractable, or upstream-candidate
- [[upstream-563-commit-import]] — Root cause: upstream import gap drives structural divergence
- [[PluginSlot]] — Existing plugin architecture that lifecycle extensions would extend

## Plugin Architecture

Proposed new slot type: `LifecycleExtension`
```typescript
type LifecycleExtension = {
  name: string;
  onSessionStatusChange?: (ctx: SessionContext, oldStatus, newStatus) => Promise<void>;
  onPollCycle?: (ctx: PollContext) => Promise<void>;
  onReaction?: (ctx: ReactionContext, reactionKey: string) => Promise<void>;
};
```

## Migration Phases

| Phase | Plugin | LOC Reduced | Files Touched |
|-------|--------|------------|---------------|
| 1 | lifecycle-skeptic | ~500 | lifecycle-manager.ts |
| 2 | lifecycle-ao-action-log | ~200 | lifecycle-manager.ts |
| 3 | scm-github-graphql + scm-github-skeptic | ~1,500 | scm-github/src/index.ts |
| 4 | spawn-queue | ~100 | spawn.ts |
| Total | 8 plugins | ~2,700 → ~80 | 4 core files |
