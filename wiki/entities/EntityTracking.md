---
title: "EntityTracking"
type: entity
tags: [module, persistence, state]
sources: ["architecture-decision-tests-pydantic-validation"]
last_updated: 2026-04-08
---

## Summary
Entity state management module in WorldArchitect.AI that handles scene manifest persistence and entity state tracking. Imports from Pydantic module and exposes VALIDATION_TYPE constant.

## Module Path
`mvp_site.entity_tracking`


## Key Exports
- SceneManifest class
- VALIDATION_TYPE = "Pydantic"
- get_validation_info() function
- get_validation_type() function
## Used By
- [[ActionResolutionFieldConsolidationTests]] — for field validation
- [[ArcEventCompletionTrackingE2ETests]] — for state persistence
