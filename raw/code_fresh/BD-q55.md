# BD-q55

## GOAL
Investigate and resolve the cache reuse order anomaly in `test_llm_wizard_flow_e2e.py` where `action1.cache.source="reused"` precedes `action2.cache.source="created"` — logically impossible if the cache is created within the same test run.

## MODIFICATION
- Inspect the Firestore `cachedContents/4l9ov5kvdnzs1vxf7w7pzqp213lhyv8h5w5x5qd4` entry to determine its creation timestamp vs the test run timestamp (`run_1773554578`, ~2026-03-14T23:04).
- If the cache predates the test run: document that the first story action reused a cache from a prior campaign, and the second action created a new one — add a test assertion or log clarifying which run owns which cache.
- If the cache was created in-run: trace `llm_service.py` cache-write path to find why the `source` field is populated in reverse order.
- Update `test_complete.json` schema docs (or the JSON-emitting code) to clarify `cache.source` field semantics.

## NECESSITY
A `reused`→`created` ordering makes it impossible to distinguish genuine cache reuse from stale cross-campaign cache hits. If a prior campaign's cache is silently reused the LLM context window may differ from what the test expects, producing subtly wrong story responses that pass only because assertions are loose.

## INTEGRATION PROOF
- Evidence artifact: `run_1773554578: llm_wizard_flow_e2e/test_complete.json` (CI artifact or local evidence dir)
- Affected test: `testing_ui/test_llm_wizard_flow_e2e.py`
