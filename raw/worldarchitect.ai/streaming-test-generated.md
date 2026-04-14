# Streaming Flows E2E Test - Generated

**Test File:** `testing_mcp/test_streaming_flows.py`
**Generated:** 2026-02-08
**Purpose:** Validate streaming functionality for PR #2541

## Test Overview

Comprehensive E2E test for streaming across all story flows:

### Test Scenarios

1. **Create Story with Streaming**
   - Create campaign with streaming enabled
   - Verify SSE events emitted during story generation
   - Validate structured output (narrative + state_updates)

2. **Continue Story with Streaming**
   - Continue existing story with streaming
   - Verify incremental chunk delivery
   - Validate narrative continuity

3. **Streaming vs Non-Streaming Equivalence**
   - Compare output structure between modes
   - Verify same JSON schema regardless of streaming flag
   - Check required fields: narrative, state_updates, planning_block

4. **Tool Execution During Streaming**
   - Force dice roll scenario (Stealth check)
   - Verify dice_rolls array populated during streaming
   - Validate dice roll structure (notation, rolls, total)

5. **Response Validation Before Persistence**
   - Verify all actions persisted correctly
   - Check story history completeness
   - Validate each entry has required fields (actor, text)

## Test Architecture

**Base Class:** `MCPTestBase` from `testing_mcp/lib/base_test.py`

**Key Features:**
- Automatic server management (start/stop)
- Built-in evidence collection
- User/model configuration
- Campaign tracking for evidence

**Evidence Standards:** Follows `.claude/skills/evidence-standards.md`

## Test Configuration

```python
TEST_NAME = "streaming_flows"
MODEL = "gemini-3-flash-preview"  # Pinned to avoid fallback noise
WORK_NAME = "streaming_flow_test"
```

## Evidence Collection

**Evidence Directory:** `/tmp/worldarchitect.ai/claude/design-llm-streaming-C3snt/streaming_flow_test/`

**Generated Files:**
- `README.md` - Test overview and methodology
- `methodology.md` - Test execution approach
- `evidence.md` - Raw test results
- `notes.md` - Analysis and observations
- `run.json` - Structured test results with scenarios
- `metadata.json` - Git provenance and environment
- `request_responses.jsonl` - MCP tool call history
- `*.sha256` - Checksums for all evidence files

## Running the Test

```bash
# Run with evidence collection (REAL MODE)
TESTING_AUTH_BYPASS=true python3 testing_mcp/test_streaming_flows.py --work-name streaming_flow_test

# Run against existing server
python3 testing_mcp/test_streaming_flows.py --server http://localhost:8001

# Custom evidence directory
python3 testing_mcp/test_streaming_flows.py --evidence-dir /path/to/evidence
```

## Success Criteria

**Test Passes If:**
- ✅ All 5 scenarios pass
- ✅ Streaming produces structured JSON output
- ✅ Tool execution occurs during streaming (dice rolls)
- ✅ Response validation before persistence
- ✅ Story history complete and valid

**Test Fails If:**
- ❌ Missing narrative or structured output
- ❌ No tool execution evidence (dice rolls)
- ❌ Incomplete story history
- ❌ Invalid entry structure

## Integration with PR #2541

This test validates the architectural changes for streaming:

**What It Tests:**
- ✅ Single unified codepath handles streaming/non-streaming
- ✅ JSON mode works with streaming
- ✅ Tool execution during streaming (not after)
- ✅ Response validation before Firestore persistence

**Related Beads:**
- REV-h1g: Consolidate streaming/non-streaming codepaths
- REV-05w: Add JSON mode + tool execution to streaming
- REV-m7u: Add response validation to streaming persistence
- REV-69t: Add integration tests for streaming equivalence

## Known Limitations

**Current Implementation:**
- Streaming test uses standard `process_action` endpoint
- SSE endpoint (`/interaction/stream`) tested separately
- Real LLM calls may timeout in CI (use shorter timeouts for CI)

**Future Enhancements:**
- Add direct SSE endpoint testing
- Add streaming abort/cancel testing
- Add concurrent streaming session testing
- Add streaming error recovery testing

## Test Maintenance

**When to Update:**
1. Streaming endpoint changes (new events, formats)
2. Response schema changes (new required fields)
3. Tool execution changes (new tools, formats)
4. Evidence standards updates

**Dependencies:**
- `testing_mcp/lib/base_test.py` - Test infrastructure
- `testing_mcp/lib/campaign_utils.py` - Campaign operations
- `testing_mcp/lib/evidence_utils.py` - Evidence generation
- `.claude/skills/evidence-standards.md` - Evidence requirements
