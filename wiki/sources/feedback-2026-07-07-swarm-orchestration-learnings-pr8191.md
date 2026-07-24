---
title: "Swarm Orchestration Learnings — design-retro-2026-06 mission (PR #8191)"
type: source
tags: [swarm, orchestration, sidekick, rate-limiting, publishability-gate]
date: 2026-07-07
source_file: feedback_2026-07-07_swarm_orchestration_learnings_pr8191.md
---

## Summary

Six durable lessons captured from running the design-retro-2026-06 multi-agent swarm mission (session e3cce9b6, PR #8191, worldarchitect.ai repo) on 2026-07-06/07. The mission ran ~180+ adversarial sub-agents across multiple Workflow-tool fan-outs (mining → adversarial verify → doc-writing) to produce a retrospective docset, and hit two distinct classes of failure: (1) provider rate-limiting during resume attempts that produced misleadingly "clean" empty results, and (2) a cold adversarial review that found real defects surviving the entire verification chain because nothing ever re-checked the *published artifacts* as a whole.

## Key Claims

- A workflow returning 0 confirmed findings is a VOID, not a verdict, when its failure list shows mass agent death (e.g. every rejection reason is a dead-verifier placeholder, or the failures array is dominated by provider 429s) — happened twice in one session, each time with real candidate findings from a healthy earlier stage.
- Provider rate-limiting is triggered by aggregate concurrency across ALL sibling swarms running concurrently on an account, not by any single workflow's size — two individually-reasonable workflows both died once their combined in-flight agent count reached ~75.
- Multiple concurrently-running "sidekick" orchestrator agents sharing one STATE.md file must namespace their sections — reusing a generic heading (like "Next Actions") to record a different mission's plan silently overwrites a different live worker's plan.
- The sidekick pattern as implemented (a Claude Code "teammate") only survives conversation-level crashes, not a full host/process death — since a teammate's lifetime is bound to its parent CLI process. True cross-reboot durability requires an independently-scheduled worker process (e.g. an Agent Orchestrator worker).
- Adversarial verification pipelines that only ever score *candidate findings* (claims about a codebase) can still ship defective *rendered artifacts* (docs, PRs) because no lane in the pipeline ever re-reads the finished output as a whole — this produced 6 concrete defect classes (leaked credential paths, a stale cross-doc metric contradiction, a forbidden architecture recommendation, contradicting parallel doc tracks, a false-green test recipe, and the absence of any final whole-artifact gate) surviving ~180 verifying agents.
- The fix for the last point is a dedicated, final, whole-artifact "publishability gate" stage that runs after all writer lanes and checks: credential/path redaction, cross-doc numeric consistency, freshness vs. current branch head, supersession markers on superseded drafts, a repo-specific policy lens, recipe/acceptance-check validity, and basic mechanical hygiene (e.g. clean whitespace diffs).

## Key Quotes

> "0 confirmed is 100% an artifact of rate-limiting, not a real adversarial rejection." — session note on the pr-retro-gapfill workflow VOID result

> "these are not lapses of individual reviewers; each is a structural consequence of how the swarm was shaped." — from the adversarial gap report explaining why ~180 agents missed the six defect classes

## Connections

- [[swarm-orchestration-pattern]] — the general multi-agent Workflow-tool pattern this session's lessons refine, including the sidekick durability layer and its teammate-vs-independent-worker limitation
- [[publishability-gate]] — the new final-stage gate concept this source introduces
- [[jleechanorg-agent-orchestrator]] — the independent-worker upgrade path for true sidekick crash-durability
