---
title: "AO Split-Brain"
type: concept
tags: [agent-orchestrator, split-brain, lifecycle-workers, AO, claims]
last_updated: 2026-04-07
---

worldarchitect control plane had duplicate lifecycle workers (`worldarchitect` x3 plus alias `worldarchitect.ai`) while `ai.agento.lifecycle-all` sat `not running`. Claims appeared attached briefly then lost durable registration.

## Root Cause

Duplicate project names in AO config causing multiple worker instances to compete for the same work.

## Symptoms

- Claims attached to one worker, then immediately lost
- `ai.agento.lifecycle-all` appears not running
- Multiple `worldarchitect` workers visible in tmux
- No durable claim registration

## Files

- `~/.openclaw/logs/lw-watchdog.log` — watchdog logs showing duplicate workers
- `scripts/lw-watchdog.sh` — watchdog script that detects this
- `scripts/start-all.sh` — startup script that may introduce duplicates

## Pattern

AO can mark claims as covered when workers fail immediately or attach to the wrong PR/session. The split-brain state causes workers to fight over claims, with none winning durably.

## Connections

- [[AO-Daemon-Incident]] — daemon incidents masking blockers
- [[AO-Claim-Fail-Closed]] — AO claim fail-closed execution
- [[AO-Blocker-Matrix]] — PR blocker triage
- [[AO-Uncovered-Split]] — uncovered vs blocked split
