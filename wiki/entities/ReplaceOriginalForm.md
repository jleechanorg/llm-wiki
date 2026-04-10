---
title: "ReplaceOriginalForm"
type: entity
tags: [method, wizard, form]
sources: []
last_updated: 2026-04-08
---

ReplaceOriginalForm is a CampaignWizard method that accepts an optional skipCleanup parameter. When skipCleanup=true, it skips the cleanup logic that would normally trigger the problematic form reset sequence.

## Parameters
- skipCleanup (boolean, default=false): When true, skips cleanup logic

## Related Pages
- [[ForceCleanRecreation]] — calls this with skipCleanup=true
- [[CampaignWizard]] — containing component
