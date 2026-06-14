---
title: "umbrella pattern: empty default + plist-as-source-of-truth (2026-06-13)"
type: source
tags: [feedback, slack, channel-resolver, umbrella-pattern, plist, regression, code-review]
date: 2026-06-13
source_file: raw/feedback_2026-06-13_umbrella_pattern_empty_default.md
---

## Summary
Hardcoded defaults in Slack channel resolvers (or any config-driven branching) drift toward the wrong channel over time — the hardcoded fallback IS the bug. The umbrella pattern (PR #615 in jleechanclaw) makes every level of the resolver chain empty by default; the plist (or caller) is the sole source of truth, and the post function fails soft when CHANNEL is empty rather than bleeding to a hardcoded channel. PR #681 in agent-orchestrator (commit `d8940175b`) is the canonical regression: hardcoded `C0AJ3SD5C79` (design) in an "ops" variable + a back-ass guard that actively UNSETS the correct ops channel — bleeds `#all-jleechan-ai` (ops) into design for ~13h, and the regression test codified the bug as correct behavior.

## Key Claims
- **Never** write `CHANNEL="${FOO:-C0WRONGCHAN}"` — hardcoded fallback is the original sin.
- The umbrella pattern:
  ```bash
  HERMES_OPS_SLACK_CHANNEL="${HERMES_OPS_SLACK_CHANNEL:-}"
  CHANNEL="${PER_JOB_CHANNEL:-${HERMES_OPS_SLACK_CHANNEL:-}}"
  ```
  Every level empty by default. No value can drift toward the wrong channel.
- If both are empty, `post_slack` logs + returns 1 (fail-soft). It never silently bleeds to a hardcoded channel.
- The resolver MUST be a simple chain (per-job env → cross-job env → empty) — no conditional logic, no back-ass guards, no "smart" precedence rules.

## Anti-patterns to reject in code review
- `CHANNEL="${FOO:-C0WRONGCHAN}"` — hardcoded fallback
- `if [ "${FOO:-}" = "C0RIGHTCHAN" ]; then FOO=""; fi` — back-ass guard that strips the correct value
- Tests that assert "X is the resolved channel when env is unset" without checking X is the **correct** channel
- Plist templates that drop the per-job env var (forces fallback to the cross-job chain)

## Testing rule
Tests must include the regression case: **"with the live plist pattern, the channel is X"** — not just "with these specific env overrides, the channel is X." PR #681's test missed the live plist pattern entirely and codified the bleed as correct.

## Why
The 2026-06-10 24h Slack audit found 3 active misroutes. PR #615 fixed the 5 cron scripts in jleechanclaw; PR #616 fixed 4 more; PR #687 fixes the agent-orchestrator watchdogs. All three converged on the umbrella pattern.

## Key Quotes
> **Never** write a resolver chain that ends in a hardcoded channel ID as a "sensible default." The hardcoded value is the bug.

> The umbrella pattern survives because every level of the resolver chain is empty by default — no value can drift toward the wrong channel.

## Connections
- [[UmbrellaPattern]] — empty default + plist-as-source-of-truth resolver pattern
- [[Slack]] — Slack channel dispatch
- [[SlackThreadRouting]] — daily thread anchor + dedupe + umbrella channel resolution
- [[RootCauseFirst]] — PR #681's regression test codified the bug; tests must verify against the **correct** channel
- [[SurgicalFixAntiPattern]] — 4 surgical PRs led to the umbrella consolidation
- [[PR #615]] (jleechanclaw) — the umbrella implementation
- [[PR #687]] (agent-orchestrator) — the umbrella fix for watchdog misroutes
