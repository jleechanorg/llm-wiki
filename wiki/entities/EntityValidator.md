---
title: "EntityValidator"
type: entity
tags: [module, validation, mvp-site]
sources: [summary-test-unknown-entity-fix]
last_updated: 2026-04-08
---

EntityValidator is a class in `mvp_site` that validates expected entities are present in generated narratives. Prevents AI hallucinations by checking that key entities mentioned in the prompt actually appear in the generated story.


## Key Behavior
- Validates presence of expected entities in narrative text
- Filters out 'Unknown' placeholder to prevent false validation failures
- Returns missing entities list and retry flag

## Related
- [[EntityValidation]] — the concept being validated
