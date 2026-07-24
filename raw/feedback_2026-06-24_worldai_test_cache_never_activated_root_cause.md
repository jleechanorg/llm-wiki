---
name: worldai-test-cache-never-activated-root-cause
description: Root cause + fix for WORLDAI_TEST_CACHE never activating for local testing_mcp/ runs; PR #7901 MERGED
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 386e30ef-bb6c-4fb0-b649-1a216554ad45
  bead: rev-7uj75
---

## STATUS: FIXED — PR #7901 merged 2026-06-24T17:45:28Z (merge commit 0d03b317c4)

PR #7810 (merged 2026-06-22, commit c012b56b53) added `WORLDAI_IS_SERVER_PROCESS_KEY=true`
to `server_utils.py` and a bypass in `ServerCacheManager.enabled()` for server processes.
But the bypass is DEAD CODE — `enabled()` checks `WORLDAI_TEST_CACHE` first (line 110-112)
and returns False when not set, before ever reaching the WORLDAI_IS_SERVER_PROCESS_KEY check.

**The fix (PR #7901):** `env.setdefault("WORLDAI_TEST_CACHE", "read_write")` and
`env.setdefault("WORLDAI_TEST_CACHE_ROOT", "/tmp/worldarchitect.ai/cache")` added to
`start_local_mcp_server()` in `testing_mcp/lib/server_utils.py`. Also wired into
`.github/actions/run-pr-preview-test/action.yml` for CI runs.

**Why CI didn't catch it:** The cache-integrity launchd job (also added in PR #7810) sets
`WORLDAI_TEST_CACHE=read_write` explicitly in its launchd environment. So cache integrity tests
PASSED, but regular `testing_mcp/` runs never got the var. Classic "test proves the wrong env."

**Multi-gate activation contract rule (added to AGENTS.md + CLAUDE.md via this PR):**
When a feature has a multi-gate `enabled()` property, each gate must be satisfied by the
standard startup path. A test that explicitly sets the env var does NOT prove the startup
code sets it. Always add a contract test checking `enabled()=False` when only the startup
code's env is applied.

**_temp_env pattern:** Tests use a custom `_temp_env(env)` context manager that fully clears
`os.environ` and restores on exit — more reliable than `mock.patch.dict` for testing env-
dependent feature flags because it guarantees no leakage from surrounding test environment.

**How to apply:** When "cache not working" reports appear:
1. Check `ServerCacheManager.enabled` — explicit `WORLDAI_TEST_CACHE` gate at line 110
2. `WORLDAI_IS_SERVER_PROCESS=true` alone is NOT sufficient; both must be set
3. Verify `start_local_mcp_server()` calls `env.setdefault("WORLDAI_TEST_CACHE", "read_write")`
4. Run `testing_mcp/lib/llm_response_cache/tests/test_server_cache.py` as regression suite

**References:**
- PR [#7901](https://github.com/jleechanorg/worldarchitect.ai/pull/7901) — merge commit `0d03b317c4`
- PR [#7810](https://github.com/jleechanorg/worldarchitect.ai/pull/7810) — original bypass (dead code)
- `testing_mcp/lib/server_utils.py:687` — `env.setdefault("WORLDAI_TEST_CACHE", "read_write")`
- `testing_mcp/lib/llm_response_cache/tests/test_server_cache.py` — 4 contract tests

[[pr-7810-cache-integrity-launchd]]
