---
title: "Runtime activation claim required — multi-gate \"X is working\" must cite probe output"
type: source
tags: [worldarchitect, cache, harness, activation-contract, agent-discipline, zfc]
date: 2026-06-24
source_file: raw/feedback_2026-06-24_runtime_activation_claim_required.md
---

## Summary

The "cache is working" / "feature X enabled" / "warmup completed" claim pattern has failed 4+ times across PRs #7810, #7892, #7901 and 8+ worktree branches. Generalization: any multi-gate `enabled()` feature is susceptible. New rule: any claim that a multi-gate feature is "working" MUST cite a runtime probe output from the **standard harness startup path**, NOT from a launchd/cron test that explicitly sets the activation var.

## Key Claims

- Agents accept test runs that explicitly set the activation env var as proof that the standard harness path activates the feature. The standard path is a different code path with a different env. Test passes ≠ feature works in standard harness.
- The standard harness startup path differs from test/launchd env in 3 ways: (a) env not pre-set by test fixture; (b) pytest is not in sys.modules; (c) subprocess boundary ensures no parent-shell env leaks.
- None of these are tested by `with mock.patch.dict(os.environ, {"WORLDAI_TEST_CACHE": "read_write"}):`.
- Generalizes to: FastEmbed classifier, prompt embed LRU, FastAPI warmup, gunicorn worker init, embed cache, BQ cache probes, any feature gated by env var + pytest detection + bypass.

## Required Pattern

1. Read the source of the activation function (e.g., `ServerCacheManager.enabled`).
2. Identify each gate the function checks.
3. For each gate, state what env/state is required.
4. Run a probe in a CLEAN subprocess with NO env override.
5. The probe output MUST be `True` before claiming the feature works.
6. Quote the probe output verbatim in the claim.

## Banned Patterns

- "Cache works" based on launchd/cron test logs where the launchd env set the activation var.
- "Feature X works" based on a CI run where the env was set via `mock.patch.dict`.
- "Warmup completed" based on `_init_event.wait()` returning (set at init, not at warmup completion).
- "enabled=True" based on reading the source code without running it.

## Key Quotes

> "PR #7810 added the bypass but never set WORLDAI_TEST_CACHE in start_local_mcp_server(). The bypass is dead code because the WORLDAI_TEST_CACHE check fires first."

> "Test passes ≠ feature works in standard harness. The standard path is what `start_local_mcp_server()` calls."

## Connections

- [[ServerCacheManager]] — the affected class; `enabled()` property at `testing_mcp/lib/llm_response_cache/server_cache.py:106`
- [[ActivationContract]] — pattern: each gate in a multi-condition feature must be exercised by the standard startup path
- [[WORLDAI_TEST_CACHE]] — the original cache activation contract
- [[PR_7901]] — the fix that established the multi-gate activation contract rule
- [[probe-too-clean]] — the third class of false-claim (env stripped too aggressively)
- [[no-blocking-hook]] — /advice verdict: don't ship blocking PreToolUse hook
