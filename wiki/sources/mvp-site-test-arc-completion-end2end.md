---
title: "test_arc_completion_end2end.py"
type: source
tags: [test, e2e, arc, completion, firestore]
date: 2025-MM-DD
source_file: raw/mvp_site_all/test_arc_completion_end2end.py
---

## Summary
End-to-end integration tests for arc/event completion tracking via /interaction. Uses FakeFirestoreClient and FakeLLMResponse to test the full stack including Firestore persistence and LLM context inclusion.

## Key Claims
- Arc milestones persist to Firestore under custom_campaign state
- Arc milestone status stored as "completed" with timestamp and phase
- Arc milestones included in LLM context for narrative generation
- Wedding arc example: status "completed" with phase "ceremony_complete"
- LLM generates appropriate narrative for post-arc state
- Planning block included in response with thinking and choices
- session_header tracks session context (e.g., "Session 5: Post-Wedding")
- Mocked LLM can be injected for deterministic testing

## Key Connections
- Tests [[mvp-site-game-state]] persistence
- Tests arc tracking in [[mvp-site-living-world]]
- Firestore integration for [[mvp-site-entity-tracking]]
- LLM context affects narrative generation

## Related Test Files
- [[mvp-site-test-api-service-enhancements]] - Flask tests
- [[mvp-site-test-api-routes]] - route tests