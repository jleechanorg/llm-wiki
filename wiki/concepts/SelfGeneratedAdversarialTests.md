---
title: "Self-Generated Adversarial Tests"
type: concept
tags: [adversarial-testing, self-generated-tests, fuzzing, counterexamples, formal-verification]
sources: [formal-verification-frontier, ReVeal, swe-bench-2026]
last_updated: 2026-04-14
---

## Summary

Self-Generated Adversarial Tests is the practice where an AI coding agent generates adversarial test cases designed to break its own code — then fixes the code to survive those tests. This closes the loop on the observation from [[ReVeal]] that AI generates 55.8% vulnerable code by default: instead of hoping tests catch vulnerabilities, the agent actively hunts for the inputs that will expose them. The [[FormalVerification]] frontier identified this as a key missing component of the self-critique loop.

## Key Claims

### Why Self-Generated Tests Are Harder Than Generated Tests

Standard test generation: "What should the code do on valid inputs?"
Adversarial test generation: "What inputs will make the code do the *wrong* thing?"

The latter requires:
1. Understanding the code's actual logic (not just its interface)
2. Reasoning about what could go wrong at each branch point
3. Generating inputs that violate implicit contracts
4. Distinguishing between "this crashes" and "this returns wrong answer silently"

### The Adversarial Loop

```
Code Generated →
Adversary Module: "What inputs would break this?" →
Generate N adversarial test cases →
Run against code →
If test fails: Code has a bug → Fix →
Repeat (max K adversarial rounds)
→ Adversarial-hardened code
```

### Connection to [[ReVeal]]

[[ReVeal]] established that:
- Models generate 55.8% vulnerable code by default
- Self-verification catches most vulnerabilities (78.7% of self-identified issues are real)

Self-generated adversarial tests amplify this:
- Not just "does it pass my tests?" but "can I construct inputs that make it fail?"
- Tests the invariants, not just the happy path
- Particularly powerful for: security (injection, auth bypass), concurrency (race conditions), and edge cases (null, empty, overflow)

### Connection to [[SMT-BasedVerification]]

[[SMT-BasedVerification]] (Z3) is the natural engine for adversarial test generation:
- Z3 counterexample generation produces concrete inputs that violate formal contracts
- These counterexamples ARE adversarial test cases
- The formal verification loop: Contract → Z3 → Counterexample → Fix → Re-verify

### [[SWE-bench]] Connection

On [[SWE-bench]], adversarial test generation helps because:
- The original test suite may not cover the specific bug scenario
- Agent generates additional tests targeting the issue description
- Harder issues (lower pass rates) often require adversarial thinking to uncover the real problem

## Connections

- [[AdversarialTesting]] — broader concept; self-generated adversarial tests are a specific implementation
- [[ReVeal]] — the evidence standards that reveal the 55.8% vulnerability rate
- [[FormalVerification]] — formal methods provide the strongest adversarial test generation (Z3 counterexamples)
- [[SMT-BasedVerification]] — Z3 is the tool for generating adversarial inputs from formal contracts
- [[VerificationLoop]] — adversarial tests are the "hard" verification step in the loop
- [[SelfDebugging]] — fixing bugs found by adversarial tests

## See Also

- [[AdversarialTesting]] — general adversarial testing
- [[SMT-BasedVerification]] — Z3 as the adversarial test generator
- [[VerificationLoop]] — where adversarial tests fit in the pipeline
