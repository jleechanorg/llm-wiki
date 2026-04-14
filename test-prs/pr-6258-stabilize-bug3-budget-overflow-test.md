---
title: "PR #6258: [antig] Stabilize Bug3 Budget Overflow Test"
type: test-pr
date: 2026-04-14
pr_number: 6258
files_changed: [.gitignore, run_parallel_mcp_tests.sh, test_bug3_budget_overflow.py, test_bug3_fast.py, base_test.py, ...]
---

## Summary
Fixes setup latency causing flaky tests, migrates Bug3 budget overflow test strictly to `budget_warnings` verification instead of hallucinated raw usages, and properly adjusts injection multipliers to naturally trigger context compaction limits without violating Firestore's 1MB document boundary. Achieves a 7-Green reproducible stable E2E test run.

## Key Changes
- **run_parallel_mcp_tests.sh**: New script to boot local server, run all testing_mcp tests, aggregate per-test logs
- **test_bug3_budget_overflow.py**: Reworked to use `budget_warnings` (context compaction signals) instead of inferred `raw_llm_usage`, reduced scaffold generation to avoid Firestore size limits
- **test_bug3_fast.py**: Removed (superseded)
- **base_test.py**: Added `MCPTestBase.get_server_log_path()` with parallel-run fallback, updated log parsing for campaign-specific lines
- **.gitignore**: Added test artifact patterns (run_one_test.sh, tests_list.txt, server_output.log)

## Motivation
Bug3 budget overflow test was flaky due to setup latency and used unreliable verification mechanisms. The test now properly triggers context compaction limits while respecting Firestore constraints.