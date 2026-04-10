---
title: "Merge Conflict Resolution"
type: concept
tags: [git, merge, conflict-resolution]
sources: [conflict-resolution-pr-3902]
last_updated: 2026-04-08
---

## Description
The process of reconciling divergent changes between git branches during a merge operation. Involves choosing which version of conflicting code to keep, or combining elements from both branches.

## Resolution Strategies Used
- **Accept main's version:** When main has structural improvements (context managers, error handling) that PR lacks
- **Merge/append:** When both branches have complementary additions that can coexist
- **Concatenate:** When merging lists or collections from both branches

## Key Principles
1. Infrastructure patterns (context managers) preferred over ad-hoc solutions
2. Functional logic (evidence saving) prioritized over template updates
3. No forced choices when concatenation works

## Related Concepts
- [[ContextManagers]] — Python pattern used for resource management
- [[EvidencePreservation]] — Cross-process test evidence strategy
- [[GitBranch]] — Branching strategy and merge workflows
