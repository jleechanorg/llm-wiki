---
title: "Modal Agent Constraint"
type: concept
tags: [agent-routing, modal-agent, classifier]
sources: ["character-creation-level-up-mode"]
last_updated: 2026-04-08
---

System where certain agents (like [[CharacterCreationAgent]]) disable the normal semantic classifier and block access to other agents. User input cannot route to [[DialogAgent]], [[CombatAgent]], etc. while modal is active.

## Constraints During Character Creation
- Classifier disabled
- Only CharacterCreationAgent and GodModeAgent accessible
- User cannot escape via story-like inputs
- Level-up flows cannot be interrupted
