---
name: worldai-test-cache-default-read-write
description: WORLDAI_TEST_CACHE default changed to read_write in PR
metadata: 
  node_type: memory
  type: project
  bead: none
  originSessionId: 3f10d684-e8e3-43ea-b664-00db2975d3a9
---

## WORLDAI_TEST_CACHE default is now read_write

**File**: `testing_mcp/lib/llm_response_cache/config.py`

`_parse_mode()` now returns `"read_write"` when `WORLDAI_TEST_CACHE` is unset (was `"off"`).

**To disable**: `WORLDAI_TEST_CACHE=off`

**Effect**: All testing_mcp tests now use the two-tier LLM response cache by default, saving ~59% of Gemini API calls across repeated test runs on the same branch.

**Merged**: PR #7066 → main commit `e6ab5b1cba` on 2026-05-24

**How to apply**: Any new testing_mcp work should be aware the cache is active. Use `WORLDAI_TEST_CACHE=off` in environments where cache warm-hits would mask test failures.

**References**: https://github.com/jleechanorg/worldarchitect.ai/pull/7066
