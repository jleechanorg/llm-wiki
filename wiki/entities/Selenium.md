---
title: "Selenium"
type: entity
tags: [testing, browser-automation, tool]
sources: []
last_updated: 2026-04-08
---

## Summary
Selenium is a browser automation framework that enables automated testing of web applications across different browsers. The project provides WebDriver APIs for controlling browser instances programmatically.

## Key Details
- **Language**: Python (selenium package)
- **Purpose**: Browser automation for testing web applications
- **Key Classes**: WebDriver, WebDriverWait, expected_conditions (EC), By
- **Website**: https://www.selenium.dev/

## Usage in This Project
Used for end-to-end browser testing of the Campaign Wizard component, including the reset issue reproduction test that validates the wizard returns to a clean state after user navigation.

## Connections
- [[ChromeWebDriver]] — Chrome-specific WebDriver implementation
- [[BrowserAutomation]] — broader testing concept
- [[CampaignWizard]] — component being tested
