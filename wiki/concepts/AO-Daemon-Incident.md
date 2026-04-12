---
title: "AO Daemon Incident Masking"
type: concept
tags: [agent-orchestrator, daemon, launchd, AO, incident]
last_updated: 2026-04-09
---

AO monitor was reported "disabled" but the launchd label was enabled — the wrapper died under `set -u` while sourcing interactive shell init, masking the real blocker.

## Root Cause

Wrapper script `stability-report.launchd.sh` used `set -u` (nounset) while sourcing an interactive shell init file that referenced unset variables. The script exited silently, making the daemon appear dead.

## Real Blocker

Once fixed, AO logs showed the real blocker: PR backfill failing on a stale checked-out worktree branch lock.

## Pattern

AO daemon incidents can mask the real blocker. When a daemon appears dead, check:
1. Is the launchd label enabled?
2. Does the wrapper script have `set -u` or `set -e`?
3. Does it source interactive shell init files?
4. What's in the actual AO logs?

## Also Found

AO split-brain: duplicate lifecycle workers (`worldarchitect` x3 plus alias `worldarchitect.ai`) while `ai.agento.lifecycle-all` sat `not running` — claims looked attached briefly then lost durable registration.

## Connections

- [[AO-Split-Brain]] — AO split-brain with duplicate lifecycle workers
- [[AO-Blocker-Matrix]] — PR blocker triage
- [[AO-Claim-Fail-Closed]] — AO claim fail-closed execution
- [[DaemonBootstrap]] — daemon bootstrap patterns
