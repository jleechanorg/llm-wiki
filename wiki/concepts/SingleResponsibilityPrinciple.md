---
title: "Single Responsibility Principle"
type: concept
tags: [solid, design-principle, architecture]
sources: ["services-layer-architecture"]
last_updated: 2026-04-08
---

## Summary
Each service focuses on one business domain. Part of SOLID design principles for maintainable software.

## Applies To
- [[ServicesLayerArchitecture]] — service layer design
- [[CampaignService]] — campaign business logic only
- [[UserService]] — user profile management only
- [[ContentService]] — content generation only

## Connections
- [[StatelessOperations]] — complementary service principle
- [[DependencyInjection]] — enables SRP through testability
