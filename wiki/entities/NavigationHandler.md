---
title: "NavigationHandler"
type: entity
tags: [navigation, handler, routing]
sources: [root-cause-navigation-handler-missing-wizard-enable]
last_updated: 2026-04-08
---

## Description
Handler responsible for navigation in the campaign creation flow. Must call `wizard.enable()` after route changes to new-campaign.

## Connections
- [[CampaignWizard]] — requires enable() call after navigation
- [[RootCauseNavigationHandlerMissingWizardEnable]] — source documenting the bug
