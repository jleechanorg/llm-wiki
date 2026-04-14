---
title: "test_api_response_format_consistency.py"
type: source
tags: [test, api, format, consistency, frontend, mcp]
date: 2025-MM-DD
source_file: raw/mvp_site_all/test_api_response_format_consistency.py
---

## Summary
Test file ensuring all API endpoints maintain consistent response formats between legacy (main branch), new MCP format, and frontend expectations. Validates backward compatibility and documents format requirements for each endpoint.

## Key Claims
- GET /api/campaigns must return array directly for backward compatibility
- GET /api/campaigns/<id> must return object with campaign, story, game_state fields
- POST /api/campaigns must return object with success and campaign_id fields
- POST /api/campaigns/<id>/interaction must return object with narrative or response field
- PATCH /api/campaigns/<id> must return object with success field
- GET /api/settings returns settings object or wrapped response
- POST /api/settings returns object with success field
- GET /api/campaigns/<id>/export returns file content, not JSON

## Key Connections
- Related to [[mvp-site-test-api-routes]] - both test API behavior
- Related to [[mvp-site-test-architectural-boundary-validation]] - tests field format consistency
- Connects to frontend compatibility layer
- Tests MCP protocol response translation

## Related Test Files
- [[mvp-site-test-api-routes]] - MCP gateway pattern tests
- [[mvp-site-test-architectural-boundary-validation]] - field format validation