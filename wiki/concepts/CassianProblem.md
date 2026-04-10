---
title: "Cassian Problem"
type: concept
tags: [entity-tracking, edge-case, npc, sariel]
sources: [sariel-campaign-integration-test-expected-output, sariel-llm-responses-entity-tracking-analysis, sariel-campaign-integration-test-execution]
last_updated: 2026-04-08
---

## Summary
An edge case in entity tracking where the player explicitly references an NPC (e.g., "tell Cassian I was scared and helpless") but that NPC is not present in the current scene. The LLM must either infer the NPC's presence or handle the reference appropriately.

## Challenge
- **Player Action**: References absent NPC with emotional content
- **LLM Behavior**: Generate narrative without including the referenced NPC
- **Success Criteria**: NPC appears in narrative or is appropriately referenced despite not being in scene

## Test Results
- **Integration Test**: Successfully handled (marked as "CASSIAN PROBLEM: HANDLED")
- **Baseline Analysis**: 0% success in earlier tests (from [[SarielLLMResponsesEntityTrackingAnalysis]])

## Related Pages
- [[SarielCampaignIntegrationTestExpectedOutput]] — test output showing problem handled
- [[SarielLLMResponsesEntityTrackingAnalysis]] — documents 0% baseline success
- [[SarielCampaignIntegrationTestExecution]] — execution with edge case testing
