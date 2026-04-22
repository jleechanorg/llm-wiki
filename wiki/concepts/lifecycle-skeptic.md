---
title: "lifecycle-skeptic"
type: concept
tags: [agent-orchestrator, plugin, lifecycle, skeptic, upstream-integration]
date: 2026-04-22
---

## Overview

`lifecycle-skeptic` is the proposed first-phase plugin for the fork's plugin refactor. It extracts all skeptic-related code from `lifecycle-manager.ts` (~500 LOC) into a dedicated plugin package at `packages/plugins/lifecycle-skeptic/`. This is the single highest-impact extraction because skeptic integration accounts for ~500 of the ~1,000 LOC divergence in lifecycle-manager.ts.

## Key Properties

- **What**: Plugin that encapsulates all skeptic-review lifecycle behavior: `lastSkepticSha` tracking, `lastSkepticCommentId` tracking, `runSkepticReviewReaction`, `runLocalSkepticCron`, skeptic-comment methods, and skeptic reaction handlers (`skeptic-review`, `skeptic-trigger`, `skeptic-cr-approval-trigger`, `skeptic-first-seen-dispatch`)
- **Why it matters**: Without this plugin, every upstream lifecycle commit creates ~500 lines of merge conflicts in `lifecycle-manager.ts`. With it, conflicts reduce to ~5 lines of plugin registration.
- **Slot**: `lifecycle-extension` (new slot type)
- **Interface**: Hook-based — `onReaction`, `onPollCycle`, `onSessionStatusChange`

## Related Systems

| System | Type | Relevance |
|--------|------|-----------|
| [[skeptic-gate]] | Workflow | Skeptic runs via AO worker locally, not in GHA |
| [[lifecycle-manager]] | Core file | Source of ~500 LOC that this plugin extracts |
| [[fork-skeptic-extension]] | Fork module | Existing fork implementation that becomes plugin internals |
| [[agent-orchestrator-fork]] | Repo | The fork this plugin lives in |

## Connection to Upstream Integration

This plugin, when extracted, enables clean upstream import. Upstream changes to `lifecycle-manager.ts` only touch plugin registration code (~5 lines), not embedded skeptic logic (~500 lines). The acceptance criterion: upstream commit `f65e7d95` cherry-picks with no conflicts in `lifecycle-manager.ts`.

## See Also

- [[lifecycle-ao-action-log]] — Phase 2 plugin extraction
- [[scm-github-graphql]] — Phase 3 SCM plugin
- [[spawn-queue]] — Phase 4 spawn plugin
- [[fork-plugin-refactor-design]] — Full design document
