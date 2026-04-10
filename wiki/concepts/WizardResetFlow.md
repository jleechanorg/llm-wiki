---
title: "Wizard Reset Flow"
type: concept
tags: [wizard, reset, flow, state-management]
sources: []
last_updated: 2026-04-08
---

The wizard reset flow describes the sequence of events when a user completes a campaign and starts a new one. The problematic sequence involves: user completing first campaign → clicking Start Campaign → triggering enable() → route change to /new-campaign → form reset potentially interfering with wizard state.

The fix ensures forceCleanRecreation properly restores wizard content visibility and skips cleanup that would cause issues.

## Related Pages
- [[CampaignWizard]] — component managing the flow
- [[ForceCleanRecreation]] — fix method
- [[CampaignWizardResetCodeAnalysisTest]] — tests validating the flow
