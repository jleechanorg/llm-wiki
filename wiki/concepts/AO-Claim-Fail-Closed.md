---
title: "AO Claim Fail-Closed Execution"
type: concept
tags: [agent-orchestrator, claims, fail-closed, execution-verification]
last_updated: 2026-04-08
---

AO can mark claims as covered when workers fail immediately or attach to the wrong PR/session. Root-cause follow-ups needed to enforce execution proof and clean-worktree preflight before claim success.

## Problem

AO claim path has fail-open states:
- Worker fails immediately → claim still marked as covered
- Worker attaches to wrong PR/session → claim marked as covered
- No execution proof required before claim success

## Fixes Needed

1. Enforce clean-worktree preflight before claim attempt
2. Require execution proof (not just exit code)
3. Fail-closed: if execution cannot be verified, don't mark claim as covered

## Fail-Closed States

- `lifecycle.backfill.claim_failed` entries should surface immediately
- Blocked claims (`Workspace has uncommitted changes`) are legitimate blockers
- Fetch-stage stale-worktree failure now self-heals in local scm-github

## Connections

- [[AO-Blocker-Matrix]] — PR blocker matrix triage
- [[AO-Split-Brain]] — AO duplicate lifecycle workers
- [[AO-Daemon-Incident]] — AO daemon incidents masking blockers
