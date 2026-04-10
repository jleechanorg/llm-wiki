---
title: "Type Hints (PEP 484)"
type: concept
tags: [python, typing, pep-484]
sources: [python-typing-guide]
last_updated: 2026-04-08
---

Type hints (PEP 484) are Python's standard way to add type annotations to function signatures, variables, and class attributes. WorldArchitect.AI uses type hints throughout the codebase for improved code quality and bug detection.

## Example
```python
def get_campaign(user_id: UserId, campaign_id: CampaignId) -> Optional[CampaignData]:
```

## Related
- [[GradualTyping]] — adoption strategy
- [[mypy]] — static type checker
- [[TypeStubs]] — type stub files
