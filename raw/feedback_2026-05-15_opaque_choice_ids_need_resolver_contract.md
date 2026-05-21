---
name: PR6906 opaque choice IDs need resolver contract, not semantic scrubbers
description: Do not repair opaque choice-ID migration by teaching guards to read semantic intent or ID prefixes.
type: feedback
bead: rev-tn2mr
---

## Context

On 2026-05-15 in `/Users/jleechan/projects/worktree_level_choices`,
the user corrected an implementation drift during PR6906 opaque choice-ID work.
The original goal was to make `planning_block.choices[].id` an opaque exact
selection handle and clean up downstream boundaries. The drift was expanding an
active-modal correction scrubber with semantic intent and ID-prefix logic.

Related PR: https://github.com/jleechanorg/worldarchitect.ai/pull/6906
Related planning beads: `rev-1xi0m`, `rev-sjjbm`, `rev-t28fa`, `rev-87qay`,
`rev-usunn`, `rev-isjza`.

## Technical Detail

Opaque choice IDs fail if backend correction guards, modal scrubbers, or rewards
classifiers keep treating `choice.id` as semantic evidence. Adding checks such
as `id.startswith("level_up_")`, exact ID lists, or guard-side reads of
`intent.domain` can make one symptom green while preserving the wrong boundary:
the correction layer starts deciding what the selected choice means.

For this migration, the intended architecture is:

- `choice.id` is an opaque protocol handle for exact selection.
- Semantic fields live in explicit schema-owned fields such as `intent`,
  `execution`, and `ui`.
- A selected-choice resolver maps `{planning_block_id, choice_id}` against the
  persisted planning block and produces the server-side action payload.
- Narrow correction guards enforce invariants only after the resolver/schema
  contract has done the semantic work.

## Rule

When opaque choice IDs are the goal, do not repair by teaching backend
correction guards or scrubbers to read semantic intent or ID prefixes. First
separate RED contract tests from GREEN implementation, keep correction guards
narrow, and route the migration through an explicit selected-choice
resolver/schema contract.

## Verification Pattern

Start with failing contract tests before production changes:

1. Schema RED: planning choices preserve explicit `intent`, `execution`, and
   `ui` fields while using opaque IDs.
2. API/Layer 2 RED: structured `selected_choice` payload resolves by
   `planning_block_id` and `choice_id`, not by visible text or semantic ID.
3. Level-up RED: modal entry, feature selection, HP/ASI/finish, and ordinary
   story choices are distinguished by explicit schema/resolver output, not by
   ID prefixes.
4. Compatibility RED: legacy `CHOICE:<id>` and persisted semantic IDs remain
   supported only as migration compatibility.
5. `/es` GREEN: real local server, real LLM/services where applicable,
   persisted post-finish `game_state`, raw request/response logs, and browser
   video when frontend submission behavior changes.

## Reusable Pattern

For protocol migrations, separate the ownership layers:

- Contract tests define the new boundary.
- Schema and resolver implement semantic ownership.
- Guards correct only invalid state after ownership is clear.
- Legacy semantic tokens remain explicit compatibility, not the new source of
  truth.

