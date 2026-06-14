---
title: "Slack misroute: surgical fixes don't scale (PR #615, 2026-06-13)"
type: source
tags: [project, slack, misroute, dedupe, thread-anchor, consolidation, refactor, root-cause, brownfield]
date: 2026-06-13
source_file: raw/project_2026-06-13_slack_misroute_root_cause_consolidation.md
---

## Summary
Four surgical PRs (#603, #604, #606, #614) each fixed a "wrong thread" / "duplicate warnings" symptom at one call site between 2026-06-12 and 2026-06-13. All four shipped green, all four were merged, and all four left the **class** of bug unaddressed — no shared Slack post library, no dedupe, no daily thread anchor. A 24h Slack audit found 3 additional misroute patterns the merged PRs didn't cover. The fix in PR #615 replaces 5 inline `curl`/`send_slack_alert` patterns with one `slack_post` call into `lib/slack_thread_lib.sh` (daily thread anchor, 60s dedupe, env-based channel resolution, `--force` / `--no-thread` flags).

## Key Claims
- **Brownfield consolidation rule**: when the same fix pattern is needed in 3+ places, stop patching call sites and add the missing abstraction. A single replace-everywhere PR is preferred over N surgical add-ons even if it has higher net LOC, **as long as it deletes more than it adds at the call sites**.
- The 4-PR "fix parade" was the **symptom**; the root cause was "no shared `slack_post` library" — every new cron script (`spend-alert-hourly.sh` etc.) would re-introduce top-level rooting and duplicate warnings.
- Each surgical PR was internally green (CI, CR APPROVED, skeptic PASS) because it was a self-contained single-file change — green is necessary but not sufficient when the bug is a class, not an instance.
- PR #615 features: daily thread anchor per job (`var/slack/<job>/daily-thread.ts`, resets on new UTC day), per-channel dedupe (TSV keyed on `hash(text) → last_ts`, 60s window), channel resolution order = `HERMES_OPS_SLACK_CHANNEL` env → caller default → fail-soft skip.
- Also fixed: watchdog `HERMES_OPS_SLACK_CHANNEL=C0AJ3SD5C79` (design channel!) bled ops into design; cleared to empty so the launchd plist value takes effect.

## Verification
- 14/14 tests in `tests/test_slack_thread_lib.sh`
- 23/23 in `test_ao_progress_reporter_skip_unchanged.sh` (no regression)
- Direct lib smoke test for `spend-alert-daily` and `hermes-watchdog` patterns — both post OK with mocked curl

## Open Follow-ups (beads)
- `jleechan-ry3y` — cronjob sub-results post as top-level roots
- `jleechan-a5x0` — duplicate warnings within 60s
- `jleechan-fu5b` — watchdog wrong-default channel bleed
- `jleechan-owka` — this consolidation work

## Key Quotes
> when the same fix pattern is needed in 3+ places, stop patching the call sites and add the missing abstraction. The 4-PR "fix parade" between 2026-06-12 and 2026-06-13 was the symptom; the root cause was "no shared slack_post library."

## Connections
- [[Slack]] — Slack dispatch infrastructure
- [[RootCauseFirst]] — surgical fix parade as anti-pattern; root cause = missing abstraction
- [[BrownfieldRefactor]] — replace-everywhere PR with positive net-deletion-at-callsites
- [[SurgicalFixAntiPattern]] — when 3+ places need the same patch, consolidate
- [[SlackThreadRouting]] — daily thread anchor + dedupe pattern
- [[PRQuantityControl]] — 4 surgical PRs as quantity anti-pattern; consolidate to 1
- [[slack-wrong-thread-root-cause]] — the underlying channel-resolution bug
