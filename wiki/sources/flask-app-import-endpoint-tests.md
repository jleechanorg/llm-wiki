---
title: "Flask App Import and Endpoint Tests"
type: source
tags: [python, testing, flask, api, endpoints, mcp-client]
source_file: "raw/test_flask_app_import_endpoint.py"
sources: []
last_updated: 2026-04-08
---

## Summary
Test suite validating Flask app import, initialization, and API endpoint behavior. Tests verify /api/time, /api/campaigns, and /api/settings endpoints work correctly with authentication requirements and test bypass headers.

## Key Claims
- **Flask app imports successfully**: mvp_site.main module loads without errors with proper environment setup
- **App is Flask instance**: Imported app object is valid Flask application
- **Time endpoint works**: /api/time returns valid timestamp data with supported time keys
- **Campaigns endpoint requires auth**: /api/campaigns returns 401 without authentication
- **Settings endpoint requires auth**: /api/settings returns 401 without authentication
- **Test bypass headers work**: X-Test-Bypass-Auth and X-Test-User-ID headers enable authenticated access
- **MCP client mocking**: @patch decorator mocks MCPClient for campaign creation tests

## Key Test Cases
- test_flask_app_import: Verifies Flask app imports from mvp_site.main
- test_flask_app_is_flask_instance: Validates app is Flask instance
- test_time_endpoint_exists: GET /api/time returns 200 with time keys
- test_campaigns_endpoint_requires_auth: GET /api/campaigns returns 401
- test_settings_endpoint_requires_auth: GET /api/settings returns 401
- test_create_campaign_requires_auth: POST /api/campaigns returns 401 without auth

## Connections
- [[MVPSiteMain]] — main Flask application module
- [[MCPClient]] — mocked for campaign creation tests
- [[CacheBusting]] — DEFAULT_HASH_LENGTH imported from scripts.cache_busting

## Contradictions
- None identified
