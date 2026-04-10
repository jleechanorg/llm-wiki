---
title: "API Endpoint Testing"
type: concept
tags: [api, rest, testing, flask]
sources: []
last_updated: 2026-04-08
---

## Description
Testing REST API endpoints in Flask applications. Validates HTTP status codes, response format, and authentication requirements.

## In This Source
Tests three API endpoints:
- `/api/time` — GET returns timestamp data
- `/api/campaigns` — GET/POST with auth requirements
- `/api/settings` — GET with auth requirements

## Test Patterns
- Status code assertions: assert response.status_code == 200/401/500
- JSON validation: assert response.is_json, response.get_json()
- Auth headers: X-Test-Bypass-Auth, X-Test-User-ID

## Connections
- [[FlaskTesting]] — uses test client
- [[AuthenticationBypass]] — test authentication patterns
