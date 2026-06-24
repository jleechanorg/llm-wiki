---
name: pre-existing-test-contract-update-when-loosening-fail-closed-behavior
description: "When relaxing a hard-fail contract in production code, pre-existing tests that encoded the old contract will fail; update them in the same PR."
metadata:
  node_type: memory
  type: feedback
  originSessionId: f08ff1d4-c6cb-4622-bf6a-aeb6ccd60c47
  bead: bd-qbjp
---

When a behavior PR removes a hard-fail branch (e.g. "missing VERDICT now falls through"), **pre-existing tests that asserted the hard-fail format will fail under the new contract**. The fix must update those tests in the same commit — not as a follow-up. PR #725: chain-loosening removed `isMissingVerdict` hard-fail, and `__tests__/lib/llm-eval.gemini.test.ts:225` (`"fails closed when gemini omits a verdict with model=gemini"`) hard-coded the old `"gemini: missing VERDICT"` format. Diff Coverage gate failed until that test was rewritten to assert the new fall-through contract.

**Why:** Coverage workflow runs the existing test files. If a test fails, the workflow fails. The test isn't a "regression" — it's a deliberate contract change. The pre-existing test needs to be updated as part of the same PR that changes the contract.

**How to apply:** Before merging a behavior-change PR:
1. `grep -rn "<old contract signature>" packages/cli/__tests__/` — find tests that encode the old contract
2. Update each test to assert the new contract (fall-through, exhaust, etc.)
3. If a test only makes sense under the old contract, delete it or replace it with a new test for the new contract
4. Run the full test set locally before pushing: `cd packages/cli && pnpm vitest run __tests__/lib/llm-eval*.test.ts __tests__/lib/web-dir.test.ts __tests__/lib/llm-eval-shared.test.ts src/__tests__/llm-eval-chain.test.ts`

**Lesson for next time:** When the PR title says "loosen" or "remove hard-fail" or "fall through", the diff WILL break pre-existing tests that asserted the hard-fail output. Plan the test update as part of the PR, not as a follow-up.

**Why this matters here:** Coverage gate is one of the substantive gates that admin-squash-bypass requires to PASS. A pre-existing test that breaks under the new contract blocks the bypass — and a service-blocked Skeptic Gate means we can't ship the behavior change without the bypass. So this isn't just a TDD hygiene issue; it's a gate-blocking issue.

**Provenance:** PR #725 (`feat/llm-eval-chain-loosen` → `8ba9b115`), audit at `/tmp/audit_report_pr725.md`, body at `/tmp/pr725_body.md`. The diff fix was a 16-line test rewrite in `llm-eval.gemini.test.ts:225-245`.
