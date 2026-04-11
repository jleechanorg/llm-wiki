---
title: "TDD Tests for Flask API Service Enhancements"
type: source
tags: [python, testing, unittest, flask, api, pytest, test-client]
source_file: "raw/tdd-tests-flask-api-service-enhancements.md"
sources: []
last_updated: 2026-04-08
---

## Summary
Python unittest file validating REAL Flask application behavior using test_client. Tests authentication requirements, endpoint availability, CORS headers, and frontend serving fallback for the WorldArchitect.AI API.

## Key Claims
- **Flask Test Client**: Uses test_client() for real application testing without HTTP server
- **Auth Requirements**: /api/campaigns and /api/settings require authentication (401 without proper headers)
- **Test Bypass**: X-Test-Bypass-Auth header enables testing without real Firebase credentials
- **Time Endpoint**: /api/time returns server_time_utc structure
- **Campaign CRUD**: POST /api/campaigns creates campaigns with proper auth bypass
- **404 Handling**: Invalid endpoints return 404 (or 200 with SPA fallback)
- **CORS Support**: API routes properly handle Cross-Origin Resource Sharing
- **Static Files**: Frontend served from /frontend_v1/ path
- **Skipped Test**: MCPClient mocking test skipped due to closure capturing issues

## Key Quotes
> "Cannot reliably patch MCPClient due to closure capturing in create_thread_safe_mcp_getter and module import order"

## Connections
- [[API response format consistency]] — related API testing
- [[API backward compatibility tests for legacy forEach]] — related API testing
- [[Standalone Flask App Starter]] — Flask startup patterns

## Contradictions
- None identified
