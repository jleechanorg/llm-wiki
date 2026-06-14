---
name: slack-misroute-consolidation-pr-615
description: "Why the 4 prior surgical slack-misroute fixes (#603,"
metadata: 
  node_type: memory
  bead: jleechan-owka
  type: project
  originSessionId: 0045c60d-afe5-4e07-84a6-54dde9b7d8b0
---

# Slack misroute: surgical fixes don't scale, consolidate through a shared lib

## The pattern (2026-06-12 → 2026-06-13)

PRs closed in order against the "wrong thread" problem:
- [#603](https://github.com/jleechanorg/jleechanclaw/pull/603) `ao-progress-reporter.sh` — retry + state-file persistence in `resolve_thread_ts`
- [#604](https://github.com/jleechanorg/jleechanclaw/pull/604) `human_channel_bridge.py` — persist `worker_threads` to disk for crash recovery
- [#606](https://github.com/jleechanorg/jleechanclaw/pull/606) `dropped-thread-followup.sh` — route escalations to daily persisted thread
- [#614](https://github.com/jleechanorg/jleechanclaw/pull/614) `hermes-watchdog.sh` — added plist template + 1 line (parity with upstream PR #681)

Each one shipped green and merged. Each one treated the **symptom at the call site** (1 file). None of them addressed the **class** of bug:
- No shared library wrapping `chat.postMessage`
- No dedupe (so repeated warnings posted 4-5 times within 60s)
- No thread anchor (so cronjob sub-results always went to channel root)
- 5+ other cron scripts (`stability-report.sh`, `spend-alert-daily.sh`, `gh-actions-cost-monitor.sh`, `github-intake.sh`, ...) still calling `curl chat.postMessage` directly with no `thread_ts`

24h Slack audit found 3 misroute patterns the merged PRs didn't cover. Tracked as follow-up beads:
- `jleechan-ry3y` — cronjob sub-results post as top-level roots
- `jleechan-a5x0` — duplicate warnings within 60s
- `jleechan-fu5b` — watchdog `HERMES_OPS_SLACK_CHANNEL=C0AJ3SD5C79` (design channel!) bled ops into design

## The fix: PR #615 — consolidate through one shared lib

[PR #615](https://github.com/jleechanorg/jleechanclaw/pull/615) replaces 5 inline `curl`/`send_slack_alert` patterns with one `slack_post` call to `lib/slack_thread_lib.sh`:
- **Daily thread anchor** per job (`var/slack/<job>/daily-thread.ts`, resets on new UTC day)
- **Dedupe** per channel (TSV keyed on `hash(text) → last_ts`, default 60s window)
- **Channel resolution**: `HERMES_OPS_SLACK_CHANNEL` env → caller default → fail-soft skip
- `--force` bypass dedupe, `--no-thread` skip anchor
- 14 RED-GREEN tests in `tests/test_slack_thread_lib.sh`

Also fixed the watchdog wrong-default `C0AJ3SD5C79` to empty so the resolver routes to the launchd plist's `HERMES_OPS_SLACK_CHANNEL` (the actual ops channel per bead jleechan-fu5b).

## Why surgical fixes didn't hold — root cause

Each merged PR was *internally* green (CI passed, CR APPROVED, skeptic PASS) because it was a self-contained single-file change. But the *class* of bug was unaddressed: every cron script that called `chat.postMessage` was a future re-incarnation of the same problem. A new script written next week (e.g. `spend-alert-hourly.sh`) would re-introduce top-level rooting + duplicate warnings because there's no shared infrastructure to use.

**Lesson:** when the same fix pattern is needed in 3+ places, stop patching the call sites and add the missing abstraction. The 4-PR "fix parade" between 2026-06-12 and 2026-06-13 was the symptom; the root cause was "no shared slack_post library." Brownfield rule: prefer a single replace-everywhere PR over N surgical add-on PRs even if the brownfield PR has higher net LOC, as long as it deletes more than it adds at the call sites.

## Verification
- 14/14 tests pass in `tests/test_slack_thread_lib.sh`
- 23/23 `test_ao_progress_reporter_skip_unchanged.sh` (no regression)
- Direct lib smoke test for `spend-alert-daily` and `hermes-watchdog` patterns: both post OK with mocked curl

## References
- PR: https://github.com/jleechanorg/jleechanclaw/pull/615
- Branch: `fix/slack-cronjob-dedupe-thread-anchor`
- HEAD SHA: `a252489f64135af7df70ef0d494846a5912ff7dd`
- Beads: `jleechan-ry3y`, `jleechan-a5x0`, `jleechan-fu5b`, `jleechan-owka`
- Skill: `~/.hermes/skills/devops/slack-thread-routing-investigation/SKILL.md` (runtime tool-surface gap; distinct from cron-side fix)
- Plan: `~/.claude/plans/radiant-churning-tulip.md`
