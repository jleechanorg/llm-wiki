---
title: "gh pr checks reports cancelled jobs as fail — PR #7720 drive-to-green triage"
type: source
tags: [ci, github-actions, gh-cli, green-gate, flake, worldarchitect, pr-7720, mypy, deploy-preview]
date: 2026-06-20
source_file: ~/.claude/projects/-Users-jleechan-worldarchitect.ai/memory/feedback_2026-06-20_gh-pr-checks-cancelled-shows-fail.md
---

## Summary

While driving PR #7720 (jleechanorg/worldarchitect.ai — iOS WebKit IndexedDB
persistence deadlock fix, merge commit `21cf81df85`) to green, two CI checks went
red. Both were CI artifacts, not code defects: mypy's real conclusion was
`cancelled` (lifecycle/concurrency), and `deploy-preview` was a rotating Cloud Run
pool flake. Both were fixed by `gh run rerun --failed` with zero code changes. The
session establishes a CI-red triage discipline: read the actual job conclusion
before debugging code.

## Key Claims

- `gh pr checks <PR>` collapses a job whose real conclusion is `cancelled` into
  the "fail" column. Confirm with `gh run view <run_id> --json status,conclusion,jobs`
  before treating it as a defect. `cancelled` ≠ `failure`.
- A `deploy-preview` (rotating pool) failure at the "Build and Deploy" step *after*
  a successful "Assign server from pool", with logs already expired (`BlobNotFound`
  from the job logs API), is the signature of an infra/pool flake → `gh run rerun --failed`.
- `queued` gates (Green Gate, Design Doc Gate) usually mean runner SATURATION
  (10/10 `online busy=true`), not a zero-runner outage. Distinguish via
  `gh api orgs/<org>/actions/runners`.
- Final green state: 27 passed / 0 failed, `MERGEABLE / CLEAN`, 0 unresolved
  review threads.
- The MERGED `auth.js` uses `Object.defineProperty(window,'indexedDB',{configurable: true,...})`
  (line 41) — reverted from `configurable: false` to align with proven/deployed
  HTTP-capture evidence. The earlier-ingested wiki page describes `false`; reconcile.

## Key Quotes

> mypy showed `fail` in `gh pr checks` but `gh run view --json` reported
> `concl=cancelled` — prior HEADs had passed mypy, confirming no type error.

## Triage pattern (reusable)

1. Read the actual per-job `conclusion` via `gh run view <id> --json conclusion,jobs`.
2. `cancelled` or post-infra-step flake with expired logs → `gh run rerun <id> --failed`.
3. Only debug code if the rerun fails again with fresh, readable logs.
4. `queued` + busy runners = saturation (wait); zero online runners = real outage.

## Connections

- [[PR7720]] — the PR driven to green
- [[WorldArchitectAI]] — host repo
- [[Self-Hosted-Runner-Infra-Flake-vs-Real-Failure]] — parent concept (updated with this lesson)
- [[GreenGateWorkflow]] — aggregate gate that keys off Skeptic verdict at HEAD
- [[pr7720-ios-webkit-indexeddb-persistence-deadlock]] — the fix this PR ships (configurable reconciliation noted)
