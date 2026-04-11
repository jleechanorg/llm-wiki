---
title: "V2 Dashboard Campaigns vs Welcome Page Test"
type: source
tags: [testing, v2, dashboard, welcome-page, red-green, tdd]
source_file: "raw/v2_dashboard_campaigns_not_welcome.py"
sources: []
last_updated: 2026-04-08
---

## Summary
Red/Green test verifying V2 React dashboard correctly shows campaigns list for authenticated users instead of incorrectly displaying the "Create Your First Campaign" welcome page. Test simulates the Dashboard React component logic to validate campaigns array properly controls UI state.

## Key Claims
- **Critical Display Bug**: V2 console logs 18 campaigns fetched successfully but UI still shows welcome page
- **Expected Behavior**: Dashboard should show campaigns list when campaigns.length > 0 AND user authenticated
- **Welcome Page Logic**: Should ONLY display when campaigns.length === 0
- **Root Cause**: campaigns array not being properly passed to Dashboard component
- **Test Validation**: Mock user Jeff L with 19 campaigns should trigger campaigns dashboard, not welcome page

## Test Assertions
- campaigns.length == 19 should trigger should_show_campaigns_dashboard = true
- should_show_welcome_page = (campaigns.length == 0) should be false when campaigns exist
- user_authenticated = true combined with campaigns.length > 0 should show dashboard

## Connections
- [[V2 Campaign Display Logic Red/Green Test]] — related display logic validation
- [[V1 vs V2 Campaign Creation Comparison Test]] — V1 vs V2 workflow comparison
- [[RedGreenTesting]] — TDD methodology used
- [[TestDrivenDevelopment]] — testing approach

## Contradictions
- None identified
