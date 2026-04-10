---
title: "Flask App Testing"
type: concept
tags: [flask, testing, web-framework]
sources: ["llm-response-capture-sariel-campaign"]
last_updated: 2026-04-08
---

## Description
Testing methodology using Flask's test_client() for HTTP endpoint testing without making actual network requests. Enables testing with X-Test-Bypass-Auth headers for authentication bypass and test user ID injection.

## Key Patterns
- **Test Client**: app.test_client() for HTTP requests
- **Authentication Bypass**: X-Test-Bypass-Auth and X-Test-User-ID headers
- **JSON Data**: json.dumps() for request body serialization

## Connections
- [[IntegrationTesting]] — Broader testing methodology
- [[SarielCampaign]] — Campaign being tested
