---
title: "Test: Streaming Full Journey with Network Proof"
type: source
tags: [worldarchitect-ai, testing, streaming, e2e, network-proof, sse, ocr]
sources: []
date: 2026-04-07
source_file: raw/test_streaming_full_journey_with_network_proof.md
last_updated: 2026-04-07
---

## Summary
Comprehensive browser test methodology validating complete streaming UX from campaign creation through 3 story actions using multiple evidence layers: screenshots, OCR/DOM extraction, and Chrome DevTools Network tab capture to prove SSE events transmitted.

## Key Claims

- **Gold Standard Validation**: Combines visual proof (screenshots), text proof (OCR/DOM), and network proof (SSE events) for streaming validation
- **Reproducible Fixed Prompts**: Uses deterministic prompts (`NETWORK_PROOF_1`, `NETWORK_PROOF_2`, `NETWORK_PROOF_3`) for consistent testing
- **Evidence Layers**: Four distinct proof types — screenshots, DOM capture, network tab SSE events, server logs
- **Preconditions**: Requires local server on port 8005, Chrome DevTools, authenticated browser (real or test mode)
- **Pass Criteria**: Campaign creation success, 3 story actions complete, SSE events visible in Network tab, no JavaScript errors

## Test Flow

### Server Setup
Requires environment variables: `WORLDAI_DEV_MODE=true`, `PORT=8005`, `CAPTURE_RAW_LLM=true`, `TESTING_AUTH_BYPASS=true`

### Evidence Collection
1. **Step 0**: Navigate to test URL, capture home state, enable streaming in localStorage
2. **Step 1**: Create campaign with title `NETWORK_PROOF_TEST_2026`
3. **Step 2-4**: Execute 3 story actions with fixed prompts, capture network evidence at each step
4. **Step 5**: Aggregate evidence — count story entries, verify SSE event sequences

## Expected SSE Events Sequence
```
data: {"type":"status","payload":{"message":"Generating response..."}}
data: {"type":"chunk","payload":{"text":"...","sequence":0}}
data: {"type":"chunk","payload":{"text":"...","sequence":1}}
...
data: {"type":"done","payload":{"full_narrative":"...","user_scene_number":N}}
```

## Connections
- [[Cache-Busting End-to-End Testing Methodology]] — related E2E testing methodology
- [[React V2 Current Status - Verified with Visual Evidence]] — visual testing approach connection

## Contradictions
- None identified