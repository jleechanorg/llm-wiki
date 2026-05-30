# CampaignWizard.disable() Stale selectedCampaignType

**Date**: 2026-05-30
**Type**: feedback / bug fix
**Bead**: rev-rux0d
**PR**: worldarchitect.ai [#7170](https://github.com/jleechanorg/worldarchitect.ai/pull/7170) merged

## Problem

`CampaignWizard.disable()` sets `isEnabled = false` but never clears `selectedCampaignType`.
`app.js` was reading `selectedCampaignType != null` without checking `isEnabled`, so a
user who selected Dragon Knight then disabled the wizard (switching to legacy Custom form)
still got `is_dragon_knight=true` from stale wizard state.

## Fix

```javascript
// app.js line 2936 — add isEnabled guard
if (
  window.campaignWizard &&
  window.campaignWizard.isEnabled &&          // ← added
  window.campaignWizard.selectedCampaignType != null
) {
```

## Rule

Always guard with `isEnabled` before reading any wizard state in non-wizard code paths.
Stale state from a disabled wizard is unreliable.

## Related concepts

- [[CampaignWizard]]
- [[WizardResetFlow]]
