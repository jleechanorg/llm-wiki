---
title: "Authentication Bypass"
type: concept
tags: [authentication, testing, security, flask]
sources: []
last_updated: 2026-04-08
---

## Description
Test patterns for bypassing authentication in development/testing environments. Uses special headers to simulate authenticated requests.

## In This Source
Two bypass mechanisms:
- `X-Test-Bypass-Auth: "true"` — bypass authentication
- `X-Test-User-ID: "test-user-123"` — set user identity

## Environment Setup
Tests set `os.environ["TESTING_AUTH_BYPASS"] = "true"` before importing app modules.

## Connections
- [[APIEndpointTesting]] — validates auth requirements
- [[MVPSiteMain]] — implements bypass logic
