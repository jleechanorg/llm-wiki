# Fix MCP test evidence infrastructure gaps

**Type:** task
**Priority:** 3
**Status:** open
**Labels:** testing, evidence, infrastructure

## Description

Evidence-standards validation identified 5 gaps in testing_mcp evidence collection that prevent proper LLM behavior verification and traceability.

These issues affect all MCP tests using MCPTestBase, not just spicy mode tests.

**Evidence Bundle Analyzed:** `/tmp/worldarchitect.ai/claude/add-spicy-mode-detection-UPqKW/spicy_mode_comprehensive_real/iteration_004`

## Design

### Infrastructure Changes Needed

#### 1. Raw LLM Capture (CRITICAL)
**File:** `testing_mcp/lib/evidence_utils.py`
**Issue:** raw_unknown_model_*.txt files show "No raw response captured"
**Fix:**
- Capture raw_request_payload and raw_response_text from process_action results
- Write to per-scenario files with actual model name (not "unknown_model")
- Add to request_responses.jsonl

#### 2. Campaign ID Traceability
**File:** `testing_mcp/lib/base_test.py`
**Issue:** run.json missing campaign_id fields, evidence.md shows "N/A"
**Fix:**
- Ensure each scenario result dict includes campaign_id
- Pass campaign_id through from test to evidence bundle
- Update evidence.md template to show campaign IDs

#### 3. Evidence Mode Disclosure
**File:** `testing_mcp/lib/evidence_utils.py` (create_evidence_bundle)
**Issue:** metadata.json missing required evidence_mode field
**Fix:**
- Add evidence_mode field to metadata.json
- Set to "lightweight_prompt_tracking" or "full_llm_capture" based on actual capture
- Add notes explaining what was captured

#### 4. Methodology Accuracy
**File:** `testing_mcp/lib/evidence_utils.py` (methodology template)
**Issue:** methodology.md claims "Raw LLM response text captured" but it's not
**Fix:**
- Update methodology.md template to reflect actual capture level
- Remove false claims about raw LLM capture if not implemented
- Align with evidence_mode metadata

#### 5. Model Provenance in Filenames
**File:** `testing_mcp/lib/evidence_utils.py`
**Issue:** Files named raw_unknown_model_*.txt instead of actual model
**Fix:**
- Extract llm_provider/llm_model from debug_info
- Generate filenames like raw_gemini-3-flash_scenario_name.txt
- Fall back to "unknown" only if model truly unknown

## Acceptance Criteria

### Evidence Bundle Validation
- [ ] raw_request_payload and raw_response_text present in request_responses.jsonl
- [ ] Per-scenario raw response files contain actual LLM output (not "No raw response captured")
- [ ] Raw response filenames include actual model name (e.g., raw_gemini-3-flash_*.txt)
- [ ] run.json includes campaign_id field for each scenario
- [ ] evidence.md shows actual campaign IDs (not "N/A")
- [ ] metadata.json includes evidence_mode field with accurate value
- [ ] methodology.md accurately describes what was captured

### Test Coverage
- [ ] Existing tests still pass after infrastructure changes
- [ ] Evidence-standards validation passes for new test runs
- [ ] No regression in test performance (reasonable timeout)

### Documentation
- [ ] Update testing_mcp/lib/README.md with evidence capture requirements
- [ ] Document evidence_mode options and when to use each

## Notes

This task emerged from evidence-standards validation of PR #3185 (spicy mode detection).

The issues are infrastructure-level, not test-logic failures. PR #3185 can proceed while these improvements are made in a follow-up.

## Related

- PR #3185: Add LLM detection for spicy mode
- Evidence bundle: iteration_004 from spicy_mode_comprehensive_real test
