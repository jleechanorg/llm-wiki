---
title: "Lady Cressida Valeriana"
type: entity
tags: [npc, location-based, entity-tracking]
sources: [sariel-campaign-integration-test-execution, sariel-llm-responses-entity-tracking-analysis]
last_updated: 2026-04-08
---

## Overview
Location-based NPC tracked in Lady Cressida's Chambers. Used as a test case for whether NPCs in their home locations are correctly inferred and tracked.

## Tracking Behavior
- **Location**: Lady Cressida's Chambers
- **Tracking Pattern**: Location-based NPC (should appear in her chambers)
- **Success Rate**: 0% in entity tracking tests — frequently missed in later interactions

## Known Issues
- **Disappears in Later Interactions** — While initially present, Lady Cressida is frequently missed in interactions 4, 6-7, 9-10
- **Location Inference Failure** — System fails to infer her presence based on location context

## Related
- [[SarielCampaignIntegrationTestExecution]] — tests location-based entity tracking
- [[Valerius]] — domain owner with different tracking pattern
- [[EntityTracking]] — the tracking mechanism being tested
