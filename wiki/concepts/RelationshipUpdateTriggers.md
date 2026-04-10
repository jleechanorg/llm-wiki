---
title: "Relationship Update Triggers"
type: concept
tags: [game-mechanics, npc-relationships, triggers, dnd]
sources: ["relationship-mechanics-detailed"]
last_updated: 2026-04-08
---

## Description
Mandatory events that require updating NPC relationship data AFTER significant player actions.

## Update Actions and Effects

| Action | Trust Change | Required Updates |
|--------|---------------|-------------------|
| Save NPC's life | +3 to +5 | Add to history, add debt |
| Keep a promise | +1 to +2 | Add to history |
| Break a promise | -2 to -3 | Add to grievances |
| Betray NPC | -4 to -6 | Add to grievances, may remove debts |
| Give significant gift | +1 to +2 | Add to history |
| Steal from NPC | -2 to -4 | Add to grievances |
| Insult or threaten | -1 to +3 | Add to grievances |
| Defend NPC's reputation | +1 to +2 | Add to history |
| Share valuable secret | +1 to +2 | Add to history |
| Help with NPC's personal goal | +2 to +4 | Add to history, may resolve grievance |
| Ignore NPC's request for help | -1 to -2 | Add to grievances |
| Kill NPC's friend/ally | -3 to -6 | Add to grievances, may turn hostile |

## Usage
Record all updates in `state_updates` as JSON. Updates trigger [[Relationship Check Triggers]] on subsequent NPC interactions.

## Related Concepts
- [[Trust Level Scale]] — Values being modified
- [[Relationship Behavior Modifiers]] — Effect of changes
- [[Relationship Memory Protocol]] — What's recorded
