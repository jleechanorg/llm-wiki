---
title: "Server Connectivity"
type: concept
tags: [infrastructure, testing, networking]
sources: [comprehensive-authenticated-api-test-suite]
last_updated: 2026-04-08
---

Server connectivity testing validates that backend services are reachable and responding. The test suite checks both the backend (port 8081) and frontend (port 3002) endpoints.

## Test Targets
- Backend: http://localhost:8081/api/time
- Frontend: http://localhost:3002

## Connections
- [[API Testing]] — tests endpoint availability
- [[Frontend Accessibility Testing]] — tests frontend availability
