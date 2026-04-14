# BD-8w7

## GOAL
Extend self-hosted CI reliability coverage so all relevant self-hosted workflows that execute Python setup use a deterministic, writable tool-cache location.

## MODIFICATION
- Added a shared setup step/script (`scripts/ci/setup-runner-tool-cache.sh`) to define a writable tool-cache directory for runner setup actions.
- Applied it in self-hosted workflow paths that currently call `actions/setup-python`:
  - `.github/workflows/test.yml`
  - `.github/workflows/coverage.yml`
  - `.github/workflows/doc-size-check.yml`
  - `.github/workflows/hook-tests.yml`
  - `.github/workflows/mcp-smoke-tests.yml` (`try-self-hosted` job)
- Wired it via `GITHUB_ENV` so subsequent setup steps inherit `AGENT_TOOLSDIRECTORY` and `RUNNER_TOOL_CACHE`.
- Did not apply it to self-hosted shard jobs that do not call `actions/setup-python`; those jobs already use `scripts/venv_utils.sh`, which now uses writable fallback venv roots.

## NECESSITY
Self-hosted runner failures on paths like `/Users/runner` can break setup before test execution. A shared bootstrap removes a class of permission-dependent infra failures while preserving current test behavior.

## INTEGRATION PROOF
- Added `scripts/ci/setup-runner-tool-cache.sh`.
- Updated `.github/workflows/test.yml`, `.github/workflows/coverage.yml`, `.github/workflows/doc-size-check.yml`, `.github/workflows/hook-tests.yml`, and `.github/workflows/mcp-smoke-tests.yml` to call the tool-cache bootstrap step before `actions/setup-python` where applicable.

## BLOCKS
- BD-fac
