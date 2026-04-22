---
title: "FastAPI Type Safety"
type: concept
tags: [fastapi, python, types, pydantic, validation]
last_updated: 2026-04-14
---

## Summary

FastAPI provides built-in type safety through Pydantic models and Python's type hints. Leveraging this fully requires consistent use of type annotations, Optional defaults, and discriminated unions for response variants.

## Core Patterns

**Pydantic request models**:
```python
from pydantic import BaseModel, Field

class RewardsBoxRequest(BaseModel):
    campaign_id: str
    player_id: str
    delta: float = Field(ge=0, le=MAX_REWARDS)
    source: Literal["level_up", "dice_roll", "achievement"]
```

**Discriminated unions for response variants**:
```python
from pydantic import Discriminator

class SuccessResponse(BaseModel):
    status: Literal["ok"]
    data: RewardsBox

class ErrorResponse(BaseModel):
    status: Literal["error"]
    code: str
    detail: str

Response = Annotated[Union[SuccessResponse, ErrorResponse], UnionDiscriminator("status")]
```

**Generic route handlers**:
```python
@app.get("/campaign/{campaign_id}", response_model=CampaignResponse)
async def get_campaign(campaign_id: str) -> Campaign:
    return await campaign_service.get(campaign_id)
```

## Why Type Safety Matters

1. **Pydantic validation** — Automatic input sanitization
2. **OpenAPI schema** — Auto-generated API docs
3. **Editor support** — Autocomplete for request/response shapes
4. **Refactoring safety** — Type errors caught at edit time

## Connections
- [[APIDesign]] — General API design principles
- [[FastAPIErrorHandling]] — Error handling in FastAPI
- [[tRPCTypeSafety]] — Type-safe API alternative (TypeScript)
