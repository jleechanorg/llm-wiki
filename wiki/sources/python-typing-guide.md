---
title: "Python Typing Guide for WorldArchitect.AI"
type: source
tags: [python, typing, mypy, type-hints, pep-484]
source_file: "raw/python-typing-guide.md"
sources: []
last_updated: 2026-04-08
---

## Summary
Comprehensive type annotation standards and practices for WorldArchitect.AI codebase using Python's type hints (PEP 484) with a gradual typing approach. Covers mypy configuration, custom type definitions, Flask route typing, service methods, Firebase/Firestore operations, and Pydantic models.

## Key Claims
- **Gradual Typing Strategy**: Start with critical modules, add types to new code immediately, increase strictness over time
- **Custom Types Module**: Common types defined in `mvp_site/custom_types.py` including CampaignData, StateUpdate, EntityData, and type aliases
- **Modern Syntax Support**: Python 3.10+ union syntax (`str | int`) and optional (`T | None`) patterns
- **Type Stubs**: Required stubs for Flask and Requests in requirements.txt

## Key Quotes
> "We use Python's type hints (PEP 484) with a gradual typing approach to improve code quality, catch bugs early, and enhance developer experience."

## Connections
- [[mypy]] — static type checker used for validation
- [[Pydantic]] — inherently typed by design
- [[Flask]] — typed route handlers with Union[Response, Tuple[Response, int]]
- [[Firebase]] — Firestore operations with TypedDict for data structures

## Type Patterns

### Flask Routes
```python
@app.route('/api/campaigns/<campaign_id>')
@check_token
def get_campaign(user_id: UserId, campaign_id: CampaignId) -> Union[Response, Tuple[Response, int]]
```

### Firebase Operations
```python
class UserData(TypedDict):
    name: str
    email: str
    created_at: datetime
```

### Optional Values
```python
# Modern syntax (Python 3.10+)
def find_entity(name: str) -> EntityData | None:
```
