# REV: Streaming Firestore Stores JSON-Parse-Failure Marker Instead of Real Narrative

## Symptom
Firestore campaign entry stores `"Invalid JSON response received. Please try again."` for AI
responses when using OpenRouter with non-schema-support models (e.g. llama-3.1-70b-instruct).
SSE done payload correctly carries the real narrative; Firestore does not.

## Root Cause
Two-step parse failure in `streaming_orchestrator.py`:

1. `continue_story_streaming` calls `parse_structured_response(raw_openrouter_text)` → fails
   JSON parsing → returns fallback marker as `narrative_text`. Streaming fallback logic
   (lines 7145-7159 of `llm_service.py`) detects this and replaces `narrative_text` with
   the raw streaming text (correct). Done event payload: `full_narrative = narrative_text`
   (good text), `raw_response_text = full_narrative` (also the plain-text OpenRouter output).

2. `streaming_orchestrator.py` (lines 445-466) re-calls `parse_structured_response(raw_response_text)`.
   This re-parse also fails JSON → again returns the fallback marker. Since the marker is
   **non-empty**, the `not parsed_narrative or not parsed_narrative.strip()` guard does NOT
   trigger. So `validated_narrative = "Invalid JSON response received. Please try again."` →
   stored to Firestore.

## Fix
In `streaming_orchestrator.py`, after `validated_narrative = parsed_narrative`, check if it
equals `_JSON_PARSE_FALLBACK_MARKER`. If so, fall back to `full_narrative` (the done event's
pre-processed narrative which is already the correct raw streaming text).

## Affected Files
- `mvp_site/streaming_orchestrator.py` (validation block ~lines 438-480)

## Evidence
- Branch: fix/openrouter-streaming-20260303_213125
- Test: `testing_mcp/streaming/test_openrouter_streaming_real.py` iteration_010
- Firestore entry: `[gemini] character | Invalid JSON response received. Please try again.`
- Done payload: correct narrative present (test passed narrative check)
