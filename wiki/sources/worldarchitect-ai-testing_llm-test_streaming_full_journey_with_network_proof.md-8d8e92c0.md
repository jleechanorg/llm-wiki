---
title: "Streaming Full Journey with Network Proof Test"
type: source
tags: [worldarchitect-ai, testing, streaming, e2e, network, SSE, browser-automation, evidence]
date: 2026-04-07
source_file: raw/test-streaming-full-journey-network-proof.md
last_updated: 2026-04-07
---

## Summary
Comprehensive browser test specification for validating the complete WorldArchitect.AI streaming UX from campaign creation through 3 story actions with multiple evidence layers (screenshots, OCR/DOM extraction, Chrome DevTools Network tab capture, server logs). Gold standard for streaming validation using SSE event verification.

## Key Claims
- Tests complete user journey: campaign creation → character creation → story continuation with streaming enabled
- Multiple evidence layers: screenshots at each step, OCR/DOM text extraction to prove streaming content rendered, Network tab capture to prove SSE events transmitted
- Server runs on port 8005 with TESTING_AUTH_BYPASS enabled
- Test mode authentication via query params: `?test_mode=true&test_user_id=network-proof-user`
- Three story actions with fixed prompts for evidence tracing (NETWORK_PROOF_1, NETWORK_PROOF_2, NETWORK_PROOF_3)
- Verifies SSE event streaming: EventStream connection to `/api/campaigns/.../interaction/stream`
- Expected SSE events sequence: status → chunk (multiple) → done events

## Key Quotes
> "data: {\"type\":\"chunk\",\"payload\":{\"text\":\"You look around...\",\"sequence\":0}}" — chunk event format
> "data: {\"type\":\"done\",\"payload\":{\"full_narrative\":\"...\",\"user_scene_number\":2}}" — completion event format

## Connections
- [[WorldArchitect.AI Full User Journey Test Spec]] — earlier E2E test spec without network proof layer
- [[WorldArchitect.AI 20-Turn Test Improvement]] — iteration analysis showing timestamp and level progression fixes

## Contradictions
- None identified — this test builds on existing E2E testing approach with enhanced evidence capture