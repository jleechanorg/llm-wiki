---
name: umbrella-pattern-empty-default
description: Hardcoded defaults in Slack channel resolvers drift toward the wrong channel. The umbrella pattern (PR #615) is "empty default + plist-as-source-of-truth" for exactly this reason.
metadata:
  node_type: memory
  type: feedback
  bead: jleechan-5mkt
  originSessionId: 0045c60d-afe5-4e07-84a6-54dde9b7d8b0
---

## Rule

When consolidating channel resolution across multiple Slack-posting scripts (or any config-driven branching), the umbrella pattern is:

```
HERMES_OPS_SLACK_CHANNEL="${HERMES_OPS_SLACK_CHANNEL:-}"
CHANNEL="${PER_JOB_CHANNEL:-${HERMES_OPS_SLACK_CHANNEL:-}}"
```

If both are empty, the post fails soft (`post_slack` logs and returns 1) — never silently bleeds to a hardcoded channel.

**Never** write a resolver chain that ends in a hardcoded channel ID as a "sensible default." The hardcoded value is the bug.

## Why

PR #681 in `jleechanorg/agent-orchestrator` (commit `d8940175b`, 2026-06-13) was intended to consolidate `HERMES_OPS_SLACK_CHANNEL` across `ai.agento.health-guardian` and `hermes-watchdog`. The author:

1. Hardcoded `HERMES_OPS_SLACK_CHANNEL="${HERMES_OPS_SLACK_CHANNEL:-C0AJ3SD5C79}"` — the *wrong* channel (design, not ops) for the "ops" variable.
2. Added a back-ass guard: `if [ "${HEALTH_GUARDIAN_ALERT_CHANNEL:-}" = "C09GRLXF9GR" ]; then HEALTH_GUARDIAN_ALERT_CHANNEL=""` — actively UNSETS the correct ops channel.
3. Removed the plist template env entry, so new installs had no per-job channel plumbing.

Result: live alerts from `ai.agento.health-guardian` bled from `#all-jleechan-ai` (C09GRLXF9GR, ops) into `C0AJ3SD5C79` (design) for ~13 hours, and the regression test (added in PR #681 itself) **codified the bug as correct behavior** ("defaults to C0AJ3SD5C79 when no env vars are set").

This is the same class of bug PR #615 (jleechanclaw `lib/slack_thread_lib.sh`) was meant to eliminate. The umbrella pattern survives because every level of the resolver chain is empty by default — no value can drift toward the wrong channel.

## Anti-patterns to reject in code review

- `CHANNEL="${FOO:-C0WRONGCHAN}"` — hardcoded fallback, the original sin
- `if [ "${FOO:-}" = "C0RIGHTCHAN" ]; then FOO=""; fi` — back-ass guard that strips the correct value
- Tests that assert "X is the resolved channel when env is unset" without checking X is *the correct channel*
- Plist templates that drop the per-job env var (forces fallback to the cross-job chain)

## How to apply

- When reviewing a Slack-channel resolver chain: every level's default must be empty.
- The plist (or caller) is the source of truth. The script is a passive resolver.
- The resolver MUST be a simple chain (per-job env → cross-job env → empty) — no conditional logic, no back-ass guards, no "smart" precedence rules.
- The post function must refuse to post when CHANNEL is empty (fail-soft path), so a missing env can never silently post to a wrong channel.
- Tests must include the regression case: "with the live plist pattern, the channel is X" — not just "with these specific env overrides, the channel is X." The PR #681 test missed the live plist pattern entirely.

## References

- PR #615: jleechanorg/jleechanclaw `lib/slack_thread_lib.sh` (the umbrella)
- PR #681: jleechanorg/agent-orchestrator `d8940175b` (the regression)
- PR #687: jleechanorg/agent-orchestrator `47b9c60fd` (the fix)
- Bead: jleechan-5mkt
- 24h Slack audit 2026-06-10 surfaced 3 active misroutes; PR #615 fixed the 5 cron scripts; PR #616 (jleechanclaw) fixed 4 more; PR #687 fixes the agent-orchestrator watchdogs.
