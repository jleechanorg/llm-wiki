---
title: "Opaque Choice ID Contract"
type: concept
tags: [worldarchitect-ai, planning-block, schema, protocol-boundary]
sources: [opaque-choice-ids-resolver-contract-2026-05-15]
last_updated: 2026-05-15
---

## Definition

The contract that `planning_block.choices[].id` is an opaque exact-selection
handle, not a semantic routing token.

## Rule

When migrating toward opaque choice IDs, semantic meaning belongs in explicit
schema fields and resolver output. Backend correction guards and modal scrubbers
must not become the semantic classifier by reading ID prefixes or intent fields
to infer action meaning.

## Implementation Boundary

- `id`: stable handle for selecting one persisted choice.
- `intent`, `execution`, `ui`: explicit model/schema-owned semantics.
- selected-choice resolver: maps `{planning_block_id, choice_id}` to the
  server-side action payload.
- correction guards: narrow invariant repair only, after the resolver/schema
  contract has produced the action.

## Related Concepts

- [[PlanningChoice]]
- [[PlanningBlock]]
- [[ArchitecturalBoundaries]]
- [[Red-Green-Refactor]]
- [[ChoiceIdPrefix]]
## Scope Boundary From PR6906 (2026-05-17)

Opaque choice-ID migration is staged architecture work, not a tail fix for a level-up guard PR. If an active PR is already retaining backend correction guards or rerunning `/es` for moving-head evidence, do not fold full opaque-ID schema/resolver migration into that same PR. Split it into its own contract PR with RED schema/resolver tests first.

