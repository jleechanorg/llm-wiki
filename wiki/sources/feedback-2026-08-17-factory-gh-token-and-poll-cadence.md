---
title: "Linux auto-factory rate-limit misdiagnosis (2026-08-17)"
type: source
tags: [feedback, factory, gh-rate-limit, jeff-ubuntu, dark-factory, poll-cadence, evidence-gate]
date: 2026-08-17
source_file: feedback_2026-08-17_factory_gh_token_and_poll_cadence.md
---

## Summary
Linux auto-factory daemon on jeff-ubuntu was hitting GitHub's 5000/hr core + 5000/hr GraphQL rate-limit budget and emitting HTTP 403 on `gh pr view` probes — surfacing as `INTAKE → SKIPPED_INELIGIBLE` for ~70 PRs including `jleechanorg/worldarchitect.ai#8958`. The fix was two-part: slow the polls (`fast_tick_secs 10→60`, `slow_tick_secs 30→300`) AND add an explicit `GH_TOKEN` systemd drop-in for `gh` CLI auth. Same-GitHub-user tokens share one rate-limit pool, so a fresh PAT for the same account does NOT buy a separate budget.

## Key Claims
- HTTP 403 with `user ID X rate limit exceeded` from `gh` looks indistinguishable from a bad token — always check `gh api rate_limit` BEFORE chasing auth.
- A fresh PAT for the same GitHub user refills the 5000/hr budget but exhausts again under the same load; only a different account or a GitHub App installation gets a separate pool.
- `fast_tick_secs=10` + ~70 PRs + `max_workers=80` worker-side `gh` calls projects to ~25,200/hr, blowing past the 5000/hr budget in ~10 minutes.
- The pre-existing conformance test `test_conformance_validate_walker_skips_underscore_dot_libraries` was failing on `origin/main` itself because `pipelines/slim/ready.dot` claimed `level5="true"` without `gate_skeptic` + `parallel_reviewer`. PR #650 made the same one-line fix; both PRs merged cleanly.

## Key Quotes
> "Rate-limit errors look like auth errors. When `gh pr view` returns HTTP 403 with `user ID X rate limit exceeded`, the symptom is indistinguishable from a bad token."

> "Two-part fix is the right shape: (a) slow the polls so the load fits the budget; (b) make `gh` auth deterministic via an explicit systemd drop-in so failures stop depending on a keyring entry that can silently break."

> "The slow-CI operator directive (2026-08-16) is the escape hatch: when self-hosted runners are queued >10 minutes, local results SATISFY `/green` Gate 1."

## Connections
- [[Evidence Gate dual-signal contract]] — Signal A (trusted-bot `/er PASS`) and Signal B (`**Evidence**: <gist-url>` marker in PR body). The new daemon PR wired Signal B because the user authorized the merge without running `/er`.
- [[jeff-ubuntu]] — sole Linux auto-factory host. This whole incident is jeff-ubuntu-specific.
- [[Dark Factory]] — the runner project. Config change to `config/daemon.toml` and new `daemon/systemd/drop-in/` tracked directory.
- [[Slow-CI Operator Directive 2026-08-16]] — escape hatch that let this PR merge despite self-hosted runners being queued.
- [[Bead rev-y1v6g]] — bug P1 bead filed for this fix.
- [[PR #651]] — squashed to `23edb52fff269ef96c7b3080ab565f518d760197` on origin/main.
- [[PR #8958]] — `jleechanorg/worldarchitect.ai` PR that was unblocked (dice-roll maxLength bounds).
- [[PR #650]] — sibling PR that made the same one-line fix to the same file as this one; both merged cleanly.