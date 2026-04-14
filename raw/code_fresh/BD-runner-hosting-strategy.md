# Runner Hosting Strategy: Host-Agnostic Default, Selective Host-Specific Checks

## ID
BD-runner-hosting-strategy

## Title
Decision record for self-hosted runner hosting strategy and docker adoption

## Status
in_progress

## Type
infrastructure

## Priority
P2

## Created
2026-02-24

## GOAL
Capture the decision for how much of the self-hosted CI surface should be made host-agnostic versus left host-specific, and define where containerized execution adds clear value.

## MODIFICATION
- Add a design decision document at `docs/ci/runner-hosting-strategy.md`.
- Record which existing self-hosted workflows are:
  - host-agnostic and can keep Linux-like assumptions,
  - intentionally host-specific (runner sanity checks),
  - not suitable for immediate dockerization.

## NECESSITY
Recent CI failures showed non-portable assumptions causing runner fragility (notably non-interactive `sudo` calls). The team needs a reusable, documented policy so fixes are consistent across workflows instead of repeated one-off patches.

## INTEGRATION PROOF
- Decision artifact added at `docs/ci/runner-hosting-strategy.md`.
- Current branch already has the immediate hardening fixes in:
  - `.github/workflows/hook-tests.yml`
  - `.github/workflows/test.yml`
  - `.github/workflows/coverage.yml`
  - `scripts/ci/ensure-jq.sh`
  - `scripts/ci/setup-runner-tool-cache.sh`
  - `scripts/setup-all-self-hosted-runners.sh`
  - `.beads/BD-pair_followup3-ci-test-hardened-venv-bootstrap.md` (follow-up and context link).

## Decision Record
Default to host-agnostic workflows for CI logic, with explicit separate host-specific jobs only for runner infrastructure verification (e.g., runner binary checks). Defer full containerization of all self-hosted jobs to a dedicated follow-up PR after this policy is implemented and validated.
