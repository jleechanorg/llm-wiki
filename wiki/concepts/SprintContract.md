---
title: "Sprint Contract"
type: concept
tags: [sprint, contract, scope-lock, negotiation, planning]
date: 2026-03-24
source: [[anthropic-harness-design-long-running-apps]]
---

## Definition
A **sprint contract** is a negotiated agreement between Generator and Reviewer (or Evaluator) that defines what "done" looks like for a given sprint — before any code is written. It locks scope and provides concrete testable criteria for evaluation.

## Why It Works
Without contracts, scope drifts over multi-hour runs. The contract forces explicit agreement on deliverables, making failure criteria clear. Generator self-evaluation can then compare against the contract.

## Protocol
```
Generator: "Sprint 3: user auth. Done: (1) /login renders, (2) POST /api/login returns 200 JWT,
           (3) unauthenticated /dashboard redirects. Self-eval: Func 85, Code 80."

Reviewer: "Agreed. Add: (4) invalid creds return 401, (5) JWT must be RS256."

Generator: "Added. Contract locked."

Orchestrator: "signed → Generator unlocked."
```

Max 2 negotiation rounds. Orchestrator arbitrates if no agreement.

## Example Sprint Criteria
- Sprint contract can have 20+ criteria (Anthropic example had 27 test criteria for sprint 3)
- Criteria must be concrete and testable, not abstract goals
- Each criterion maps to a specific verification method

## Connections
- [[GeneratorEvaluatorSeparation]] — the contract is between Generator and Evaluator/Reviewer
- [[SprintContract]] — negotiated before each build chunk
- [[OrchestratorResponsibilities]] — orchestrator arbitrates and enforces contract
- [[FileBasedHandoffs]] — contract persisted as `sprint_contract.md`
