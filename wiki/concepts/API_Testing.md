---
title: "API Testing"
type: concept
tags: [testing, integration-testing, api]
sources: [comprehensive-authenticated-api-test-suite]
last_updated: 2026-04-08
---

API testing involves validating API endpoints for correct behavior, authentication requirements, error handling, and response formats. This test suite uses Python's requests library to test campaign endpoints with and without authentication credentials.

## Key Methods
- GET /api/time — server health check
- GET /api/campaigns — list campaigns
- POST /api/campaigns — create new campaign

## Connections
- [[Authentication]] — tests whether endpoints require auth
- [[Server Connectivity]] — basic endpoint availability
