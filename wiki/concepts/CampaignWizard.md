---
title: "Campaign Wizard"
type: concept
tags: [ui, wizard, campaign-creation, form, frontend]
sources: []
last_updated: 2026-04-08
---

## Definition

Campaign wizard is a multi-step form UI component for creating new game campaigns with various configuration options.

## Key Features


- **Checkbox Options**: Narrative flair and mechanical precision toggles
- **Begin Adventure Button**: Final action to start the campaign
- **Form Group Layout**: Organized input groupings

## Connections

- Part of [[CampaignCreation]] workflow
- Uses [[FormInputHandling]] concepts
- Tested by [[FunctionalValidationTesting]]

## State Management Gotcha (2026-05-30)

`disable()` sets `isEnabled = false` but does **NOT** clear `selectedCampaignType`.
Any code reading wizard state must check `isEnabled` first:

```javascript
if (window.campaignWizard && window.campaignWizard.isEnabled &&
    window.campaignWizard.selectedCampaignType != null) { ... }
```

Without this guard, stale `selectedCampaignType` persists after `disable()` and can
override legacy form radio buttons. See source: wizard-isenabled-guard-2026-05-30
