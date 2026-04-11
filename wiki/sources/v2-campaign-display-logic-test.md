---
title: "V2 Campaign Display Logic Red/Green Test"
type: source
tags: [testing, v2, campaign-display, playwright, red-green, tdd]
source_file: "raw/v2_campaign_display_logic_test.py"
sources: []
last_updated: 2026-04-08
---

## Summary
Red/Green test verifying V2 React frontend shows campaigns dashboard when campaigns exist, rather than incorrectly displaying the "Create Your First Campaign" landing page. Uses Playwright browser automation to validate the display logic.

## Key Claims
- **Display Logic Bug**: V2 API successfully fetches 503 campaigns but still shows landing page
- **Expected Behavior**: Users with existing campaigns should see campaigns dashboard
- **Landing Page Detection**: Checks for "Create Your First Campaign" and "Welcome, Adventurer" strings
- **Dashboard Detection**: Checks for campaign list UI and campaign data keywords (zara, elara, warrior, knight)
- **TDD Methodology**: Red phase confirms bug, Green phase validates fix

## Test Assertions
- V2 should NOT show landing page when campaigns exist
- V2 should show campaigns dashboard with campaign list
- V2 should display campaign data (characters like Zara, Elara)

## Connections
- [[V1VsV2CampaignCreation]] — related comparison testing
- [[Playwright]] — browser automation tool used
- [[RedGreenTesting]] — TDD methodology applied

## Contradictions
- None identified
