---
title: "Choice ID Prefix"
type: concept
tags: [god-mode, choices, naming-convention, legacy-compatibility]
sources: [god-mode-planning-blocks-tests, opaque-choice-ids-resolver-contract-2026-05-15]
last_updated: 2026-05-15
---

## Definition
Naming convention requiring all God mode choice IDs to use the "god:" prefix.

## Examples
- god:plot_arc_1
- god:return_story
- god:custom_direction

## Purpose
Distinguishes God mode choices from regular story choices in the frontend.

## Compatibility Note

For the PR6906 opaque choice-ID migration, prefix-based meaning should be treated
as legacy compatibility unless a mode explicitly owns that syntax. New planning
choice semantics should move to explicit schema fields and selected-choice
resolver output rather than correction scrubbers reading prefixes.

## Related Concepts
- [[PlanningBlock]] — Container for choices
- [[OpaqueChoiceIdContract]] — newer boundary for opaque planning choice IDs
- [[God Mode Return Story]] — Mandatory choice for exiting God mode

## Source
Derived from [[God Mode Planning Blocks Tests]]
