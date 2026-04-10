---
title: "NPC Tier Validation"
type: concept
tags: [validation, game-mechanic, npc]
sources: [narrative-response-social-hp-tests]
last_updated: 2026-04-08
---

**NPC Tier Validation** is the validation logic in [[narrative_response_schema.py]] that ensures Social HP Challenge data follows game design rules.

## Validation Rules
1. **Valid tier check**: npc_tier must be one of the defined tiers
2. **HP range check**: social_hp_max must fall within the tier's valid range
3. **Warning logging**: Invalid values trigger warnings via [[logging_util]]

## Tier Ranges
```
tier_ranges = {
    "commoner": (1, 2),
    "merchant": (2, 3),
    "guard": (2, 3),
    "noble": (3, 5),
    "knight": (3, 5),
    "lord": (5, 8),
    "general": (5, 8),
    "king": (8, 12),
    "ancient": (8, 12),
    "god": (15, 20),
    "primordial": (15, 20),
}
```

## Implementation
The `_validate_social_hp_challenge()` function performs these checks and logs warnings for:
- Invalid npc_tier values
- social_hp_max outside tier range (too high or too low)

## Related
- [[SocialHPChallenge]] — the feature being validated
- [[NarrativeResponse]] — schema containing the challenge
