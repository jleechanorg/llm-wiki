---
title: "Inline 7-green drive beats subagent fanout (PRs #7564 + #7565)"
type: source
tags: [7-green, green-gate, skeptic-gate, subagent-fanout, github-actions, bq-logging, adversarial-review, feedback]
date: 2026-06-15
source_file: raw/project_2026-06-15_pr7564_7565_merged_after_review.md
---

## Summary

Subagent fanout for "drive PRs to 7-green" over-dispatches smoke and Green Gate workflow runs, wasting CI capacity and getting stuck in queued-runner wait loops. Direct operator drive (single Bash agent, explicit `gh workflow run` triggers, per-SHA `check-runs` API queries) is the right control surface. Skeptic verdicts on prior SHAs persist and block GG; `SKEPTIC_GATE_TRIGGER` comments do NOT auto-trigger skeptic-self-verify.yml — must use `gh workflow run`. `gh pr view --json statusCheckRollup` shows STALE entries; `gh api .../commits/<sha>/check-runs` is the authoritative per-SHA view. For BQ-logging PRs, preempt the user's "adversarial review" instinct with a code-review agent classification of every change.

## Key Claims

- Subagent approach for 7-green drive over-dispatches smoke and GG runs (2+ per PR), wastes CI capacity; cancel redundant queued runs via `gh api -X POST .../actions/runs/<id>/cancel`
- Subagents stuck in `gh run watch` loop while runner pool saturated — kill via TaskStop and take over directly
- `SKEPTIC_GATE_TRIGGER` PR comment does NOT auto-trigger `skeptic-self-verify.yml` — must explicitly `gh workflow run skeptic-self-verify.yml -f pr_number=N --ref <branch>`
- Stale skeptic verdicts (>4h old) block GG even after smoke+body fixes — re-trigger to get fresh verdict
- `gh pr view --json statusCheckRollup` shows STALE entries from old SHAs — use `gh api repos/.../commits/<sha>/check-runs` for authoritative per-SHA view
- Cancel API gotcha: `/actions/runs` endpoint returns `databaseId: null` (broken for jq); use `/actions/workflows/<wf>/runs` for real `id` values
- For BQ-logging PRs, preempt adversarial review with code-review agent classification: LOGGING_ONLY / LOGGING_INFRASTRUCTURE / TEST_ONLY / PROD_BEHAVIOR_CHANGE / NEEDS_HUMAN
- PR #7564 (test fix) MERGED @d9bc9a764; PR #7565 (BQ OpenAI proxy logging) MERGED @e8ffde8a8 with 4 files classified: 2 prod LOGGING_ONLY + 2 tests TEST_ONLY

## Key Quotes

> "Subagent dispatched 2+ smoke runs and 2+ GG runs per PR, wasting CI capacity — I had to cancel redundant queued runs (id 27573120508 + 27573119800)"

> "SKEPTIC_GATE_TRIGGER comment alone does NOT auto-trigger skeptic-self-verify.yml — must explicitly trigger via `gh workflow run skeptic-self-verify.yml -f pr_number=N --ref <branch>`"

> "New `user_id: str | None = None` param on `invoke_openclaw_gateway*` defaults to None; existing Flask call sites in `mvp_site/main.py:1954, :2040` don't pass it — backward compatible"

## Connections

- [[GreenGate]] — workflow with `cancel-in-progress: true`; comment-triggered cascades from AO workers
- [[SkepticGate]] — self-verify workflow requires explicit `gh workflow run`, not just trigger comment
- [[AOWorker]] — subagent fanout approach over-dispatches; better as monitor-only delegating to Bash
- [[AdversarialEvaluation]] — for BQ-logging PRs use code-review agent to classify changes
- [[BQLogging]] — BQ instrumentation pattern with try/except fail-open + double-gated by `bq_logging_enabled()` and `provider_logging_suppressed()`
- [[PR7564]] — test fix (echo no-op hook validation)
- [[PR7565]] — OpenAI proxy BQ logging instrumentation; 4 files, all LOGGING_ONLY
