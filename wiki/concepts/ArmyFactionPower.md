---
title: "Army Faction Power"
type: concept
tags: [game-mechanics, military, calculation]
sources: ["faction-power-rankings-system", "living-world-tick-9139"]
last_updated: 2026-08-19
---

## Unit Power Weights

Military component of faction power. Soldiers contribute 1.0× their count, spies contribute 0.5× (combat penalty), and elites contribute 3.0× with a level bonus of +10% per level above 6.

## Conflict Resolution — Simultaneous Raids

When two or more factions raid the same target in the same tick (added 2026-08-19 per Reviewer A gap in [living-world-tick design doc](https://github.com/jleechanorg/worldarchitect.ai/blob/main/docs/plans/2026-08-19-living-world-tick-design.md)):

- Each faction commits **50% of intended force** to the combined assault.
- Target takes the **sum of remaining damage** from each simultaneous attacker.
- Each attacking faction loses units in proportion to the share of damage they contributed (no free-riders).
- Detection risk: each attacker's individual detection check resolves independently; multiple factions being detected in the same tick does not compound.

**Example:** Faction A raids target with 100 soldiers (intends to commit all 100). Faction B raids same target with 60 soldiers (intends to commit all 60). Effective: A commits 50, B commits 30; target takes A_damage + B_damage; A loses ~50/(50+30) = 62.5% of combined casualties, B loses 37.5%.

This rule must be deterministic (no LLM interpretation) and is enforced server-side in `mvp_site/world_sim/event_writer.py`. Contract test: `mvp_site/tests/test_world_sim_simultaneous_raid.py`.