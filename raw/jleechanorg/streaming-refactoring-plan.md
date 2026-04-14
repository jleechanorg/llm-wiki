# Streaming Refactoring Plan - Task to Bead Mapping

**PR:** #2541 - Design streaming response for LLM APIs
**Branch:** `claude/design-llm-streaming-C3snt`
**Status:** ✅ All tests passing, ready for implementation

## Overview

This document maps the implementation tasks to their corresponding beads for tracking the streaming architecture refactoring.

## Critical Bug Fixed ✅

**Task #1:** Fix missing json import in gemini_provider.py
**Status:** ✅ COMPLETED
**Commit:** `2413aa290`
**Impact:** Resolved 7 test failures in CI
**No bead needed:** This was a critical bug fix completed immediately

## Architecture Refactoring Beads

### Priority 1: Core Architecture

#### REV-h1g - Consolidate Streaming and Non-Streaming
**Task #5:** Consolidate continue_story and continue_story_streaming
**Priority:** 1 (CRITICAL)
**Status:** Open

**Objective:** Create single unified codepath for story generation

**Implementation:**
- Extract shared preparation logic into `_prepare_story_request()`
  - Provider/model selection
  - Agent selection
  - System instruction building
  - Budget allocation
  - Context truncation
  - LLMRequest building
- Create unified `_generate_story_response(streaming: bool)`
- Update `continue_story()` to use shared functions
- Update `continue_story_streaming()` to use shared functions

**Benefits:**
- Single source of truth (~150 lines of duplication eliminated)
- Bug fixes apply to both paths
- Easier to maintain and test
- Ensures feature parity

**Acceptance Criteria:**
- Both functions use same preparation logic
- Both use same generation logic (conditional on streaming flag)
- All existing tests pass
- No behavioral changes
- <150 lines of shared code extracted

---

#### REV-05w - Add JSON Mode + Tool Execution to Streaming
**Task #2:** Add JSON mode support to generate_content_stream_sync
**Task #3:** Implement two-phase streaming with tool execution
**Priority:** 1 (CRITICAL)
**Status:** Open
**Depends on:** REV-h1g

**Objective:** Streaming should produce same structured output as non-streaming

**Implementation:**
1. Modify `generate_content_stream_sync` to support `json_mode` parameter
   - When `json_mode=True`, set `response_mime_type="application/json"` in GenerateContentConfig
2. Implement two-phase streaming:
   - **Phase 1:** Stream JSON chunks (may contain tool_requests)
   - Parse completed Phase 1 JSON
   - Execute tool_requests (dice rolls, faction tools)
   - **Phase 2:** Stream final narrative with tool results injected
3. Emit tool_start/tool_result events in real-time
4. Validate response before persisting

**Benefits:**
- Streaming produces same structured output as non-streaming
- Tool execution happens during streaming (not after)
- Real-time tool events for frontend display
- Same validation as non-streaming path

**Acceptance Criteria:**
- `generate_content_stream_sync` accepts `json_mode` parameter
- Streamed chunks form valid JSON when concatenated
- Tool execution happens during streaming
- Tool events emitted for frontend display
- Response validated against schema before persistence
- Streaming produces same structured output as non-streaming

---

#### REV-m7u - Add Response Validation to Streaming
**Task #4:** Add response validation to streaming path
**Priority:** 1 (SECURITY)
**Status:** Open
**Depends on:** REV-05w

**Objective:** Streaming responses must be validated before Firestore persistence

**Current Issue:**
- Location: `streaming_orchestrator.py:286-314`
- Streaming persists LLM responses without validation
- No schema enforcement
- No dice roll validation
- No faction minigame state validation

**Implementation:**
1. Import validation from `narrative_response_schema.py`
2. Before persisting `full_narrative`:
   - Parse streamed text as JSON
   - Validate required fields (narrative, session_header, state_updates)
   - Validate dice_rolls format and authenticity
   - Validate faction_minigame state updates
   - Validate action_resolution if present
3. Handle validation errors gracefully:
   - Emit warning event
   - Persist partial data with error flag
   - Log validation failure

**Benefits:**
- Same security checks as non-streaming
- Prevents malformed responses from being saved
- Maintains data integrity

**Acceptance Criteria:**
- Streaming path validates responses before persistence
- Validation errors logged and emitted as warning events
- Invalid responses don't crash streaming flow
- Same validation as non-streaming path
- All security checks applied

---

### Priority 2: Quality & Polish

#### REV-69t - Add Integration Tests
**Task #6:** Add integration tests for streaming equivalence
**Priority:** 2 (QUALITY)
**Status:** Open
**Depends on:** REV-m7u

**Objective:** Verify streaming produces equivalent results to non-streaming

**Test Coverage:**
1. **Basic narrative generation**
   - Same input → same narrative content
2. **Tool execution parity**
   - Dice rolls produce same results (with fixed seed)
   - Faction tools execute in same order
   - Tool results identical
3. **Structured output parity**
   - Same JSON structure
   - Same state_updates
   - Same planning_block
   - Same dice_rolls array
4. **Error handling parity**
   - Same error messages
   - Same fallback behavior
   - Same validation errors

**Test Files:**
- `test_streaming_orchestrator.py` - Add equivalence tests
- `test_streaming_integration.py` - End-to-end streaming tests
- `test_llm_service_streaming.py` - Unit tests for continue_story_streaming

**Acceptance Criteria:**
- 10+ new tests for streaming equivalence
- Tests validate JSON structure matches
- Tests validate tool execution matches
- Tests run in CI with all other tests
- All tests pass

---

#### REV-nh9 - Update Frontend for Tool Events
**Task #7:** Update frontend streaming client for tool events
**Priority:** 2 (UX)
**Status:** Open
**Depends on:** REV-05w

**Objective:** Frontend displays tool execution in real-time during streaming

**Location:** `mvp_site/frontend_v1/js/streaming.js`

**Implementation:**
1. Add handler for `tool_start` events (show "Rolling dice..." spinner)
2. Add handler for `tool_result` events (display dice results inline)
3. Update UI to show tool execution in real-time
4. Add dice roll animation during streaming
5. Add faction tool result display during streaming

**UI Updates:**
- Show dice roll icon + result when tool_result event received
- Animate dice roll between tool_start and tool_result
- Display faction power calculations inline
- Show combat resolution results in real-time

**Acceptance Criteria:**
- Tool events properly handled and displayed
- Dice rolls animate during streaming
- No UI flashing or content jumps
- Graceful handling of missing tool events
- Works with existing StreamingClient

---

## Implementation Order

```
1. REV-h1g (Consolidate codebase)
       ↓
2. REV-05w (Add JSON mode + tools to streaming)
       ↓
3. REV-m7u (Add validation)
       ↓
4. REV-69t (Add tests)

   REV-nh9 (Frontend updates) ← starts after REV-05w
```

## Success Criteria

**After completing all beads:**
- ✅ Single codepath for streaming/non-streaming
- ✅ Same validation regardless of streaming flag
- ✅ Same tool execution during streaming
- ✅ Same structured output format
- ✅ DRY principle - one function to maintain
- ✅ Feature parity - identical user experience
- ✅ Comprehensive test coverage
- ✅ Real-time tool events in UI

## Current Status

- **Beads Created:** 5/5 ✅
- **Tasks Linked:** 7/7 ✅
- **Critical Bug Fixed:** 1/1 ✅
- **Tests Passing:** All ✅
- **Ready to Start:** REV-h1g (waiting for go-ahead)

---

**Last Updated:** 2026-02-08
**Commit:** 2413aa290 (json import fix)
**PR Status:** All tests passing, mergeable
