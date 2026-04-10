---
title: "Action Resolution Protocol"
type: concept
tags: [game-mechanics, player-actions, resolution]
sources: [narrative-directives]
last_updated: 2026-04-08
---

## Description
Protocol for processing player-declared outcomes without rejection. When players declare outcomes ("The king agrees", "It kills the guard"), the system interprets as attempts, resolves via appropriate mechanics, audits in JSON, and narrates the actual result.

## Steps
1. **Interpret**: Identify the underlying attempt from the declared outcome
2. **Resolve**: Use appropriate mechanics (combat, social, exploration)
3. **Audit**: Document in `action_resolution` JSON field
4. **Narrate**: Describe actual outcome, not declared outcome

## Key Principle
Zero rejections - always process and resolve player-declared outcomes.

## Related Concepts
- [[Tabletop DM Test]]
- [[SocialHP]]
- [[CombatMechanics]]
