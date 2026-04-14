# BD-pair_followup3-ci-test-hardened-venv-bootstrap

## ID
BD-pair_followup3-ci-test-hardened-venv-bootstrap

## Title
pair_followup3-ci: adopt hardened virtualenv bootstrap in test workflow

## Status
closed

## Type
infrastructure

## Priority
medium

## Created
2026-02-24

## Description
[PR `#5734`](https://github.com/jleechanorg/worldarchitect.ai/pull/5734) documented a follow-up decision to evaluate mixed versus hardened `.github/workflows/test.yml` virtualenv bootstrap paths. This bead records the decision and acceptance criteria that were completed in PR `#5751`.

## Definitions
For the purposes of this evaluation:
- **Current main bootstrap path**: The venv bootstrap logic present on `main` in `.github/workflows/test.yml` (around lines 304–365). This path uses the cached venv when available, performs a health check, enforces a bootstrap timeout, and falls back to creating a fresh venv if the cache is unhealthy or bootstrap exceeds the timeout.
- **Hardened bootstrap path**: A stricter variant of the bootstrap logic that favors correctness and determinism over speed. Concretely, it tightens or disables reuse of a potentially unhealthy cached venv, treats health-check or timeout failures as hard failures (or forces a full rebuild), and minimizes silent fallback behavior so that bootstrap issues are surfaced clearly in CI.
- **Mixed bootstrap path**: A configuration in which the workflow runs both variants in CI (for example, some jobs or matrix entries use the current main bootstrap path while others use the hardened bootstrap path) to compare performance, flakiness, and failure modes before committing to a single strategy.

## Decision Criteria
The hardened path was chosen based on:
- CI stability and flake rate, with no regressions compared to the current `main` bootstrap path.
- End-to-end test runtime and resource usage remaining within the agreed CI budget.
- Reproducibility between local and CI environments, including dependency pinning and isolation.
- Security posture of dependency installation and caching (e.g., reduced supply-chain risk).
- Operational complexity for developers and release engineers, including ease of debugging and maintenance.

## Scope
- `.github/workflows/test.yml`

## Acceptance
- Record and close out the bootstrap decision:
  - compare the `main` bootstrap path against the hardened bootstrap path proposed in `PR #5734`,
  - retain only one canonical path in CI,
  - document rationale for the retained path in this bead.
- Keep CI bootstrap behavior deterministic and documented for future maintenance.
- Preserve the final decision in this bead.

## Decision
- Adopted the hardened bootstrap path in the follow-up PR (`.github/workflows/test.yml`).
- The hardened path removes `source venv/bin/activate` in CI bootstrap and uses explicit `venv/bin/python`/`venv/bin/pip` invocation for install and validation.
- This reduces stale activation-state risks on self-hosted runners and makes venv usage deterministic across cache restores.

## Close Reason
Implemented by `pair_followup3-ci-test-hardened-venv-bootstrap` in
`.github/workflows/test.yml`; venv validation and install now execute through explicit interpreter/pip paths (no activation of `venv/bin/activate`), and CI runtime is made deterministic by passing `VIRTUAL_ENV` explicitly.

## Notes
- Follow-up PR body includes explicit decision criteria and this bead link.
- Additional hardening: Install step validates venv via explicit $VENV_PY invocations (no vpython/activate). Test step exports `VIRTUAL_ENV=$PWD/venv` so `run_tests.sh`/`ensure_venv` skips sourcing activate, eliminating activation entirely in CI.
