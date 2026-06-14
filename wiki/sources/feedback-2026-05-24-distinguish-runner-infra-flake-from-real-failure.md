---
title: "Self-Hosted Runner Infra Flakes Show as CheckRun FAILURE — Must Distinguish from Real Test Failures"
type: source
tags: [self-hosted-runner, ci, infra-flake, check-runs, monitor]
sources: []
last_updated: 2026-05-24
source_file: raw/feedback_2026-05-24_distinguish_runner_infra_flake_from_real_failure.md
---

## Summary
A `Directory tests (core-mvp-N(self hosted))` CheckRun FAILURE may be `runner lost communication` — a pure infrastructure flake, not a real test failure. The cause is only visible via `gh api repos/<owner>/<repo>/check-runs/<job-id>/annotations`, NOT via `gh run view --log-failed` (which returns empty while the run is still in progress overall). GitHub Actions auto-retries the job within seconds (new job id, same check name), and the retry usually passes cleanly.

## Key Claims
- When a self-hosted CI job FAILS, check `gh api repos/X/Y/check-runs/<id>/annotations` BEFORE diagnosing test logic.
- "runner lost communication" / "starves it for CPU/Memory" annotations are infra flakes — wait for the auto-retry, don't push a fix commit.
- Monitor loops watching for "real failures" should compute the LATEST check-run per name (not just count any FAILURE), since the retry will land as a new check-run with the same name.
- Diagnostic endpoint: `gh api repos/<owner>/<repo>/check-runs/<job-id>/annotations` returns annotation text including the cause.
- Reusable monitor query: group check-runs by name, sort by `started_at`, take the LAST per name, then count failures. A real failure = the latest run for any check-name has `conclusion == "failure"`.

## Key Quotes
> "When a self-hosted CI job FAILS, always check `gh api repos/X/Y/check-runs/<id>/annotations` BEFORE diagnosing test logic." — feedback_2026-05-24_distinguish_runner_infra_flake_from_real_failure

> "'runner lost communication' / 'starves it for CPU/Memory' annotations are infra flakes — wait for the auto-retry, don't push a fix commit." — feedback_2026-05-24_distinguish_runner_infra_flake_from_real_failure

> "Monitor loops watching for 'real failures' should compute the LATEST check-run per name (not just count any FAILURE), since the retry will land as a new check-run with the same name." — feedback_2026-05-24_distinguish_runner_infra_flake_from_real_failure

## Connections
- [[7-Green-Proof-Artifact]] — PR #7048 was the first session to surface this distinction
- [[PR-7048-Location-Centralization-Merged]] — the PR where the flake appeared
- [[Self-Hosted-Runner-Setup]] — the underlying infrastructure
- [[CI-Worktree-Runner-Infra]] — broader runner infra context
- [[Green-Gate-CI-Pattern]] — 6-gate pattern that consumes check-run state
