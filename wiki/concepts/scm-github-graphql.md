---
title: "scm-github-graphql"
type: concept
tags: [agent-orchestrator, plugin, scm, github, graphql]
date: 2026-04-22
---

## Overview

`scm-github-graphql` is the proposed Phase 3 plugin for extracting GraphQL-based PR detection from `scm-github/src/index.ts` (~400 LOC). The fork uses GraphQL-based `detectPR()` with REST fallback, while upstream uses REST-only approach. This plugin encapsulates the fork's GraphQL enhancement as a composition layer over the base SCM.

## Key Properties

- **What**: Plugin that overrides SCM `detectPR()` to use GraphQL first with REST fallback on rate limit
- **Why it matters**: Fork's `scm-github/src/index.ts` is 2.7x larger than upstream (~2,924 vs ~1,065 LOC). GraphQL queries account for ~400 LOC of this divergence. Extracting to plugin reduces conflict surface dramatically.
- **Slot**: `scm` extension via method composition
- **Interface**: Extends base SCM with `enrichPR()` method using GraphQL, fallback to REST on rate limit

## Related Systems

| System | Type | Relevance |
|--------|------|-----------|
| [[scm-github]] | SCM file | Source of ~400 LOC GraphQL code this plugin extracts |
| [[fork-skeptic-extension]] | Fork module | Skeptic comment retrieval also in scm-github — separate plugin |
| [[agent-orchestrator-fork]] | Repo | The fork this plugin lives in |

## See Also

- [[lifecycle-skeptic]] — Phase 1 (extract first before SCM changes)
- [[fork-plugin-refactor-design]] — Full design document
