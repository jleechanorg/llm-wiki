---
title: "test_api_routes.py"
type: source
tags: [test, api, routes, mcp, gateway]
date: 2025-MM-DD
source_file: raw/mvp_site_all/test_api_routes.py
---

## Summary
Tests API endpoints through MCP API gateway pattern. Validates authentication requirements, story pagination service, endpoint response formats, and MCP protocol field handling. Includes TestAPIRoutes and TestStoryPagination test classes.

## Key Claims
- Campaigns endpoint returns 200/401/404 depending on auth mode
- Settings endpoint returns 200 or 401 based on auth state
- Campaign interaction endpoint handles request gracefully
- MCP endpoint requires authentication in production mode
- MCP endpoint allows unauthenticated access in non-production
- Test bypass headers (X-Test-Bypass-Auth, X-Test-User-ID) enable test auth
- Pagination must not drop entries that share the cursor timestamp
- has_older reflects presence of extra entry beyond limit
- sequence_id and user_scene_number remain absolute across pages
- Invalid timestamp raises ValueError for validation

## Key Connections
- Related to [[mvp-site-test-api-response-format-consistency]] - tests API response formats
- Related to [[mvp-site-test-architectural-boundary-validation]] - tests field translation
- Tests MCP gateway behavior under different auth modes
- Story pagination affects [[mvp-site-combat]] context loading

## Related Test Files
- [[mvp-site-test-api-response-format-consistency]] - response format consistency
- [[mvp-site-test-architectural-boundary-validation]] - boundary validation