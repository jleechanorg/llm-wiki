---
title: "Social HP Challenge"
type: concept
tags: [game-mechanic, social-interaction, npc]
sources: [narrative-response-social-hp-tests]
last_updated: 2026-04-08
---

The **Social HP Challenge** is a game mechanic in World Architect that tracks NPC resistance to player social interactions. Similar to combat HP, NPCs have social hit points that deplete as players use persuasion, deception, or intimidation skills.

## Structure
- **npc_name**: The NPC being challenged
- **npc_tier**: The NPC's social tier (determines HP range)
- **objective**: What the player is trying to achieve
- **social_hp**: Current HP remaining
- **social_hp_max**: Maximum HP based on tier
- **status**: Current state (e.g., RESISTING, CONVINCED)
- **skill_used**: The social skill used


## Tier Ranges
| Tier | HP Range |
|------|----------|
| commoner | 1-2 |
| merchant/guard | 2-3 |
| noble/knight | 3-5 |
| lord/general | 5-8 |
| king/ancient | 8-12 |
| god/primordial | 15+ |

## Related
- [[NarrativeResponse]] — schema containing social_hp_challenge field
- [[NPCTierValidation]] — validation of tier values
