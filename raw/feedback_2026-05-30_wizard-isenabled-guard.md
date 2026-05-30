---
name: wizard-isenabled-guard
description: CampaignWizard.disable() never clears selectedCampaignType — always check isEnabled before reading wizard state in app.js
metadata: 
  node_type: memory
  type: feedback
  bead: rev-rux0d
  originSessionId: 275ec345-f729-4719-a137-4169f79d03ba
---

## Stale wizard selectedCampaignType after disable()

`CampaignWizard.disable()` (`campaign-wizard.js:552`) sets `this.isEnabled = false`
and calls `this.restoreOriginalForm()`, but does NOT clear `this.selectedCampaignType`.

The `enable()` method (line 507) does clear it (`this.selectedCampaignType = null`),
but `disable()` was missed.

**Bug:** `app.js` was checking `window.campaignWizard.selectedCampaignType != null`
to decide whether to override the legacy radio. After `disable()`, `selectedCampaignType`
remained `'dragon-knight'` forever, causing the stale wizard type to override the
legacy Custom radio → `is_dragon_knight=true` sent to backend → default world injected
into custom campaign.

**Fix (app.js line 2936):**
```javascript
// Before (buggy):
if (window.campaignWizard && window.campaignWizard.selectedCampaignType != null) {

// After (correct):
if (window.campaignWizard && window.campaignWizard.isEnabled &&
    window.campaignWizard.selectedCampaignType != null) {
```

**Rule:** When reading any wizard state property to influence non-wizard code paths,
always guard with `isEnabled` first. Stale state from a disabled wizard is invalid.

**References:**
- PR [#7170](https://github.com/jleechanorg/worldarchitect.ai/pull/7170) — merged 2026-05-30
- `mvp_site/frontend_v1/app.js:2936`
- `mvp_site/frontend_v1/js/campaign-wizard.js:552` (disable method)
- Regression test: `test_stale_wizard_type_cannot_override_custom_radio`
