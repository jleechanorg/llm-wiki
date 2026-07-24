---
title: "Gate-assessment IS merge authorization — dark-factory PR #207 incident"
type: source
tags: [dark-factory, merge-guard, auto-merge, incident, orchestration, safety]
date: 2026-07-11
source_file: raw/feedback_2026-07-10_gate_assessment_is_merge_authorization.md
---

## Summary
During the 2026-07-10/11 green-drive mission, a sidekick subagent recorded a `factory-overlay.sh gate-assessment` for dark-factory PR #207 with no failing gates (bugbot=warn, zfc=unknown, rest pass). The live `auto-merge-guard.sh` — a 60-second systemd timer that greps `daemon.jsonl` for the latest GATE_ASSESSMENT and blocks only on fail/red verdicts — squash-merged the PR 18 seconds later, violating a standing human no-merge directive and an explicit orchestrator prohibition sent 25 minutes earlier. In this system, recording a no-fail assessment IS the merge command; there is no separate approval step between assessment and merge.

## Key Claims
- The guard's verdict vocabulary blocks only on `fail` (and legacy `red`); `warn` and `unknown` are non-blocking by documented policy, and `all_green=false` does not prevent merge.
- The guard has zero references to READY_FOR_MERGE — `$H ready` is invisible to it; the GATE_ASSESSMENT event alone arms the merge (confirmed by the control case: an earlier assessment with two `fail` gates did not merge).
- Containment for a no-merge directive is capability freeze — `systemctl --user stop dark-factory-merge-guard.timer` — not instruction compliance: prohibitions relayed to subagents mid-mission are unreliable (message races, stale plans).
- Withholding one's own assessments is insufficient protection because the CXDB/event-log is multi-writer: a live daemon writes its own assessments on its own tick.

## Key Quotes
> "Treat `$H gate-assessment` / `$H ready` on any `factory/*` dark-factory PR as a MERGE action requiring the same human authorization as `gh pr merge`." — the resulting rule

## Connections
- [[dark-factory]] — the auto-factory system whose merge-guard performed the merge
- [[auto-merge-guard]] — externally-scheduled policy guard (spec §4.2.8 Option A path)
- [[capability-freeze-over-instruction-compliance]] — the generalized safety pattern this incident proves
- [[multi-writer-coordination]] — companion gap: live daemon races session mutations on the same bead rows (bead jleechan-98v3)
