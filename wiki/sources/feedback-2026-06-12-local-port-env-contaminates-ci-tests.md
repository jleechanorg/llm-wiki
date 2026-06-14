---
title: "Local PORT env var contaminates CI tests (2026-06-12)"
type: source
tags: [ci, environment, testing, dev-server, env-leak]
date: 2026-06-12
source_file: /Users/jleechan/.claude/projects/-Users-jleechan-projects-worldarchitect-ai/memory/feedback_2026-06-12_local_port_env_contaminates_ci_tests.md
---

## Summary
A local Flask dev server bound to a non-default `PORT=9130` leaks into the test process, causing `test_gunicorn_config.py::test_bind_address_is_cloud_run_compatible` to assert against the wrong bind address (`0.0.0.0:9130` instead of `0.0.0.0:8080`). The failure looks real but is purely an env-contamination artifact. Run tests with `PORT=8080` (or unset) to match CI self-hosted runner defaults.

## Key Claims
- `PORT` env var from a running local dev server leaks into the test process via inherited env, producing false failures in `test_gunicorn_config.py::TestGunicornConfiguration::test_bind_address_is_cloud_run_compatible`.
- Self-hosted CI runner has `PORT=8080`; locally with a server bound to 9130, the test process sees `PORT=9130` and asserts against the wrong bind address.
- Two pre-existing test failures (`test_agent_architecture_end2end.py` god mode rewards_box guard, `test_shared_cache_probe.py` probe errors) are unrelated to PR #7439 and were confirmed untouched by `git diff origin/main..HEAD`.
- Discovery context: local CI verification before merge of PR #7439 (BQ forensic logging, merged 2026-06-12).

## Key Quotes
> "When a local dev server is running on port 9130, the `PORT=9130` env var leaks into the test process and the test fails: `AssertionError: '0.0.0.0:9130' != '0.0.0.0:8080'`" — pattern

> "Before reporting a local test failure, check if the test involves port/bind config and whether a dev server is running." — operational rule

## Connections
- [[WorktreeWorkflow]] — local dev workflow on a worktree, the contamination source
- [[GreenGate]] — local CI verification precedes the Green Gate decision
- [[SelfHostedRunners]] — CI runner config sets `PORT=8080` as the canonical test default
- [[EvidenceStandards]] — distinguishing real failure vs env-contamination artifact
- [[PR7439]] — driving PR (BQ forensic logging)
