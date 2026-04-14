# Raw Output "Unknown" Prefix Investigation

## Status
🟡 Investigation Required - Evidence Integrity Question

## Created
2026-01-22

## Type
Evidence Quality Issue (Priority 1 - Investigation)

## Scope
- testing_mcp/lib/evidence_utils.py - Raw output file naming
- Evidence Bundle: iteration_004 artifacts

## Problem Statement

### Unexpected File Naming
**Expected:** `raw_<scenario_name>.txt`
**Actual:** `raw_unknown_<scenario_name>.txt`

**Evidence Files:**
```
/tmp/worldarchitect.ai/.../iteration_004/artifacts/
  raw_unknown_companion_emotional_query.txt
  raw_unknown_npc_conversation.txt
  raw_unknown_persuade_guard.txt
  raw_unknown_quoted_dialog.txt
  raw_unknown_social_negotiation.txt
```

### What "Unknown" Suggests
The `unknown` prefix typically indicates:
1. **Classifier source not captured** - Metadata tracking failed
2. **Fallback naming** - Code couldn't determine proper scenario identifier
3. **Missing metadata** - Agent/intent information unavailable at capture time
4. **Debug mode artifact** - Test infrastructure bug

### Why This Matters
- **Evidence Integrity:** Are these actually semantic classification results?
- **Metadata Tracking:** Is classifier source properly captured in metadata?
- **Test Infrastructure:** Is evidence capture working correctly?
- **Reproducibility:** Can we trust the evidence bundle structure?

## Current Evidence

### File Naming Pattern
All raw output files have `unknown` prefix, suggesting **systematic issue** not random error.

### Metadata Verification Needed
Check if classification metadata is correctly captured:
```json
{
  "classifier_metadata": {
    "agent_name": "DialogAgent",
    "intent": "dialog",
    "classifier_source": "semantic_intent",  // ← Is this captured?
    "confidence": 0.698793351650238,
    "routing_priority": "7_semantic_intent"
  }
}
```

### run.json Analysis
**From iteration_004/run.json:**
All scenarios show:
- `"classifier_source": "semantic_intent"` ✅
- `"intent": "dialog"` ✅
- `"confidence": 0.69-0.74` ✅

**Contradiction:** Metadata shows semantic classification was used, but file names suggest "unknown" source.

## Investigation Steps

### Step 1: Locate File Naming Logic
**File:** `testing_mcp/lib/evidence_utils.py`
**Search for:** `raw_unknown` or file naming logic in evidence capture

```bash
grep -n "raw_unknown\|raw_.*\.txt" testing_mcp/lib/evidence_utils.py
```

### Step 2: Check Evidence Capture Code
**Hypothesis:** Code might use placeholder "unknown" when:
- Scenario name not available at capture time
- Agent type unknown
- Classifier source not in expected enum

**Expected Logic:**
```python
def save_raw_output(scenario_name, output):
    filename = f"raw_{scenario_name}.txt"  # ← What actually happens?
```

**Actual Logic (?):**
```python
def save_raw_output(scenario_name, output):
    # BUG: scenario_name might be None or empty
    filename = f"raw_{scenario_name or 'unknown'}.txt"
```

### Step 3: Test Evidence Capture
**Run single test and observe:**
```bash
TESTING=true vpython -c "
from testing_mcp.test_dialog_agent_real_e2e import *
# Run one scenario and check file name
"
```

### Step 4: Review Metadata Capture Timing
**Hypothesis:** File is saved BEFORE classification metadata is available

**Timeline:**
1. Test sends user input
2. MCP server processes request
3. **File saved here?** → No metadata yet → "unknown" prefix
4. Classification happens
5. Metadata captured
6. **File should be renamed or saved later**

## Possible Root Causes

### Cause 1: Early File Save (MOST LIKELY)
Raw output saved before classification metadata available.

**Fix:** Delay file save until after classification completes.

### Cause 2: Missing Scenario Metadata
Scenario name not passed to evidence capture function.

**Fix:** Ensure scenario name propagates through capture pipeline.

### Cause 3: Backward Compatibility
Old naming convention preserved for compatibility.

**Fix:** Update naming convention and document change.

### Cause 4: Debug Mode Artifact
Test infrastructure uses "unknown" prefix during development.

**Fix:** Remove debug naming, use production naming.

## Solution

### Option 1: Fix File Naming Logic (RECOMMENDED)
**Action:** Ensure files are named with actual scenario names, not "unknown"

**Changes:**
1. Find evidence capture code in `evidence_utils.py`
2. Fix scenario name propagation
3. Update file save timing (after classification)
4. Re-run tests and verify correct naming

### Option 2: Document and Accept
**Action:** Document that "unknown" is expected behavior

**Rationale:**
- Metadata IS correctly captured in run.json
- File naming is cosmetic issue
- Evidence integrity not compromised

**Changes:**
1. Update evidence bundle documentation
2. Explain "unknown" prefix in README.md
3. No code changes needed

## Recommended Action

**Investigate FIRST, then fix if needed:**

1. **Search code:** `grep -r "raw_unknown" testing_mcp/`
2. **Check metadata:** Verify classifier_source in run.json matches actual classification
3. **Run test:** Single scenario with debug logging to trace file creation
4. **Determine severity:**
   - If metadata is correct: P2 (cosmetic issue)
   - If metadata is wrong: P0 (evidence integrity issue)

## Acceptance Criteria
- [ ] Root cause identified
- [ ] Severity determined (P0 if metadata wrong, P2 if cosmetic)
- [ ] Fix implemented OR documented as expected behavior
- [ ] Re-run tests to verify correct file naming
- [ ] Update evidence bundle documentation

## Related Beads
- evidence-bundle-compliance (evidence infrastructure)
- multi-intent-evidence-capture (test infrastructure)

## Priority
**P1 - Investigation Required**
- Must investigate before PR merge
- Could be evidence integrity issue OR cosmetic naming issue
- Risk: If metadata tracking is broken, cannot trust classification results

---

**Investigation Evidence:**
- Files: `/tmp/worldarchitect.ai/.../iteration_004/artifacts/raw_unknown_*.txt`
- Metadata: `/tmp/worldarchitect.ai/.../iteration_004/run.json` (shows correct classifier_source)
- Code: `testing_mcp/lib/evidence_utils.py` (needs review)
