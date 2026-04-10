---
title: "Entity Tracking Budget"
type: concept
tags: [context-budgeting, token-management, entity-tracking]
sources: [entity-tracking-budget-fix-end2end-test]
last_updated: 2026-04-08
---

## Definition

A reserved token budget for entity tracking overhead (entity_preload_text, entity_specific_instructions, entity_tracking_instruction, timeline_log) that is explicitly included in scaffold calculation BEFORE truncation, preventing ContextTooLargeError.

## Implementation

The ENTITY_TRACKING_TOKEN_RESERVE constant (~10,500 tokens) is added to scaffold budget before calculating the truncation threshold, ensuring entity tracking overhead is accounted for in the token limit.

## Problem Solved

Original bug: entity tracking was added AFTER truncation, causing final prompt to exceed context window. For qwen-3-235b-a22b-instruct-2507, this resulted in 97,923 tokens used when max was 94,372 — a ~3,500 token overage.

## Related Concepts
- [[ScaffoldCalculation]] — where the budget is applied
- [[ContextBudgeting]] — broader token allocation system
- [[TokenEstimation]] — used to calculate overhead
