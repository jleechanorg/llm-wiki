# Evidence Bundle Compliance - COMPLETED

## Date Completed
2026-01-22

## Summary
All 4 infrastructure fixes implemented in testing_mcp/lib/evidence_utils.py

## Changes Made

### 1. Per-scenario Raw LLM Output Files ✅
- Extract narratives from request_responses.jsonl (path: [*].response.result.narrative)
- Save to artifacts/raw_{model}_{scenario_name}.txt
- Generate SHA256 checksums for each file
- Commit: 6a378384d (initial), b1af87b27 (path fix)

### 2. Enhanced Claim → Artifact Map ✅
- Added "Key Field(s)" column with JSON paths
- Examples: scenarios[*].passed, scenarios[*].classifier_metadata.{intent,source,confidence}
- Improves traceability to exact data locations
- Commit: 6a378384d

### 3. Capture Mode Documentation ✅
- Added metadata.json → capture_mode field
- Documents: llm_outputs, system_instructions, request_responses capture methods
- Improves evidence bundle transparency
- Commit: 6a378384d

### 4. Methodology Template Accuracy ✅
- Removed false claim about raw_response_text in server.log
- Added accurate description of per-scenario raw files
- server.log now documented as operational logs only
- Commit: 6a378384d

## Testing
Evidence bundle verified in iteration_002:
- ✅ Claim → Artifact Map has 3 columns
- ✅ metadata.json has capture_mode field
- ✅ methodology.md mentions per-scenario files
- ⚠️  Raw files need final verification after path fix

## Next Steps
- Run test to verify raw files are created with path fix
- Update bead status to ✅ Complete
