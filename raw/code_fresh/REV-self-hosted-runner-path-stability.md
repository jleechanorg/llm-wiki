# Self-Hosted Runner Path Stability

**Status:** IN_PROGRESS
**Priority:** P1
**Component:** self-hosted runner infrastructure
**Created:** 2026-02-24
**Type:** task
**Labels:** runner, ci, reliability, workflows

## GOAL
Eliminate path-coupled and ownership-related instability in self-hosted runner CI execution.

## MODIFICATION
- Standardize workflow install commands to `python3 -m pip` for self-hosted execution paths.
- Keep strict `_work` ownership/permission hygiene and apply automated repair procedures when drift is detected.
- Document and enforce one-shot migration plus post-migration verification for nested runner layouts.
- Define targeted tool-cache repair for stale wrapper shebangs after runner path changes.

## NECESSITY
Recent CI incidents showed repeated failures from stale absolute paths and ownership drift after runner directory migration, causing checkout and dependency install failures unrelated to application code quality.

## INTEGRATION PROOF
- Design documented in `roadmap/2026-02-24-self-hosted-runner-path-stability-design.md`.
- Existing workflows and scripts impacted include:
  - `.github/workflows/test.yml`
  - `.github/workflows/mcp-smoke-tests.yml`
  - local runner maintenance scripts under `/home/jleechan/actions-runners/`
- Validation path: rerun failed jobs on active PRs and confirm stable pass rates on self-hosted checks.
