---
title: "Campaign Wizard Headless Screenshots Script"
type: source
tags: [python, selenium, browser-automation, campaign-wizard, screenshots]
source_file: "raw/test_campaign_wizard_screenshots_headless.py"
sources: []
last_updated: 2026-04-08
---

## Summary
Python Selenium script that automates capturing screenshots of all three steps of the Campaign Wizard in headless Chrome mode. The script navigates through the complete wizard workflow and saves screenshots of the Basics, AI Style, and Launch steps.

## Key Claims
- **Headless Automation**: Uses Chrome headless mode for background screenshot capture without UI
- **Complete Workflow**: Tests all three wizard steps (Basics → AI Style → Launch)
- **Dynamic Port Allocation**: Navigates to app via localhost:3001 with test_mode and test_user_id query params
- **Error Handling**: Uses try/finally to ensure browser cleanup regardless of outcome

## Key Screenshots Captured
1. Step 1: Basics - campaign name/description fields
2. Step 2: AI Style - LLM configuration options
3. Step 3: Launch - final campaign creation

## Connections
- [[Campaign Wizard]] — the feature being documented
- [[Selenium]] — the automation framework used
- [[Headless Mode]] — browser execution mode

## Contradictions
[]
