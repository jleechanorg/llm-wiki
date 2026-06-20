---
title: "Wizard Pattern"
type: concept
tags: [ui-pattern, wizard, state-management]
sources: [root-cause-navigation-handler-missing-wizard-enable]
last_updated: 2026-04-08
---

## Description
UI pattern for multi-step processes (like campaign creation) where a wizard component manages state and requires explicit enable/disable calls to control interactivity.

## Key Methods
- `wizard.enable()` — makes the wizard interactive
- `wizard.disable()` — prevents user interaction
- Navigation handlers must call enable() after route changes

## Connections
- [CampaignWizard](CampaignWizard.md) — implementation of wizard pattern
- [NavigationHandler](NavigationHandler.md) — must coordinate with wizard state
