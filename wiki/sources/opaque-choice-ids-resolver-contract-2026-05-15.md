---
title: "Opaque Choice IDs Need Resolver Contract"
type: source
tags: [worldarchitect-ai, choice-contract, tdd, zfc, pr-6906]
date: 2026-05-15
source_file: raw/feedback_2026-05-15_opaque_choice_ids_need_resolver_contract.md
sources: []
last_updated: 2026-05-15
---

## Summary

For PR6906 opaque choice-ID migration, do not fix drift by adding semantic
intent or ID-prefix reads to backend correction guards and modal scrubbers.
Start with RED contract tests, then implement the schema and selected-choice
resolver boundary. Keep correction guards narrow and compatibility-only.

## Key Rule

`planning_block.choices[].id` should be an opaque exact-selection handle. New
semantic ownership belongs in explicit fields such as `intent`, `execution`, and
`ui`, plus a resolver that maps `{planning_block_id, choice_id}` against the
persisted planning block.

## Connections

- [[PlanningChoice]]
- [[PlanningBlock]]
- [[ArchitecturalBoundaries]]
- [[Red-Green-Refactor]]
- [[ChoiceIdPrefix]]

## Metadata

- **Project**: `/Users/jleechan/projects/worktree_level_choices`
- **PR**: https://github.com/jleechanorg/worldarchitect.ai/pull/6906
- **Bead**: `rev-tn2mr`
- **Affects [[jeffrey-oracle]]**: No. This is engineering workflow and protocol-boundary discipline.

