---
title: "Arc/Event Completion Tracking End-to-End Tests"
type: source
tags: [python, testing, unittest, e2e, firestore, integration]
source_file: "raw/arc-event-completion-tracking-e2e-tests.md"
sources: []
last_updated: 2026-04-08
---

## Summary
End-to-end integration tests validating arc/event completion tracking through the /interaction endpoint. Tests verify that arc milestones persist to Firestore and are included in LLM context for narrative generation.

## Key Claims
- **Arc Milestones Persistence**: Game state arc_milestones data (status, completed_at, phase) persists to Firestore under custom_campaign_state
- **LLM Context Inclusion**: Arc milestones are included in context passed to LLM for generating narrative responses
- **Test Setup**: Uses FakeFirestoreClient mock and FakeLLMResponse for testing without external dependencies
- **Interaction Endpoint**: POST /api/campaigns/{id}/interaction accepts mode parameter for character/story modes

## Key Test Cases
1. test_arc_milestones_persist_to_firestore: Validates Firestore storage of arc_milestones with wedding_tour example
2. test_arc_milestones_included_in_llm_context: Validates arc milestone data reaches LLM for narrative generation

## Connections
- [[Firestore]] — database for persisting game state including arc_milestones
- [[LLM Context]] — prompt context that includes current arc status for narrative decisions
- [[Interaction Endpoint]] — /api/campaigns/{id}/interaction for user input processing

## Contradictions
- None identified
