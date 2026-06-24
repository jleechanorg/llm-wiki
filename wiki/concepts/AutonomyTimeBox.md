---
title: "Autonomy Time Box"
type: concept
tags: [harness, autonomy, time-box, regression]
date: 2026-06-24
---

## Definition
An **autonomy time-box** is a wall-clock cap on how long a single autonomous
agent session, AO worker, or `/converge`/`/eloop`/`/goal_harness`/`/auton`/`/f`/`/goal`
invocation may run before requiring explicit human re-approval. The canonical
cap is **3 hours (10,800 seconds)** without an `.approved_until` companion
file. Past the cap, the agent MUST pause, post a status snapshot to Slack,
and require the literal phrase `CONTINUE N HORUS` (or `EXTEND TO N HORUS`) in
the live user message to continue.

## Why it matters
LLM agent sessions can run for many hours if not capped. Long runs:
- **Mask stuck loops** — a worker that has been looping on the same failure for 4 hours looks identical to one that's 4 minutes into a long task.
- **Burn token budget** — context fills, costs climb, and the agent loses calibration as it processes more output.
- **Burn Slack quota** — babysit status updates and completion notifications drain per-channel limits.
- **Mask real alerts** — when a true CI/cron failure occurs during an autonomous run, the agent may ignore it because it's "busy" with its long-running flow.

## Detection pattern
- Autonomous flow invoked → no `started_at` marker written → no cap applies → run can extend indefinitely.
- Started_at marker present but `.approved_until` not updated → run blocks at 3-hour mark (good).
- Started_at marker + `.approved_until` set, but no human actually typed the phrase → bypass file written by automation (bad).

## Enforcement layers
1. **Skill-level** — `/babysit --max-min 180` already enforces for one-shot watches.
2. **CLAUDE.md policy** — single canonical rule in `~/.claude/CLAUDE.md` "Autonomy time-box."
3. **Helper script** — `~/.claude/scripts/check_autonomy_time_box.sh` reads `~/.hermes/runtime/*.started_at` + `tmux list-sessions` for `ao-*` workers; returns rc=1 if any entry > 10,800 s.
4. **Documented exemption** — literal phrase `CONTINUE N HORUS` / `EXTEND TO N HORUS` in the most recent user message writes `approved_until = now + N*3600`. Paraphrases NOT accepted.

## Bypass pattern (LiteralApprovalPhrase)
The bypass phrase is intentionally non-paraphraseable. Paraphrases like
"keep going", "ship it", "yes" are NOT authorization. The literal phrase
`CONTINUE N HORUS` (or `EXTEND TO N HORUS`) must appear in the most recent
user message. N is the number of hours to extend by. The companion
`.approved_until` file makes extensions visible + reversible.

## Canonical incident
2026-06-24: User asked "5 horus is way too long wtf is going on?" (history.jsonl:1780704230249). `/babysit --max-min 180` already enforced a cap for one-shot watches but other flows had no shared cap. New policy + helper close the gap.

## Connections
- [[AOSpawnSafety]] — sibling worker-COUNT cap (20 hard limit); this is worker-TIME cap
- [[BabysitMaxMin]] — existing one-shot watch cap (180 min default)
- [[LiteralApprovalPhrase]] — bypass mechanism
- [[SkillStaleness]] — same root cause class: trust the harness structure, verify the mechanism
- [[SlackStatusSnapshot]] — post-pause notification channel
