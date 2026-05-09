---
title: "AND-Logic Modal Exit Guard Anti-Pattern"
type: concept
tags: [modal, guard, logic, anti-pattern]
---

Modal exit guards that require multiple conditions to be TRUE simultaneously (AND logic) create impossible states when one condition can be true without the other. Use OR logic when any single condition alone proves the modal should dismiss.

## Example

PR #6225 required BOTH `character_creation_in_progress=True` AND `character_creation_completed=True` to clear the CC modal. Templates start with `completed=False` (they skip manual creation), so the guard never fired — soft-locking template users.

## Rule

When writing modal exit guards:
1. Ask: "Is there a valid state where condition A is true but condition B is false?"
2. If yes, use OR (any true condition triggers exit)
3. AND is only correct when both conditions are always simultaneously true
4. Test the guard with the "only one condition true" state

## Related

- [[ModalAgentConstraint]] — modal entry/exit constraints
- [[AdminOverrideContract]] — admin overrides are common trigger for guard logic
- [[StaleFlag]] — the symptom when guards fail
