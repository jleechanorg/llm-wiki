---
title: "Rewards Box Schema"
type: concept
tags: [rewards, schema, pydantic, validation, worldai]
last_updated: 2026-04-14
---

## Summary

The RewardsBox schema defines the canonical structure for storing player rewards state. It must be normalized before persistence — see [[StreamingPassthroughNormalization]].

## Schema Definition

```python
from pydantic import BaseModel, Field
from typing import Literal
from datetime import datetime

class RewardsBox(BaseModel):
    campaign_id: str
    player_id: str
    total_rewards: float = Field(ge=0, le=1_000_000)
    level: int = Field(ge=1, le=20)
    xp: float = Field(ge=0)
    xp_to_next_level: float
    rewards_history: list[RewardEvent] = Field(default_factory=list)

    # Source tracking
    source: Literal["level_up", "dice_roll", "achievement", "gm_grant"]
    last_updated: datetime

    class Config:
        frozen = False  # Allow mutations

class RewardEvent(BaseModel):
    amount: float
    source: str
    timestamp: datetime
    narrative: str | None = None  # LLM-generated explanation
```

## Normalization Rules

Before persisting to Firestore, all RewardsBox instances must pass through `normalize_rewards_box_for_ui()`:

1. Clamp `total_rewards` to [0, MAX_REWARDS]
2. Clamp `level` to [1, 20]
3. Ensure `xp_to_next_level` > 0
4. Sort `rewards_history` by timestamp ascending

## Connections
- [[RewardsBoxAtomicity]] — Atomic update semantics
- [[RewardsBoxObservability]] — Observability patterns
- [[StreamingPassthroughNormalization]] — Normalization in streaming path
- [[CentralizedNumericExtraction]] — Numeric extraction from LLM
