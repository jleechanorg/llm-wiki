---
name: testable-bash-via-extracted-helpers
description: "bash scripts in launchd-driven / 5-min-tick paths must have automated test coverage; bats is rarely installed, use hand-rolled framework with extracted pure helpers"
metadata: 
  node_type: memory
  type: feedback
  bead: bd-2oll
  originSessionId: 4920971d-1790-4e87-8227-a17d7f18ef21
---

# Testable bash: extract pure helpers + hand-rolled test harness

## Rule

When a bash script in a launchd/automation path (5-min tick, watchdog, etc.) has logic that
should be unit-testable — regex construction, pattern matching, input validation, file
detection — extract those functions into a sourced library (`scripts/lib/<name>-helpers.sh`)
and write a hand-rolled bash test harness using `set -euo pipefail` + `FAILED=0` + exit codes.

**Do NOT** rely on `bats` — it is not installed in this environment. Follow the existing
`scripts/test-launchd-env.sh` pattern (assertion helpers `ok`/`fail`/`assert_eq`/`assert_match`/
`assert_no_match`, summary line at the end).

## Why

The Skeptic (PR #717 verdict) explicitly flagged that PR #717's `ao-health.sh` single-orchestrator
migration had **zero automated test coverage** for the bash-script behavioral goal — only
manual `bash scripts/ao-health.sh` output as evidence. Gate 7/8a failed on this. The fix is
not "add bats" (env constraint) — it is "extract pure logic + test it directly".

## Pattern (applied in PR #718)

1. **Extract pure helpers** into `scripts/lib/ao-health-helpers.sh`:
   - `escape_ere` — ERE escape
   - `build_project_alt` — projects → `a|b|c` alternation
   - `orchestrator_pgrep_pattern` / `orchestrator_orphan_sweep_pattern` — pattern builders
   - `should_clean_stale_running_json` — predicate
   - `command_matches_ao_binary` — was inline; moved to lib for testability
2. **Source the lib** in both the main script (`source "$SCRIPT_DIR/lib/<name>-helpers.sh"`)
   and the test (`source "$HELPERS"`). Add `set -euo pipefail` and use `source` not `bash`.
3. **Write the test** with sections: pure-function assertions, pattern-shape assertions
   (`assert_match` / `assert_no_match` against fixture cmdlines), and source-level regression
   guards (`grep -qE` against the main script to lock in `--no-dashboard --no-open` etc.).
4. **TDD red→green**: temporarily revert one fix, re-run the test, capture the failing
   output, restore. Embed the failing output in the PR body as RED evidence.

## Verification (PR #718)

- 33/33 checks pass in `scripts/test-ao-health.sh` across 6 sections
- RED captured: reverting `start-all.sh` to the vulnerable `python3 -c "...'$project'..."`
  form caused Section 6 to fail both assertions (verified before commit, output in PR body)
- Live smoke test: `bash scripts/ao-health.sh` after refactor reports
  `OK: orchestrator already running started=0 killed=0 failures=0`

## Why

- **ZFC exemption**: pure-function bash tests are deterministic; judgment-free;
  not an application-logic "if text.contains X then Y" pattern
- **TDD compliance**: bash test framework is a TDD surface just like vitest/jest
- **Regression guard**: the source-level grep checks (`grep -qE` against the main script)
  lock in CLI flag pass-throughs, so a refactor that drops `--no-open` will fail tests

## Files

- `scripts/lib/ao-health-helpers.sh` (new, +71 lines) — pure helpers
- `scripts/test-ao-health.sh` (new, +196 lines, 33 checks) — test harness
- `scripts/ao-health.sh` (-58/+34) — sources helpers, replaces inline logic
- `scripts/start-all.sh` (+10/-2) — shell-quoting fix (separate learning)

## References

- PR [#718](https://github.com/jleechanorg/agent-orchestrator/pull/718) merged as `5ebd4cc2`
- Predecessor PR [#717](https://github.com/jleechanorg/agent-orchestrator/pull/717) — merged
  with `lifecycle-worker` bash migration but **no** bash tests; Skeptic Gate 7 failed on this
- bd-#667 — original health-guardian watchdog chain issue
- Related: `feedback_2026-06-05_evidence_gate_claim_floor_override.md` (claim class selection)
