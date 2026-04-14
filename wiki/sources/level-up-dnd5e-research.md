---
title: "Level-Up D&D 5e Research"
type: source
tags: [level-up, dnd-5e, xp, asi, mechanics]
date: 2026-04-14
source_file: /tmp/research_levelup_full.md
---

## Summary
D&D 5e level-up mechanics research for digital game platform implementation. Covers XP threshold calculations using cumulative XP storage with binary search lookup, ASI multiclass rules (total character level checked against each class's schedule independently), idempotent reward system design for deferred/batch awards, modal level-up UI patterns, and server-authoritative game state to prevent client manipulation.

## Key Claims

### XP Thresholds (Cumulative)
Store cumulative XP as integer; level is derived via lookup. Overflow XP is retained (never discarded).

| Level | Cumulative XP | Delta |
|-------|-------------|-------|
| 1 | 0 | — |
| 2 | 300 | 300 |
| 3 | 900 | 600 |
| 4 | 2,700 | 1,800 |
| 5 | 6,500 | 3,800 |
| … | … | … |
| 20 | 355,000 | — |

**Implementation**: Store `xpThresholds = [0,300,900,2700,6500,14000,23000,34000,48000,64000,85000,100000,120000,140000,165000,195000,225000,265000,305000,355000]`. Binary search for O(log n) lookup.

### ASI Multiclass Rule (Critical)
When a character gains a level in **any** class, check the **total character level** against the ASI schedule of **each** class.

**Algorithm**:
1. `total_level = sum(class_levels)` — NOT individual class level
2. For each class, check if total_level matches an ASI level for that class
3. If overlapping ASI at same total level (e.g., Fighter4/Cleric4 at total=8), player receives ONE ASI, not two

**ASI Levels by Class**:
- **Fighter**: 4, **6**, 8, 12, 14, 16, 19 (extra at 6, not just 4/8/12/14/16/19)
- **Rogue**: 4, 8, **10**, 12, 16, 19 (extra at 10, not just 4/8/12/14/16/19)
- **All other classes**: 4, 8, 12, 16, 19

**Example**: Fighter 6 / Rogue 10 at total level 16:
- Fighter ASI ≤ 16: 4, 6, 8, 12, 14, 16 → sixth Fighter ASI at 16
- Rogue ASI ≤ 16: 4, 8, 10, 12, 16 → fourth Rogue ASI at 16
- Character gains ONE ASI at level 16 (player chooses which class benefits)

### Idempotent Reward Design
For deferred/batch XP awards:
- Use `rewards_processed` flags to prevent double-counting
- rewards_engine must be **idempotent**: calling twice with same inputs = same outputs
- `DeferredRewardsProtocol` runs every 10 turns; idempotency prevents duplicate awards
- Guard against negative XP — treat as no-op

### Modal Level-Up UI Constraints
- User **cannot exit** until explicit finish choice selected
- `finish` option must be **last** in `planning_block.choices`
- World events **do not advance** while level-up modal is active
- `freeze_time: True` required on all synthesized choices

## Key Quotes

> "Store cumulative XP (an integer) rather than 'current-level XP'. The level is derived by a simple lookup or binary search over the threshold array." — Roll20 SRD

> "When a character gains a level in any class, you check the total character level against the ASI schedule of each class the character possesses." — PHB Multiclassing Rules

> "Overflow XP is retained for the next level (e.g., a character at 2,900 XP [level 3] gains 400 XP → total 3,300 XP, still level 3, with 400 XP toward level 4)." — Research finding

## Sources
- [Roll20 SRD: Experience Points and Level Advancement](https://roll20.net/compendium/dnd5e/Experience%20Points%20and%20Level%20Advancement#content)
- [Roll20 SRD: Ability Score Improvement](https://roll20.net/compendium/dnd5e/Ability%20Score%20Improvement#content)
- [Roll20 SRD: Multiclassing](https://roll20.net/compendium/dnd5e/Multiclassing#content)

## Connections
- [[LevelUpMechanics]] — core level-up process
- [[AbilityScoreImprovement]] — ASI with class-specific levels
- [[RewardsEngineIdempotency]] — idempotent design for deferred rewards
- [[LevelUpModalRouting]] — modal constraints
- [[SingleResponsibilityPipeline]] — server-authoritative architecture
