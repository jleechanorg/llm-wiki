---
title: "Campaign Wizard Reset Issue Reproduction Test"
type: source
tags: [python, testing, selenium, browser-automation, campaign-wizard, bug-reproduction]
source_file: "raw/test_campaign_wizard_reset_issue_reproduction.py"
sources: []
last_updated: 2026-04-08
---

## Summary
Selenium-based browser automation test that reproduces the exact user workflow leading to a persistent spinner issue in the Campaign Wizard. The test validates that after creating a campaign, navigating back to the dashboard, and starting a new campaign, the wizard appears clean without any stuck spinner states.

## Key Claims
- **Workflow Reproduction**: Test simulates complete user journey: create first campaign → navigate to dashboard → click "Start Campaign" again → verify clean wizard state
- **Performance Gated**: Test only runs when ENABLE_BROWSER_TESTS=1 environment variable is set, as it is an expensive 30+ second test
- **Dynamic Port Allocation**: Uses socket for dynamic port assignment to avoid port conflicts during test server startup
- **Headless Chrome**: Runs Chrome in headless mode for automated CI/CD integration

## Test Implementation Details
- Uses `http.server.SimpleHTTPRequestHandler` to serve the application
- Chrome WebDriver configuration with `--headless`, `--no-sandbox`, `--disable-dev-shm-usage` flags
- WebDriverWait for explicit waits on element presence
- Custom TCPServer setup with daemon thread for test server

## Connections
- [[CampaignWizard]] — the component being tested for reset behavior
- [[Selenium]] — browser automation framework used
- [[ChromeWebDriver]] — Chrome driver for headless browser control

## Contradictions
- None identified
