---
title: "Streaming Full Journey with Network Proof"
type: source
tags: [testing, streaming, worldarchitect-ai, e2e, sse, network, validation]
date: 2026-04-07
source_file: raw/worldarchitect.ai-testing_streaming_full_journey_network_proof.md
last_updated: 2026-04-07
---

## Summary
Comprehensive browser test validating complete streaming UX from campaign creation through 3 story actions with multiple evidence layers: screenshots (visual proof), OCR/DOM extraction (text proof), and Chrome DevTools Network tab capture (SSE event proof). This is the gold standard streaming validation test.

## Key Claims
- **Four-layer evidence validation**: Screenshots, OCR/DOM text extraction, Network tab SSE capture, and server logs for backend correlation
- **Campaign wizard flow**: Full end-to-end from home page through character creation
- **Three fixed story actions**: Predefined prompts (tavern observation, innkeeper interaction, quest acceptance) for reproducibility
- **SSE event verification**: Validates EventStream connections to `/api/campaigns/.../interaction/stream` with proper chunk/done sequence
- **Pass criteria**: Campaign creation redirects successfully, streaming content renders in DOM, Network tab shows SSE chunks, story entries count >= 4

## Key Quotes
> "data: {\"type\":\"status\",\"payload\":{\"message\":\"Generating response...\"}}
> data: {\"type\":\"chunk\",\"payload\":{\"text\":\"You look around...\",\"sequence\":0}}
> ...
> data: {\"type\":\"done\",\"payload\":{\"full_narrative\":\"...\",\"user_scene_number\":2}}" — Expected SSE events sequence

## Test Flow
1. **Setup**: Navigate to test URL, enable streaming via localStorage, open DevTools Network tab
2. **Campaign Creation**: Fill wizard form (title: NETWORK_PROOF_TEST_2026, setting: Tavern adventure), submit, complete character creation
3. **Action 1** (NETWORK_PROOF_1): "I look around the tavern carefully" — capture network SSE, verify chunk sequence
4. **Action 2** (NETWORK_PROOF_2): "I approach the innkeeper and ask about rumors" — verify streaming consistency
5. **Action 3** (NETWORK_PROOF_3): "I accept the quest and prepare my gear" — final validation
6. **Aggregation**: Count story entries, document network events, verify console for errors

## Evidence Directory Structure
```
/tmp/worldarchitect.ai/claude/<branch>/streaming_full_network_proof/iteration_001/
├── run.json, metadata.json, evidence.md
├── llm_request_responses.jsonl, request_responses.jsonl
└── artifacts/ (server.log, screenshots, OCR txt, network_events_summary.txt)
```

## Connections
- [[WorldArchitectAI]] — platform being tested
- [[StreamingValidation]] — concept: SSE-based streaming UX testing methodology

## Contradictions
- None noted
