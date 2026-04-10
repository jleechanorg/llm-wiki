---
title: "Lady Vex"
type: entity
tags: [npc, named-npc, assassin]
sources: [npc-death-state-persistence-tdd-tests]
last_updated: 2026-04-08
---

## Context
A named NPC in the test suite for death state persistence. A mysterious assassin from the eastern kingdoms who can be killed in combat.

## Test Reference
Referenced in `test_named_npc_with_backstory_marked_dead_not_deleted` as a named NPC with backstory that should be preserved with status: ["dead"] when hp_current reaches 0.

## Related
- [[Marcus]] — another named NPC tested for death state preservation
- [[NPC Death State Persistence TDD Tests]] — source tests
