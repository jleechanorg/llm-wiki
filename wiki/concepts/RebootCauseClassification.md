---
title: "Reboot Cause Classification"
type: concept
tags: [ops, crash-investigation, linux, triage]
date: 2026-07-07
---

# Reboot Cause Classification

A Linux reboot has exactly one of four causes, and each leaves a distinct forensic signature. Automation (and agents) that treat "uptime < elapsed" as "crash" produce false verdicts — on 2026-07-07 this misclassified two watchdog(8) load shutdowns as kernel crashes and auto-failed a soak that had zero panics in four days.

## The classification ladder (check in order)

1. **Panic** — new files under `/var/lib/systemd/pstore/` (world-readable; dir-name epoch = crash time). Authoritative; overrides everything.
2. **Watchdog shutdown** — `journalctl -b <idx> -t watchdog | grep -E "error 253|load average too high"`. Query the indexed syslog identifier, NOT a journal tail: teardown spam pushes the marker out of any fixed-size tail.
3. **Clean shutdown** — PID-1/journald markers only in the boot's final lines: `systemd-shutdown[`, `Journal stopped`, `systemd[1]: Reached target Shutdown`, `systemd-reboot.service`. A **user-session** manager reaching shutdown.target (`systemd[NNNN]`) does NOT count — sessions die for many reasons.
4. **Silent stop** — none of the above: journal cuts mid-stream. Suspect hard reset, power loss, or an uncaptured panic. Treat as a real failure until explained (e.g. by a human confirming a manual reset).

## Verdict semantics for stability tests

- Panic or silent stop → FAILED.
- Watchdog/clean reboot → INTERRUPTED: the soak clock is invalid but the config was **not falsified**; restart the soak, don't record a crash.

## Implementation

`~/.local/bin/soakctl` (`classify_dead_boots()`, 2026-07-07, bead bd-9ac); staged copy in `user_scope/scripts/soakctl`.

## Related

- [[WatchdogOfWatchdogsArchitecture]] — layered guards whose self-shutdowns motivated this
- Source: [[feedback-2026-07-07-reboot-classification-and-concurrent-missions]]
