---
title: "Agentic Self-Critique + Formal Verification — Frontier AI (2026)"
type: source
tags: [self-critique, formal-verification, adversarial-testing, self-repair, self-debug, proof, lean, coq, skeptic]
date: 2026-04-14
source_file: frontier-research/formal-verification-2026.md
---

## Summary

The next evolution beyond generate-PR: agents that generate code + tests + formal proofs + adversarial examples, then critique and fix their own output in a closed loop. Moving from "probably correct" to "provably correct." Your existing evidence standards, skeptic gates, and beads system are already halfway there — this is the natural extension.

## Key Claims

### The Gap: Most "AI Generated Code" Is Unverified
- AI writes code that passes tests
- But tests are also written by AI → same blind spots
- No adversarial examination of edge cases
- No formal guarantees, just "seems to work"

### The Agentic Self-Critique Loop
```
Code Generation → Test Generation → Adversarial Examples → 
Formal Proof Attempt → Critique → Fix → Repeat until verified
```

### Formal Verification Tools Emerging (2026)
- **Lean** — formal proof assistant, increasingly used for code verification
- **Coq** — proof assistant for certified software
- **Alphacode** — DeepMind's competitive programming system with self-evaluation
- **Copilot + verification plugins** — IDE-integrated formal checks

### Adversarial Example Generation
- Model generates edge cases that break its own code
- Then fixes those edge cases
- Repeat until no more adversarial examples found

### Your Infrastructure Already Does Half of This
| What You Have | What It Enables |
|--------------|-----------------|
| Evidence review gate | Skeptic reviews code + tests + claims |
| Beads tracking | Proven patterns get priority; broken patterns flagged |
| [[DeterministicFeedbackLoops]] | Automated regression detection |
| [[Skeptic]] | LLM-judgment review of claims |

**What's missing for full self-critique loop:**
- Automated adversarial example generation
- Formal proof integration (Lean/Coq)
- Multi-pass self-verification before PR

## Connections

- [[SelfCritique]] — concept page
- [[FormalVerification]] — concept page
- [[AdversarialTesting]] — concept page
- [[EvidenceReviewPipeline]] — your existing skeptic gate
- [[SkepticAgent]] — the agent that reviews claims
