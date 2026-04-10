---
title: "Business Logic Extraction"
type: concept
tags: [architecture, refactoring, design]
sources: [unified-api-implementation]
last_updated: 2026-04-08
---

## Definition
The process of removing duplicated business logic from multiple interface layers and consolidating it into a shared module that all interfaces call.

## Application
Unified API extracts game state preparation, debug command handling, campaign prompt building, and legacy state migration into shared functions.

## Key Extracted Functions
- create_campaign_unified()
- process_action_unified()
- get_campaign_state_unified()
- update_campaign_unified()
- export_campaign_unified()
- get_campaigns_list_unified()

## Related Concepts
- [[UnifiedAPIPattern]]
- [[DRYPrinciple]]
- [[SingleSourceOfTruth]]
