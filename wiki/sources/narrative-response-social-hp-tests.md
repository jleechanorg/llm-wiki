---
title: "Narrative Response Social HP Tests"
type: source
tags: [python, testing, social-hp, validation, narrative-response, tdd]
source_file: "raw/test_narrative_response_social_hp.py"
sources: []
last_updated: 2026-04-08
---

## Summary
TDD tests for Social HP Input→Output Mapping and Validation Logic in [[narrative_response_schema.py]]. Tests validate NPC tier extraction from npc_data, tier-based social_hp_max calculation, and strict enforcement of valid tier ranges with warning logs.

## Key Claims
- **NPC tier extraction**: npc_tier can be extracted from npc_data.<name>.tier input
- **Tier-based HP calculation**: social_hp_max follows tier-based calculation rules from game_state_instruction.md
- **Invalid tier warning**: Invalid NPC tier triggers warning log
- **HP range validation**: social_hp_max above/below tier range triggers warning

## Key Quotes
> "commoner=1-2, merchant/guard=2-3, noble/knight=3-5, lord/general=5-8, king/ancient=8-12, god/primordial=15+"

## Connections
- [[narrative_response_schema.py]] — source file under test
- [[NarrativeResponse]] — schema class being validated
- [[SocialHPChallenge]] — structured field concept
- [[NPCTierValidation]] — validation concept

## Contradictions
- None identified
