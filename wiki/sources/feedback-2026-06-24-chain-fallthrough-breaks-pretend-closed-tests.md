---
title: "Pre-existing test contract update when loosening fail-closed behavior"
type: source
tags: [agent-orchestrator, llm-eval, testing, contract-change, pr-725]
date: 2026-06-24
source_file: /Users/jleechan/.claude/projects/-Users-jleechan-project-agento-agent-orchestrator/memory/feedback_2026-06-24_chain_fallthrough_breaks_pretend_closed_tests.md
---

## Summary
When a behavior PR removes a hard-fail branch in production code, pre-existing tests that encoded the old hard-fail output format will fail under the new contract. The fix is to update those tests in the same commit, not as a follow-up — Diff Coverage gate (a substantive gate) will block the merge otherwise. PR #725 in `jleechanorg/agent-orchestrator` had to rewrite `llm-eval.gemini.test.ts:225` from "fails closed when gemini omits a verdict" to "falls through to next model" to land the chain-loosening refactor.

## Key Claims
- Behavior-change PRs that remove a hard-fail branch (e.g. "missing VERDICT now falls through to next model") WILL break pre-existing tests that asserted the old hard-fail output format.
- These broken tests are not "regressions" — they encode the deliberate contract change.
- Diff Coverage is a substantive gate (not a service gate), so the admin-squash-bypass pattern does not exempt it. The test must be updated in the same PR.
- The pattern: grep for `<old contract signature>` in `packages/cli/__tests__/` BEFORE pushing the behavior change; rewrite or replace each test that asserts the old format.

## Key Quotes
> "When a behavior PR removes a hard-fail branch (e.g. 'missing VERDICT now falls through'), pre-existing tests that asserted the hard-fail format will fail under the new contract. The fix must update those tests in the same commit — not as a follow-up."

## Connections
- [[AdminOverrideContractWiring]] — admin-squash-bypass requires substantive gates to PASS; a broken Diff Coverage test blocks the bypass.
- [[GreenGateCIPattern]] — substantive vs service gate distinction determines which checks can be bypassed.
- [[PostMergeFollowupWorkflow]] — keeping test updates in the same PR (not as a follow-up) avoids the same-outage deadlock.
- [Coverage workflow hardcodes CLI test list (2026-06-24)](feedback-2026-06-24-coverage-workflow-test-list-hardcode.md) — related root cause: brittle test file list compounds the contract-change breakage.
