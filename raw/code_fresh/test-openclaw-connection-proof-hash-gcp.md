---
id: test-openclaw-connection-proof-hash-gcp
type: task
priority: 1
status: in_progress
labels: [testing, openclaw, pr-5879]
---

# test(openclaw): GCP real-server test for proof-prompt hash in connection test endpoint

## Description

PR #5879 adds `proof_prompt` → `response_hash` path to
`POST /api/settings/test-openclaw-connection`. No real-server test exercises this path.

## Acceptance Criteria

- `testing_mcp/test_openclaw_connection_proof.py` runs against GCP remote
- Scenario 1: basic connection test (no proof_prompt) → `success=True`
- Scenario 2: connection test with `proof_prompt` → `response_hash` non-empty, `proof_prompt_used=True`
- Evidence bundle created, codex /er returns PASS

## Implementation

`testing_mcp/test_openclaw_connection_proof.py`
