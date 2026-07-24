---
title: "Testable bash: extract pure helpers + hand-rolled test harness (2026-06-23)"
type: source
tags: [bash-testing, launchd-coverage, tdd]
date: 2026-06-23
source_file: feedback_2026-06-23_testable_bash_extracted_helpers.md
---

## Summary
Bash scripts in launchd-driven / 5-min-tick paths must have automated test coverage. bats is not installed; use a hand-rolled framework with extracted pure helpers sourced by both the main script and the test. Follow the `test-launchd-env.sh` pattern (`set -euo pipefail` + `FAILED=0` + exit codes). Source-grep regression guards lock in CLI-flag pass-throughs.

## Key Claims
- bats is not installed in this environment; the test framework must be hand-rolled
- Pure helpers (regex, pattern, predicate) belong in `scripts/lib/<name>-helpers.sh`, sourced from BOTH the main script and the test
- Source-grep checks like `grep -qE 'no-dashboard.*no-open' main.sh` lock in CLI flag pass-throughs and prevent silent refactor regressions
- TDD red→green must be captured in the PR body as evidence

## Key Quotes
> "When a bash script in a launchd/automation path (5-min tick, watchdog, etc.) has logic that should be unit-testable — regex construction, pattern matching, input validation, file detection — extract those functions into a sourced library and write a hand-rolled bash test harness."

## Connections
- [[PR718BashTestSuite]] — concrete application in PR #718 (33-check harness)
- [[PR717SkepticVerdict]] — predecessor finding that flagged missing bash tests as Gate 7 FAIL
- [[IntegrateHardStopPattern]] — integrate.sh also auto-stops test servers
