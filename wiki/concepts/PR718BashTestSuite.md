---
title: "PR #718 Bash Test Suite"
type: concept
tags: [bash-testing, agent-orchestrator, pr-718]
date: 2026-06-23
---

# PR #718 Bash Test Suite

The 33-check hand-rolled bash test harness in `scripts/test-ao-health.sh` that
exercises the testable helpers extracted from `scripts/ao-health.sh` into
`scripts/lib/ao-health-helpers.sh`.

## Test sections (6)
1. `escape_ere` — 6 checks
2. `build_project_alt` — 4 checks
3. `pgrep pattern shape` — 11 checks
4. `should_clean_stale_running_json` — 4 checks
5. Source-level regression guards — 6 checks
6. `start-all.sh` shell-quoting regression — 2 checks

## How it runs
```bash
bash scripts/test-ao-health.sh
# Passed: 33
# Failed: 0
```

## Why it exists
PR #717's Skeptic verdict (Gate 7 FAIL) flagged that the bash-script
single-orchestrator migration in `scripts/ao-health.sh` had **zero automated
test coverage**. The followup PR #718 extracted pure helpers, wrote this
harness, and captured RED→GREEN as evidence in the PR body.

## See also
- [[TestableBashPattern]]
- [[PR717SkepticVerdict]]
