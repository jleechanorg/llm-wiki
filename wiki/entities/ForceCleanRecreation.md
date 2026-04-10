---
title: "ForceCleanRecreation"
type: entity
tags: [method, wizard, cleanup]
sources: []
last_updated: 2026-04-08
---

ForceCleanRecreation is a method in CampaignWizard that ensures clean wizard state restoration by calling replaceOriginalForm with skipCleanup=true, bypassing normal cleanup logic to prevent the problematic form reset sequence.

## Related Pages
- [[CampaignWizard]] — containing component
- [[ReplaceOriginalForm]] — method called with skipCleanup parameter
- [[CampaignWizardResetCodeAnalysisTest]] — tests validating this method
