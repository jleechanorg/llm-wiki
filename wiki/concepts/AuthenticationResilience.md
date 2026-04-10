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
- [[AutoRetryMechanism]] — automatic retry with fresh tokens
- [[UserFriendlyErrorMessages]] — clear error communication
- [[OfflineCampaignCaching]] — offline data access

## Related Entities
- [[JWT]] — token system being made resilient
- [[ApiJs]] — implements retry logic
- [[AppJs]] — displays user-facing errors
