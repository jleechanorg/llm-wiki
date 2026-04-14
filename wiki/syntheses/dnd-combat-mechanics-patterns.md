---
title: "D&D 5e Combat Mechanics — Cross-Campaign Patterns"
type: synthesis
tags: [dnd-5e, combat, mechanics, action-resolution, battle-simulation]
sources: [concepts/ActionResolution, concepts/AttackRoll, concepts/AdvantageDisadvantage, concepts/Attunement, concepts/Alignment, concepts/AbilityScoreImprovement]
last_updated: 2026-04-14
---

## Summary

The wiki documents extensive D&D 5e mechanical implementation across worldarchitect.ai: action resolution protocols, attack roll systems, advantage/disadvantage stacking, attunement constraints, and ability score improvement progressions. Cross-campaign analysis reveals consistent mechanical patterns around dice authenticity, combat morale routing, and the distinction between fast/detailed/deterministic battle simulation modes.

## Key Insights

### 1. Action Resolution Protocol

[[ActionResolution]] is a core concept: the AgentAdapter property `requires_action_resolution` affects how the streaming parse path handles responses. This is critical for the level-up bug chain — action resolution in the streaming path bypasses postcondition enforcement that the unified path runs.

The [[ActionResolutionProtocol]] defines the semantic routing between:
- Dice roll extraction (audit events)
- Narrative response integration
- Level-up trigger detection

### 2. Advantage/Disadvantage Stacking Rules

[[AdvantageDisadvantage]] mechanics in D&D 5e:
- Multiple advantages don't stack — roll once with advantage
- Multiple disadvantages cancel advantage (not stack)
- Situational advantage from Bardic Inspiration, subclass features, spells
- The [[SRD-Battle-Simulation]] implements three modes: fast (single roll), detailed (full advantage calculation), deterministic (preset outcomes for testing)

### 3. Attunement Constraints

[[Attunement]] limits:
- 3 items maximum attuned at once (5e RAW)
- Attunement requires short rest (usually)
- Some items require specific classes or alignments
- WorldArchitect implementation: [[Attunement]] tracked in game state, enforced on equip action

The [[AegonTargaryen]] campaign uses attunement as narrative constraint — dragon-bonded characters can't attune other legendary items.

### 4. Ability Score Improvement Progression

[[AbilityScoreImprovement]] and [[AbilityScores]]:
- Standard array: 15, 14, 13, 12, 10, 8
- Point buy systems for campaign flexibility
- Level 4, 8, 12, 16, 19 ASI/half-feat progression
- [[LevelUpBug]] chain specifically involves XP → ability score progression calculation bugs

### 5. Battle Simulation Modes

The [[SRD-Battle-Simulation]] module implements three [[SimulationModes]] configurations:

| Mode | Use Case | Roll Behavior |
|------|----------|---------------|
| Fast | Quick encounters | Single d20 + modifiers |
| Detailed | Boss fights | Full advantage calculation, morale checks |
| Deterministic | Testing/regression | Fixed rolls for reproducible results |

Morale routing: enemy groups can yield, flee, or fight based on leadership casualties — implemented via faction power calculations in [[ArmyFactionPower]].

### 6. Dice Roll Audit Trail

[[AuditEventExtraction]] captures dice rolls as structured audit events:
- Roll formula (e.g., "1d20+5")
- Natural roll vs. modified result
- Advantage/disadvantage applied
- Context (attack, save, ability check)

The [[DiceRollDebugRegression]] (same pattern as FrontendRewardsBoxGate) — backend emits correct roll data but frontend gates it on `debugMode`.

## Connections

- [[ActionResolution]] — the agent property affecting parse path
- [[AttackRoll]] — d20 + modifiers + advantage/disadvantage
- [[AdvantageDisadvantage]] — stacking rules
- [[Attunement]] — 3-item limit, short rest requirement
- [[AbilityScores]] — standard array, point buy, ASI progression
- [[SRD-Battle-Simulation]] — three-mode system
- [[AuditEventExtraction]] — structured roll capture
- [[LevelUpBug]] — XP/ASI calculation bugs
