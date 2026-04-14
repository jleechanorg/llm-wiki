---
title: "SMT-Based Verification"
type: concept
tags: [Z3, SMT, formal-verification, symbolic, bounded-model-checking, lightweight-formal-methods]
sources: [formal-verification-frontier]
last_updated: 2026-04-14
---

## Summary

SMT (Satisfiability Modulo Theories) solvers like Z3 provide a practical middle ground between informal testing and heavyweight proof assistants like Lean or Coq. Rather than requiring full formal proofs, SMT-based verification lets agents express code contracts (preconditions, postconditions, loop invariants) as Horn clauses and automatically check them via bounded model checking. Ideal for AI coding agents that need "probably correct with high confidence" without the overhead of proof assistants.

## Key Claims

### SMT vs Proof Assistants

| Tool | Approach | Overhead | Soundness |适合 AI Agent |
|------|----------|----------|-----------|--------------|
| Lean/Coq | Interactive proofs | Very high | Complete | Hard to integrate |
| Z3/STP | Automatic solving | Low | Bounded | Ideal for agents |
| Testing | Bug finding | Low | No guarantee | Insufficient |

### How AI Agents Can Use Z3

1. **Specification extraction**: Agent reads code and infers likely contracts (pre/post conditions)
2. **Invariant generation**: Agent proposes loop invariants based on code patterns
3. **Bounded checking**: Z3 checks whether contracts hold for all inputs within a finite bound (e.g., all arrays up to length 10)
4. **Counterexample generation**: If violation found, Z3 returns a concrete input that triggers it — useful for adversarial testing

### Common Z3 Use Cases for Code Agents

- **Array bounds verification**: Prove `i < len(arr)` given loop conditions
- **Memory safety**: Prove no null dereference or use-after-free paths
- **Concurrency contracts**: Prove lock ordering invariants
- **Protocol verification**: Prove state machine never reaches invalid states

### Integration with Verification Loop

```
Code Generation → Contract Extraction → Z3 Bounded Check →
If violation: Generate counterexample → Fix code → Re-verify
If passes: High confidence (bounded) → Continue
```

This fits naturally into the [[VerificationLoop]]: bounded formal verification as an intermediate gate between testing and full proof.

## Connections

- [[FormalVerification]] — broader concept; Z3 is a lightweight practical form
- [[VerificationLoop]] — SMT can serve as the automated verification step
- [[AdversarialTesting]] — Z3 counterexamples are perfect adversarial inputs
- [[SkepticAgent]] — skeptic could request Z3 verification before accepting code
- [[Lean]] / [[Coq]] — heavier alternatives when bounded verification is insufficient

## See Also

- [[FormalVerification]] — Lean/Coq-based formal proofs
- [[VerificationLoop]] — the full generate → verify → fix pipeline
- [[AdversarialTesting]] — counterexample generation for adversarial test cases
