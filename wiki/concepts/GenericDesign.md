---
title: "Generic Design"
type: concept
tags: [design-pattern, software-engineering]
sources: [generic-entity-tracking-tests]
last_updated: 2026-04-08
---

Design principle requiring systems to work with any input, not just specific known cases. In entity tracking context, means removing hardcoded references to specific campaigns (e.g., Sariel) and using dynamic detection instead.


## Application to Entity Tracking
- No hardcoded entity names in instruction generation
- Location-based rules return empty to avoid false assumptions
- Player character detection uses runtime data, not static lists

## Related Concepts
- [[GenericDesign]] vs [[HardcodedCampaignData]]
- [[SemanticUnderstanding]] approach over pattern matching
