---
title: "Authentication Resilience"
type: concept
tags: [authentication, resilience, error-handling]
sources: ["auth-resilience-clock-skew-tests"]
last_updated: 2026-04-08
---

## Description
System design pattern for handling authentication failures gracefully. In WorldArchitect.AI, this includes automatic retry for clock skew errors and user-friendly error messaging.

## Key Components
- [AutoRetryMechanism](AutoRetryMechanism.md) — automatic retry with fresh tokens
- [UserFriendlyErrorMessages](UserFriendlyErrorMessages.md) — clear error communication
- [OfflineCampaignCaching](OfflineCampaignCaching.md) — offline data access

## Related Entities
- [JWT](../entities/JWT.md) — token system being made resilient
- [ApiJs](../entities/ApiJs.md) — implements retry logic
- [AppJs](../entities/AppJs.md) — displays user-facing errors
