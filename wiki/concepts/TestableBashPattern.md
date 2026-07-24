---
title: "Testable Bash Pattern"
type: concept
tags: [bash-testing, hand-rolled, tdd, launchd]
date: 2026-06-23
---

# Testable Bash Pattern

The pattern for making bash scripts in launchd/cron/automation paths
testable without bats (which is not installed in this environment).

## Recipe

1. **Extract pure helpers** into `scripts/lib/<name>-helpers.sh`:
   - regex escapes (e.g. `escape_ere`)
   - pattern builders (e.g. `build_project_alt`, `orchestrator_pgrep_pattern`)
   - predicates (e.g. `should_clean_stale_running_json`)
   - path resolution (e.g. `command_matches_ao_binary`)

2. **Source the lib** in both the main script (`source "$SCRIPT_DIR/lib/<name>-helpers.sh"`)
   and the test (`source "$HELPERS"`).

3. **Write the test** with sections:
   - pure-function assertions (`assert_eq`)
   - pattern-shape assertions (`assert_match` / `assert_no_match` against fixture cmdlines)
   - source-level regression guards (`grep -qE` against the main script to lock in
     CLI flag pass-throughs)

4. **Capture RED→GREEN** in the PR body:
   - Temporarily revert one fix
   - Re-run the test, capture the failing output
   - Restore the fix, re-run, capture all-pass output
   - Embed both in the PR body as evidence

## Framework template (matches `test-launchd-env.sh` style)

```bash
#!/usr/bin/env bash
set -euo pipefail
FAILED=0
PASSED=0

source "$SCRIPT_DIR/lib/<name>-helpers.sh"

ok()    { echo "  PASS: $1"; PASSED=$((PASSED + 1)); }
fail()  { echo "  FAIL: $1"; FAILED=$((FAILED + 1)); }
assert_eq() { ... }   # check label expected actual
assert_match() { ... }   # check pattern subject
assert_no_match() { ... }

# ...sections...

if [ "$FAILED" -gt 0 ]; then exit 1; fi
echo "All checks passed."
```

## Example
[[PR718BashTestSuite]] — 33-check harness, 6 sections, applied to the
single-orchestrator migration in `scripts/ao-health.sh`.

## See also
- [[PR717SkepticVerdict]]
- [[IntegrateHardStopPattern]]
