---
title: "DOM Manipulation Testing"
type: concept
tags: [testing, dom, javascript, frontend]
sources: [campaign-wizard-reset-red-green-test-html]
last_updated: 2026-04-08
---

## Description
Testing technique that validates Document Object Model changes in response to user interactions. The wizard reset test validates DOM state by checking:
- Container existence after enable()
- Content presence after reset
- Spinner removal in reset state
- Step navigation visibility

## Application
Used in [[CampaignWizard]] testing to verify form elements (campaign-title, campaign-prompt) are properly created, displayed, and cleaned up during state transitions.
