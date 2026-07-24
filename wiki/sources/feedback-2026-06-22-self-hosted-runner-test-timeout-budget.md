---
title: "Self-hosted runner test-timeout budget: 90s Flask + 60s Playwright page.goto"
type: source
tags: [feedback, worldarchitect, ci, testing, timeout-budget, self-hosted-runner, pr-7815]
date: 2026-06-22
source_file: raw/feedback_2026-06-22_self_hosted_runner_test_timeout_budget.md
---

## Summary
Default 20s budgets in `testing_ui/**` mobile auth same-origin test were too tight for memory-pressured self-hosted GitHub Actions runners. Two distinct slow phases were racing: gunicorn FastEmbed classifier `BAAI/bge-small-en-v1.5` model load (~20s) and auth.js fetch during `domcontentloaded` (10s+). The fix in PR [#7815](https://github.com/jleechanorg/worldarchitect.ai/pull/7815) bumps the budgets to 90s Flask-start + 60s page.goto. The substantive PASS/FAIL signal is in the test cases, not in startup/load time.

## Key Claims
- For any new `testing_ui/**` test that boots Flask via gunicorn and exercises the live server, default to **90s Flask-start** + **60s page.goto** budgets
- Memory-pressured self-hosted runners regularly exceed the default 20s budgets on the first boot because gunicorn workers must load FastEmbed models
- A slow first worker killed by gunicorn master forces a fresh worker to redo the full boot — the 20s budget races the worker's full lifecycle, not just the first response
- Use `wait_until="domcontentloaded"` (not `"load"`) for SPA smoke tests — `domcontentloaded` is the right event for auth.js + first-paint
- The "real fix" is reducing runner memory pressure (lower `containerConcurrency` + raise `minScale` in Cloud Run), not tightening the test budgets. That's an infra matter outside this PR's scope.

## Key Quotes
> "The substantive PASS/FAIL signal is in the test cases, not the startup/load time, so we give the worker plenty of headroom instead of flaking." — `testing_ui/mobile_auth_same_origin/test_auth_same_origin.py:91`

## Connections
- [[SelfHostedRunnerInfraFlakeVsRealFailure]] — same family of "is this a real bug or a runner flake?" diagnostics
- [[GATE6bDescriptionGate]] — companion learning from same PR: GATE-6 evidence URL requirement + `gh pr edit --body "$()"` body-wipe bug
- [PR #7815](https://github.com/jleechanorg/worldarchitect.ai/pull/7815) (merged 2026-06-23T02:21:20Z, commit `e08abf3215`) — fix landed
- [Run 27991914172 / job 82845940066](https://github.com/jleechanorg/worldarchitect.ai/actions/runs/27991914172/job/82845940066) — pre-fix Flask startup FAIL on PR [#7810](https://github.com/jleechanorg/worldarchitect.ai/pull/7810)
- [Run 27992750133](https://github.com/jleechanorg/worldarchitect.ai/actions/runs/27992750133) — mid-fix page.goto FAIL on PR #7815
- [Run 27992975784 / job 82849096053](https://github.com/jleechanorg/worldarchitect.ai/actions/runs/27992975784/job/82849096053) — post-fix PASS (1m30s, Layer A 4/4 + Layer B 2/2)
- Code: `testing_ui/mobile_auth_same_origin/test_auth_same_origin.py:84-92` (start_flask 90s budget + FastEmbed comment) and `testing_ui/mobile_auth_same_origin/test_auth_same_origin.py:283-289` (page.goto 60s budget + auth.js-fetch comment)
- Bead: rev-mfcp4
