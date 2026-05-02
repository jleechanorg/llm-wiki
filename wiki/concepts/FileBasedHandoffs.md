---
title: "File Based Handoffs"
type: concept
tags: [file-based, handoff, state-persistence, agent-restart, persistence]
date: 2026-03-24
source: [[anthropic-harness-design-long-running-apps]]
---

## Definition
Communication between agents via files instead of in-memory state. One agent writes artifacts, the next reads and resumes. This enables agents to survive restarts and operate independently.

## Key Artifacts
| Artifact | Written By | Read By | Purpose |
|----------|-----------|---------|---------|
| research.md | Researcher | Strategist, Generator | Deep codebase understanding |
| spec.md | Strategist | All | Full product specification |
| plan.md | Strategist | Reviewer, Generator | Feature breakdown with priorities |
| plan_review.md | Reviewer | Generator | L1 constraint violations, corrections |
| sprint_contract.md | Generator + Reviewer | Both | Agreed "done" criteria before sprint |
| sprint_N_report.md | Generator | Evaluator | What was built + self-eval |
| sprint_N_eval.md | Evaluator | Generator, Orchestrator | Dual verdict + scores |
| harness_state.json | Orchestrator | All | Canonical state; survives restarts |

## Why File Over Memory
- **Restart proof**: agents can terminate and resume without losing state
- **Independent operation**: each agent reads its inputs independently
- **Audit trail**: every decision is captured in artifact
- **Orchestrator arbitration**: orchestrator can inspect any artifact

## Connections
- [[ContextReset]] — resets use handoff artifacts to restore state
- [[SprintContract]] — contract persisted as `sprint_contract.md`
- [[OrchestratorResponsibilities]] — orchestrator maintains canonical state