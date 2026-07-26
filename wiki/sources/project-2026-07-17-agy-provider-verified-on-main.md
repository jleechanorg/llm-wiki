---
title: "AGY provider verified working on origin/main (2026-07-17)"
type: source
tags: [agy, llm-provider, worldarchitect, testing-mcp, verification]
date: 2026-07-17
source_file: raw/project_2026-07-17_agy_provider_verified_on_main.md
---

## Summary
The AGY CLI provider works end-to-end on fresh worldarchitect.ai origin/main
(`2d65754fa3`, 2026-07-17), verified locally with the real-mode testing_mcp
integration test — real gunicorn server, real AGY subprocess LLM calls, no
mocks. Both scenarios passed, including the load-bearing typed-tool dice turn
where AGY requests `roll_skill_check` and the server owns execution.

## Key Claims
- `testing_mcp/dice/test_agy_provider_default_integration.py` passed 2/2 with
  `AGY_PROVIDER_ENABLED` unset (implicit local default activation via
  `WORLDAI_PROD=false`).
- Evidence asserts `provider_mode=agy`, `provider_type=agy`,
  `tool_requests_executed=True` — no Gemini SDK/BYOK leak, no Gemini
  code-execution claim.
- Only machine preconditions: agy CLI liveness (`agy --print ... "pong"` probe)
  and the sanitized runtime home `~/.cache/worldai/agy-clean-home-v1`.
- The 15 commits on `origin/feat/agy-provider-follows-gemini` beyond main are
  follow-on work, not required for the provider to function on main.

## Key Quotes
> "Total scenarios: 2 / Passed: 2 / Failed: 0" — test summary, evidence bundle
> `/tmp/worldarchitect.ai/dev-agy-verify/agy_provider_default/iteration_001`

## Connections
- [[AgyCli]] — the provider under test; auth durability covered in the
  2026-07-11 Keychain source
- [[WorldArchitectAI]] — repo whose local-default LLM provider this is
- [[TestingMcpRealMode]] — the no-mock real-service test layer that produced
  the evidence
- [[ServerOwnedDice]] — the typed-tool boundary this test proves (model
  requests, server rolls)
