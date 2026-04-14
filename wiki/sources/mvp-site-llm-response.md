---
title: "mvp_site llm_response"
type: source
tags: []
date: 2026-04-14
source_file: raw/mvp_site_all/llm_response.py
---

## Summary
Gemini Response wrapper for clean architecture between AI service and main application. Provides structured response handling with NarrativeResponse parsing, debug tag detection, and backward compatibility for legacy responses.

## Key Claims
- LLMResponse wraps narrative_text, structured_response (NarrativeResponse), and metadata
- create() factory method parses raw text to extract narrative and structured data
- create_from_structured_response() is the preferred creation method for JSON mode responses
- _detect_old_tags() identifies deprecated patterns like [DEBUG_START], [STATE_UPDATES_PROPOSED]
- Properties provide backward compatibility: state_updates, entities_mentioned, location_confirmed, debug_info, dice_rolls

## Connections
- [[NarrativeResponse]] — structured_response is a NarrativeResponse object
- [[LLMIntegration]] — response wrapper consumed by the main application
- [[DiceMechanics]] — dice_rolls property accesses structured response rolls