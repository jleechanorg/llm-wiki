---
title: "Coverage workflow hardcodes CLI test list — new test files must be registered"
type: source
tags: [agent-orchestrator, coverage, ci, vitest, pr-725]
date: 2026-06-24
source_file: /Users/jleechan/.claude/projects/-Users-jleechan-project-agento-agent-orchestrator/memory/feedback_2026-06-24_coverage_workflow_test_list_hardcode.md
---

## Summary
`.github/workflows/coverage.yml:127` in `jleechanorg/agent-orchestrator` runs an explicit list of 4 test files for CLI coverage: `__tests__/lib/llm-eval.test.ts`, `__tests__/lib/llm-eval.claude.test.ts`, `__tests__/lib/llm-eval.gemini.test.ts`, `__tests__/lib/web-dir.test.ts`. New test files added to `packages/cli/src/__tests__/` (e.g. PR #725's `llm-eval-chain.test.ts`) are NOT picked up by the coverage workflow, even though `packages/cli/vitest.config.ts:49` includes both directories. The hardcoded list overrides the include pattern, so Diff Coverage fails at 0% on new production lines.

## Key Claims
- Coverage workflow has a hardcoded test file list that overrides vitest's `include` pattern — config drift creates silent coverage blind spots.
- When adding a new CLI test file, ALSO update `.github/workflows/coverage.yml:127` to include it, OR replace the hardcoded list with a glob matching vitest's `include` pattern.
- Long-term fix: replace the hardcoded list with `__tests__/lib/llm-eval*.test.ts __tests__/lib/web-dir.test.ts` (wildcard picks up the per-adapter tests and any future llm-eval tests).
- The `coverage.include` filter (`src/lib/llm-eval.ts,src/lib/web-dir.ts`) is also brittle — should be widened to cover all `src/lib/*.ts` files via glob.

## Key Quotes
> "When you add a new test file to `packages/cli/src/__tests__/` (e.g. `llm-eval-chain.test.ts`), the coverage workflow does NOT run it. The default vitest `include` pattern would, but the explicit list overrides it. So: new test file passes locally, coverage workflow only runs the 4 hardcoded files, lines added to `src/lib/llm-eval.ts` are NOT exercised by any test run by the coverage workflow, **Diff Coverage gate fails** at 0% on the new lines."

## Connections
- [[GreenGateCIPattern]] — Diff Coverage is a substantive gate; the admin-squash-bypass cannot exempt it.
- [Pre-existing test contract update when loosening fail-closed (2026-06-24)](feedback-2026-06-24-chain-fallthrough-breaks-pretend-closed-tests.md) — the brittle test list compounds contract-change test breakage; both are CI-config drift patterns.
- [[WorktreeWorkflow]] — same dev/test worktree applies to coverage workflow changes.
