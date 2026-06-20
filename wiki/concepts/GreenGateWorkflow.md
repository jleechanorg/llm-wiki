---
title: "Green Gate Workflow"
type: concept
tags: [green-gate, ci, pr-workflow, skeptic-gate, bugbot, smoke]
sources: [pr7720-ios-webkit-indexeddb-persistence-deadlock]
last_updated: 2026-06-20
---

# Green Gate Workflow

## What Green Gate keys on

Green Gate keys off the **latest Skeptic Self-Verify VERDICT** for the current head SHA. The dispatch order matters:

1. Dispatch **MCP Smoke (real)** first.
2. Dispatch **Skeptic AFTER it**, pinned to the current head SHA.

## Gate 8 quirk (smoke skip)

The Skeptic's Gate 8 skips smoke when it can't find the workflow. This means smoke is NOT the true blocker. The true blockers are:

- CI green (core-mvp + dependent shards)
- Resolved threads (CodeRabbit + chatgpt-codex-connector)
- Bugbot NEUTRAL verdict

If smoke didn't run, that is not a Green Gate blocker — verify the three above are present instead.

## Self-hosted CI flakes (NOT regressions)

On self-hosted runners, expect:

- `core-mvp` shards OOM-`Killed` (...truncated in source...)
- Intermittent timeouts on long-tail test steps

When a flake occurs, re-run the affected shard once. Do not classify the flake as a regression unless it reproduces on a clean re-run.

## Related

- [[PRMidReviewMergeAncestryCheck]]
- [[IntegrateHardStopPattern]]
- [[MobileAuthReproFidelity]]
- [[PR7720]]
