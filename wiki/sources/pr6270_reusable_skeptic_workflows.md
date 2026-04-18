---
title: "PR #6270 — Infrastructure: Migrate to Reusable Skeptic Workflows"
type: source
tags: [infrastructure, CI, skeptic-gate, workflow, agent-orchestrator]
date: 2026-04-15
source_file: wiki/sources/pr6270_reusable_skeptic_workflows.md
---

## Summary
Migrates worldarchitect.ai skeptic automation from in-repo GitHub Actions logic to reusable workflows in `jleechanorg/agent-orchestrator`. Reduces `skeptic-cron.yml` and `skeptic-gate.yml` to thin callers. Deletes local `skeptic-evaluate.sh`. Changes are medium risk — failures in the external reusable workflows could block/merge PRs unexpectedly.

## Key Claims
- `skeptic-gate.yml` and `skeptic-cron.yml` replaced with calls to `jleechanorg/agent-orchestrator/.github/workflows/skeptic-*-reusable.yml@main`
- Thin callers pass runner labels/inputs and inherit secrets
- Local inline gate/trigger/poll implementations removed
- Verified triggers match original definitions

## Key Quotes
> "Replaces local skeptic gate/cron logic with thin callers to agent-orchestrator. Eliminates code duplication and drift." — PR description

## Connections
- [[Skeptic Gate]] — now delegates to external agent-orchestrator reusable workflows
- [[agent-orchestrator]] — external workflow provider (jleechanorg/agent-orchestrator)
- Related: PR #6269 (Port CR Fallback Logic to Skeptic Gates)
