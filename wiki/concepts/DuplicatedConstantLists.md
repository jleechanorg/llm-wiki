---
title: "Duplicated Constant Lists Anti-Pattern"
type: concept
tags: [architecture, duplication, merge-rebase, anti-pattern]
---

Duplicated constant lists across files are a merge-rebase bomb. When two files define the same list independently, a rebase can update one copy without updating the other, causing NameError or stale-field bugs. The fix is a single source of truth in a shared module.

## Example

PR #6308 fractured Living World stripping logic across `world_logic.py` and `llm_parser.py` with duplicated inline tuples of cooldown field names. During a rebase, one variable name drifted (`_cooldown_lw_fields_resp` vs `_cooldown_lw_fields`), causing a fatal NameError. PR #6839 fixed this by moving all logic to `living_world_contract.py`.

## Rule

Any list of fields/constants used in multiple files must be defined ONCE in a shared module and imported. Never duplicate inline tuples across files, even temporarily.

## Related

- [[LivingWorldProtocol]] — LW field handling
- [[SingleResponsibilityPrinciple]] — single source of truth
- [[MergeConflictResolution]] — why duplication causes rebase failures
