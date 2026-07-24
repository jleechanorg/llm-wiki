---
name: coverage-workflow-hardcodes-cli-test-list-new-test-files-must-be-registered
description: .github/workflows/coverage.yml:127 has a hardcoded test file list; new llm-eval test files must be added there or Diff Coverage fails silently
metadata:
  node_type: memory
  type: feedback
  originSessionId: f08ff1d4-c6cb-4622-bf6a-aeb6ccd60c47
  bead: bd-0f3i
---

# Coverage workflow hardcodes CLI test list at coverage.yml:127

## The problem

`packages/cli` has two test directories:
- `packages/cli/__tests__/` (top-level — commands, lib/, scripts/)
- `packages/cli/src/__tests__/` (src-relative — for tests colocated with source)

Vitest config (`packages/cli/vitest.config.ts:49`) includes BOTH:
```ts
include: ["__tests__/**/*.test.ts", "src/__tests__/**/*.test.ts"]
```

But the **coverage workflow** at `.github/workflows/coverage.yml:127` runs an explicit file list:
```yaml
run: npx vitest run --coverage --coverage.reporter=lcov \
  --coverage.include='src/lib/llm-eval.ts,src/lib/web-dir.ts' \
  --coverage.exclude='**/__tests__/**' \
  __tests__/lib/llm-eval.test.ts \
  __tests__/lib/llm-eval.claude.test.ts \
  __tests__/lib/llm-eval.gemini.test.ts \
  __tests__/lib/web-dir.test.ts
```

When you add a new test file to `packages/cli/src/__tests__/` (e.g. `llm-eval-chain.test.ts`), the coverage workflow does NOT run it. The default vitest `include` pattern would, but the explicit list overrides it. So:

1. New test file passes locally
2. Coverage workflow only runs the 4 hardcoded files
3. Lines added to `src/lib/llm-eval.ts` are NOT exercised by any test run by the coverage workflow
4. **Diff Coverage gate fails** at 0% on the new lines

## What to do when adding a new CLI test file

**Option A — preferred**: Update `.github/workflows/coverage.yml:127` to add the new test file. This is the long-term fix because the hardcoded list is brittle.

**Option B — short-term**: Don't add the new test file to `src/__tests__/`. Add it to `__tests__/lib/` instead so it's covered by the existing list. (Suboptimal — colocates tests outside the source dir they test.)

**Option C — best long-term**: Replace the hardcoded list with a glob that matches the vitest `include` pattern. e.g. `--coverage.include='src/lib/llm-eval.ts,src/lib/web-dir.ts' __tests__/lib/llm-eval*.test.ts __tests__/lib/web-dir.test.ts`. (Note `lib/llm-eval*.test.ts` glob — the wildcard picks up the per-adapter tests and any future llm-eval tests.)

## Why this is brittle (root cause)

The coverage workflow was written before the dual-directory test layout (when all tests were in `__tests__/lib/`). When tests started being added to `src/__tests__/` (closer to source), the workflow wasn't updated. The "service outage → can't ship" pressure is exactly when this kind of latent config drift bites.

## How to apply

When writing a PR that adds a new test file in `packages/cli/src/__tests__/`:

1. **Before pushing**, run the exact command from `.github/workflows/coverage.yml:127` locally (replace the explicit file list with the new file added):
   ```bash
   cd packages/cli
   npx vitest run --coverage --coverage.reporter=lcov \
     --coverage.include='src/lib/llm-eval.ts' \
     __tests__/lib/llm-eval.test.ts __tests__/lib/llm-eval.claude.test.ts \
     __tests__/lib/llm-eval.gemini.test.ts __tests__/lib/llm-eval-chain.test.ts
   ```
2. If the diff coverage is < 70%, the test file isn't enough — either:
   - The test doesn't cover the new code paths
   - The test list in coverage.yml is missing this file
3. **Add the new file to `coverage.yml`** so it runs in CI
4. Verify: push the change to coverage.yml in the same PR

## References

- `.github/workflows/coverage.yml:127` — hardcoded list
- `packages/cli/vitest.config.ts:49` — vitest include pattern
- PR [#725](https://github.com/jleechanorg/agent-orchestrator/pull/725) — `llm-eval-chain.test.ts` added at `packages/cli/src/__tests__/`. Coverage initially failed until test was added implicitly via `__tests__/lib/llm-eval.gemini.test.ts` rewrite (which IS in the hardcoded list and covers the new code path indirectly through shared module imports).
