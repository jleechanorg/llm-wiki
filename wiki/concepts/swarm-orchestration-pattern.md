---
title: "Swarm Orchestration Pattern (/swarm)"
type: concept
tags: [swarm, orchestration, workflow-tool, sidekick, adversarial-verification, publishability-gate]
date: 2026-07-07
last_updated: 2026-07-07
---

## Overview

The `/swarm` pattern (worldarchitect.ai `~/.claude/skills/swarm/SKILL.md`) runs a goal as a deterministic Workflow-tool fan-out: `agent()/parallel()/pipeline()` scripts that mine, adversarially verify, and write findings, with a persistent "sidekick" durability layer supervising the whole run so it survives conversation crashes. Distilled from the 2026-07-06/07 design-retro-2026-06 mission (~180+ agents across 5+ workflows, PR #8191).

## Canonical shape

Collect (themed miners) → Verify (≥3 independent refute-by-default adversarial lenses per candidate) → Solutions/Docs (one writer agent per confirmed finding, single-file write lock) → [publishability gate, see below].

## Sidekick durability layer

One persistent background "teammate" agent owns the swarm; the main session only writes/updates a disk-checkpointed `STATE.md`, spawns the sidekick, and relays milestones. The sidekick reads `STATE.md` on start (never redoes logged steps), commits+pushes after every green unit of work, and propagates the commit-often instruction into every sub-agent prompt.

**Known limitation**: the sidekick-as-teammate only survives *conversation* crashes, not a full host/process death (a teammate's lifetime is bound to its parent CLI process). True cross-reboot durability needs an [[jleechanorg-agent-orchestrator]]-style independently-scheduled worker instead.

**Multi-sidekick namespacing**: when more than one sidekick shares a STATE.md (e.g. two concurrent missions in the same repo), each must write its own mission into a clearly-separated named section rather than reusing a generic heading like "Next Actions" — reusing the heading silently overwrites a different live worker's plan.

## Failure modes discovered 2026-07-06/07

- **False-empty completion / VOID results**: a workflow returning 0 confirmed findings can be an artifact of mass agent death (provider 429s killing every verifier), not a real "nothing found" verdict. Detect by checking whether the failure list is dominated by rate-limit errors or every rejection reason is a dead-verifier placeholder.
- **Aggregate rate-limit concurrency**: provider 429s are triggered by the TOTAL agent count in flight across ALL concurrently-running swarms on an account, not any single workflow's size — serialize big fan-outs across sibling swarms, use a tiny throwaway "sibling-workflow-as-canary" to probe health before resuming a real fan-out.
- **Publishability gate gap**: adversarial verification pipelines that only score candidate findings — never the rendered artifacts that ship — can still publish real defects (leaked paths, stale cross-doc claims, forbidden recommendations, contradicting doc tracks, false-green recipes) because no lane ever re-reads the finished output as a whole. See [[publishability-gate]].

## Related

- [[MultiAgentOrchestration]] — the general multi-agent-framework concept this pattern specializes
- [[publishability-gate]] — the final whole-artifact gate this pattern's newest rule introduces
- [[jleechanorg-agent-orchestrator]] — the independent-worker upgrade path for true sidekick durability
