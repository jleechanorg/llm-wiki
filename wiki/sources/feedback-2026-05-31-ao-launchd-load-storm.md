---
title: "AO launchd respawners cause runaway load — kill is insufficient, bootout the agents"
type: source
tags: [feedback, project, worldarchitect-ai, memory-file]
date: 2026-05-31
source_file: raw/memory_backfill_2026_06_13/feedback_2026-05-31_ao_launchd_load_storm.md
---

## Summary

Machine became unusable: (~35× oversubscription, 0% idle, 47GB RAM used / 248MB free, 100M+ swapins). Symptom looked like "PRs are heavy" but the PR/review work was negligible. Root cause was an .

## Key Claims

- `com.apple.Virtualization.VirtualMachine` (Docker's Linux VM) — **255% CPU** + `com.docker.backend` 61%.
- **~44 `agy` (Antigravity/Gemini AO worker) processes** — ~423% CPU aggregate.
- `openclaw-gateway` crash-looping (etime 5–14s, ~50% CPU) — constantly respawned.
- AO `lifecycle-worker cmux` (respawns agy), plus `eloop` drivers.
- 1,496 procs / 13,152 threads / 23 user sessions.
- `uptime` 486→8.05; `pgrep -xc agy`=0, `pgrep -fc openclaw-gateway`=0, `lifecycle-worker`=0, VM=0.
- Protected confirmed alive: `pgrep -fc 'cmux DEV'`=9, `pgrep -fc 'bin/claude'`=5.
- Reports: /tmp/triage_report.txt, /tmp/ao_fullstop_report.txt.

## Key Quotes

_(No blockquotes in source)_

## Connections

_(No prior wiki links detected)_
