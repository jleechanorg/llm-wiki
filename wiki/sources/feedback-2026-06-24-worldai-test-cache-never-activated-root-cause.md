---
title: "WORLDAI_TEST_CACHE activation contract — root cause + fix (PR #7901)"
type: source
tags: [worldarchitect, cache, testing, activation-contract, env-vars, tdd]
date: 2026-06-24
source_file: raw/feedback_2026-06-24_worldai_test_cache_never_activated_root_cause.md
---

## Summary

PR #7810 (2026-06-22) added a `WORLDAI_IS_SERVER_PROCESS` bypass to `ServerCacheManager.enabled()` but the bypass was dead code — `enabled()` checks `WORLDAI_TEST_CACHE` first and returns `False` before ever reaching the bypass. PR #7901 (merged 2026-06-24, commit `0d03b317c4`) fixed this by adding `env.setdefault("WORLDAI_TEST_CACHE", "read_write")` to `start_local_mcp_server()`. This established a durable **multi-gate activation contract rule**: each gate of a multi-condition `enabled()` must be satisfied by the standard startup path, not by test overrides.

## Key Claims

- `ServerCacheManager.enabled` requires `WORLDAI_TEST_CACHE` to be set explicitly; `WORLDAI_IS_SERVER_PROCESS=true` alone is insufficient and the bypass at line 117 is unreachable without the env var.
- The cache-integrity launchd job (PR #7810) set `WORLDAI_TEST_CACHE` in its launchd env, so *those* CI tests passed — masking the gap for all regular `testing_mcp/` runs.
- Classic "test proves the wrong env" failure class: CI passing ≠ feature active on the actual production/test code path.
- The `_temp_env` pattern (fully clears `os.environ` + restores on exit) is more reliable than `mock.patch.dict` for testing env-dependent feature flags — no leakage from surrounding test environment.
- Contract tests must prove `enabled()=False` when only the startup code's env is applied, not just `enabled()=True` with the var forced in.

## Key Quotes

> "PR #7810 added the bypass but never set WORLDAI_TEST_CACHE in start_local_mcp_server(). The bypass is dead code because the WORLDAI_TEST_CACHE check fires first."

> "Multi-gate enabled() features need contract tests proving each gate is satisfied by the startup path, not just by force-setting vars in tests."

## Connections

- [[ServerCacheManager]] — the affected class; `enabled()` property at `testing_mcp/lib/llm_response_cache/server_cache.py:110`
- [[ActivationContract]] — pattern: each gate in a multi-condition feature must be exercised by the standard startup path
- [[TempEnvPattern]] — `_temp_env(env)` context manager for isolated env testing
- [[WorldArchitectTestingInfra]] — `testing_mcp/lib/server_utils.py:start_local_mcp_server()`
