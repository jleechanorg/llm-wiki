---
title: "Debug Tags Detection"
type: concept
tags: [llm-response, debugging, parsing]
sources: [llm-response-object-tdd-tests]
last_updated: 2026-04-08
---

## Definition
Debug tags detection is the process of automatically identifying and extracting debug metadata from LLM responses. The LLMResponse class scans the debug_info block for specific fields: dm_notes, dice_rolls, resources, and state_rationale.

## How It Works
1. LLMResponse.create() receives raw response text (JSON string)
2. Parser extracts debug_info block from structured response
3. Each debug tag field is checked for non-empty content
4. debug_tags_present dictionary maps each tag to boolean (has content?)
5. has_debug_content returns True if ANY debug tag has content

## Use Cases
- Separating debug information from narrative for frontend display
- Allowing players to optionally view DM notes and dice rolls
- Debugging LLM response quality by inspecting generated metadata
- Preserving resource tracking (HD, Spells) in structured form

## Related Concepts
- [[LLMResponse]] — class that implements debug tags detection
- [[State Updates Extraction]] — complementary extraction of game state changes
- [[Entities Mentioned Detection]] — extraction of named entities from narrative
