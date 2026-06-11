# Smoke Mode Routing CI Guards (2026-06-10)

**Type**: feedback | **Bead**: rev-k8jq1

Three CI guards added to `mcp-smoke-tests.yml` to prevent silent `/smoke`→mock regression:

1. Runtime assertion in `determine-smoke-mode.sh` — `issue_comment` + no mode must resolve to `real`
2. Grep gate — `determine-smoke-mode.sh` still called from workflow (≥2 occurrences)
3. Grep gate — `try-self-hosted` job still has `TEST_MODE: mock` hardcoded

**Key insight**: Two independent mock-enforcement mechanisms exist (the routing script and a hardcoded env block). Guards must cover both independently.

**Evidence exception**: scripts/CI-only changes don't require real-LLM `/es` bundles — contract tests are sufficient.

**PRs**: [#7242](https://github.com/jleechanorg/worldarchitect.ai/pull/7242) fix, [#7446](https://github.com/jleechanorg/worldarchitect.ai/pull/7446) guards
