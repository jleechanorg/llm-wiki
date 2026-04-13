---
title: "Social HP (Skill Challenges)"
type: concept
tags: [game-mechanics, social, skill-challenges]
sources: [narrative-directives]
last_updated: 2026-04-08
---

## Description
Skill challenge system for social interactions. Triggered when a human DM would say "that won't work with one roll" - requires multiple successful checks to overcome NPC resistance.

## NPC Tier HP Scaling
| Tier | HP Range |
|------|----------|
| Commoner | 1-2 |
| Merchant/Guard | 2-3 |
| Noble/Knight | 3-5 |
| Lord/General | 5-8 |
| King | 8-12 |
| God | 15+ |

## Request Difficulty Multiplier
- "Teach me" / "Alliance": 1x base HP
- "Betray beliefs": 2x base HP
- "Submit/Surrender": 3x base HP

## Display Requirement
EVERY social HP challenge interaction MUST show [SOCIAL SKILL CHALLENGE: NPC] box with Objective/HP/Status - shown every turn, not just first.

## V6 Nocturne Social HP System
In [[nocturne-bg3-v6-bug-repro-test]], Nocturne uses Siren's Gaze to deplete target Social HP. The system tracks target resistance through multiple turns:

| Target | Social HP | Status | Appears In |
|--------|-----------|--------|------------|
| Minthara | 30 | Yielded in Scene 7 | [[nocturne-bg3-v6-bug-repro-test-entry-007]] |

**Mechanic Flow:**
1. **Siren's Gaze** — Primary social attack, depletes target's Social HP pool
2. **Social HP Depletion** — Each successful Charisma check reduces Social HP
3. **Yield** — When Social HP reaches 0, target surrenders to Nocturne's influence
4. **Gilded Tether** — After yield, can bind target as Thrall

## V5-V6 Comparison
The V6 system is more aggressive than the generic skill challenge rules above. In V6:
- Minthara's 30 Social HP was tracked across 4 scenes before yielding
- Multiple companion assets (Astarion, Lae'zel, Shadowheart) were involved in the social encounter
- Social HP correlated with the [[RiteOfThorns]] subversion plan

## Related Concepts
- [[SirensGaze]] -- ability that depletes Social HP
- [[GildedTether]] -- uses depleted Social HP for thrall binding
- [[CollegeOfTheAbyssalSiren]] -- subclass using this mechanic
- [[CompanionAssetFramework]] -- V6 companion tracking system

## Related Entities
- [[NocturneSosuke]] -- primary user of Social HP attacks
- [[Minthara]] -- primary target with 30 Social HP
- [[BG3Companions]] -- affected by social mechanics

## Appearances
- [[nocturne-bg3-v6-bug-repro-test]] -- Minthara's Social HP tracked in Scenes 4-7
- [[nocturne-bg3-v5]] -- basic social combat integration
- [[nocturne-bg3-v5-succubus]] -- Thrall system linked to Social HP
