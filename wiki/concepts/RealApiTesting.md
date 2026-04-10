---
title: "Real API Testing"
type: concept
tags: [testing, apis, integration]
sources: []
last_updated: 2026-04-08
---

Real API testing involves testing application behavior using actual external services (Firebase, Gemini, etc.) instead of mock implementations. This approach validates the complete integration but incurs actual API costs and requires network connectivity.

## Why Real APIs
- Validates complete integration with production-like behavior
- Catches issues that mocks might miss (timeout handling, API changes, etc.)
- More accurate cost estimation for production usage

## Trade-offs
- Costs money per test run (Gemini API calls)
- Requires network connectivity
- Slower than mock-based tests
- Can fail due to external service issues unrelated to code

## Used In
- [[CompleteE2ECampaignCreationRealApisTest]] — real Firebase + Gemini
