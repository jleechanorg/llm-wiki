---
title: "STATE_UPDATES_PROPOSED"
type: concept
tags: [state-updates, legacy-pattern, json-mode]
sources: [json-mode-constants-tests]
last_updated: 2026-04-08
---

## Definition
STATE_UPDATES_PROPOSED was a marker used in character design narrative to instruct the system to update game state. This pattern has been deprecated in favor of JSON mode.

## History
- **Old pattern**: Include "[STATE_UPDATES_PROPOSED]" blocks in narrative text
- **New pattern**: State updates in JSON field, not narrative

## Related Concepts
- [[JSONMode]] — the new approach replacing this pattern
- [[CharacterDesignReminder]] — constant that was updated

## Transition
The CHARACTER_DESIGN_REMINDER constant was updated to remove "MANDATORY: Include [STATE_UPDATES_PROPOSED]" instructions and instead direct users to include state updates in a JSON field.
