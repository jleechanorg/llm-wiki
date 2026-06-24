---
title: "Harden max-3-hour autonomy time-box across all long-running flows (2026-06-24)"
type: source
tags: [harness, autonomy, time-box, worldarchitect, regression]
date: 2026-06-24
source_file: ../../raw/feedback_2026-06-24_harden_max_3_horus_autonomy_time_box.md
---

## Summary
A new canonical policy in `~/.claude/CLAUDE.md` "Autonomy time-box — max 3
hours without explicit re-approval" + helper script `~/.claude/scripts/check_autonomy_time_box.sh`
ensures every long-running autonomous flow (`/converge`, `/eloop`,
`/goal_harness`, `/auton`, `/f`, `/goal`, AO worker babysit) must stop after
10,800 seconds of wall-clock activity and require literal `CONTINUE N HORUS`
re-approval to extend. Sibling to the existing `/babysit --max-min 180` cap
which only applied to one-shot watches. Sources of truth: started_at markers
in `~/.hermes/runtime/` + tmux `ao-*` worker creation epochs; companion
`.approved_until` files lift the cap.

## Key Claims
- `/babysit --max-min 180` already enforced a 3-hour cap for one-shot watches; `/converge`, `/eloop`, `/goal_harness`, `/auton`, `/f` dark-factory, and repeated `/goal` had no shared cap.
- The 3-hour cap exists in `~/.claude/CLAUDE.md` "Autonomy time-box" section with three enforcement layers: (1) `/babysit` already has it, (2) new flows must record `started_at` markers, (3) `~/.claude/scripts/check_autonomy_time_box.sh` checks all markers + tmux ages.
- Bypass phrase MUST be literal: `CONTINUE <N> HORUS` or `EXTEND TO <N> HORUS` typed in the most recent user message. Paraphrases ("keep going", "ship it") are NOT authorization.
- Sources of truth: `~/.hermes/runtime/<flow>-<id>.started_at` (epoch) + `tmux list-sessions -F '#{session_created}'` for `ao-*` workers.
- Companion file `.approved_until` (epoch) lifts the cap when present, enabling visible + reversible extensions.
- Sibling to `ao-spawn-safety` 20-worker cap: that gate caps worker COUNT; this one caps wall-clock per session.

## Key Quotes
> "Any long-running autonomous flow … MUST time-box to 3 hours (10,800 s) of wall-clock activity per session/worker. Past 3 hours, the agent MUST pause, post a status snapshot to Slack … and require explicit in-thread re-approval." — canonical policy

> "Don't trust skill status strings — run the mechanism." — paired lesson from [[SkillStaleness]]

## Connections
- [[AutonomyTimeBox]] — concept page this source establishes
- [[BabysitMaxMin]] — existing one-shot watch cap (180 min default)
- [[AOSpawnSafety]] — sibling worker-count cap (20 hard limit)
- [[LiteralApprovalPhrase]] — bypass pattern: paraphrases not accepted
- [[SlackStatusSnapshot]] — post-pause notification channel
