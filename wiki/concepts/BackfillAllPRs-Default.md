---
title: "backfillAllPRs Opt-Out Default Bug"
type: concept
tags: [agent-orchestrator, backfill, CI, bug, AO]
last_updated: 2026-04-06
---

worldarchitect project in agent-orchestrator.yaml silently omitted backfillAllPRs:true, causing 5 WA PRs (#6109/#6116/#6118/#6119/#6122) to sit CI-green but CR-blocked for days.

## Problem

The backfillAllPRs flag was not set to true in the worldarchitect project config. This silently disabled PR backfill for that project.

## Impact

5 worldarchitect.ai PRs blocked at CR stage despite green CI — nobody knew why.

## Fix

PR #404 to flip default to opt-out + warn observation for explicit opt-out projects with open PRs.

## Pattern

Silent configuration gaps in AO project configs can cause PRs to be silently excluded from automated workflows.

## Connections

- [[AO-Blocker-Matrix]] — PR blocker triage
- [[AO-Claim-Fail-Closed]] — AO claim fail-closed execution
