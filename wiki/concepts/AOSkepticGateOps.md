---
title: "AO Skeptic Gate — Operational Lessons"
type: concept
tags: [agent-orchestrator, skeptic-gate, ops, evidence, antigravity, ci]
sources: [keychain-ao-skeptic-2026-06-05.md]
last_updated: 2026-06-05
---

## Summary

Operational lessons for running the Agent Orchestrator (AO) Skeptic Gate as a live system — distinct
from the CI-gate mechanics in [[SkepticGate]]. Focuses on what breaks when AO workers are killed and
how to post verdicts manually.

## Killing AO Workers Has Two Side Effects

1. **Breaks the Skeptic Gate.** Killing AO workers removes the verdict-poster, so the gate gets no
   verdict and hits a **20-minute timeout** instead of resolving.
2. **Regresses the agent-antigravity dist.** AO rebuilds from the *currently checked-out branch*, so
   killing/restarting workers on a feature branch can roll the distributed build backward.

**Durable fix:** merge to `main`. A branch-local fix is undone the next time AO rebuilds the dist.

## Posting Skeptic Verdicts Manually

```bash
ao skeptic verify -n <PR> -m claude --trigger-sha <sha> --request-id <id>
```

- `--dry-run` — preview the verdict without posting.
- `--prompt` — scope the evidence to the **feasible class** for the PR. Example: a macOS-GUI fix
  cannot be CI-integration-tested, so scope the evidence prompt accordingly rather than demanding a
  CI integration artifact that can never exist.

## Evidence Discipline

- **Do NOT commit evidence `.md` files** — they trip CodeRabbit and the Evidence Gate. Publish
  evidence as **gists** and link them instead.

## Connections
- [[SkepticGate]] — the underlying CI-gate mechanics (evidence-over-assertion).
- [[AgentOrchestrator]] — the orchestration system whose workers post verdicts and rebuild the dist.
- [[macOS Keychain]] — the 2026-06-05 session where these ops lessons were captured.
