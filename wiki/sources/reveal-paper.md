---
title: "ReVeal: LLM Verification Against Evidence Standards"
type: source
tags: [verification, evidence-standards, ReVeal, formal-verification, skeptical-agents]
date: 2026-04-14
source_file: research/ReVeal-2026
---

## Summary

ReVeal (2026) applies rigorous self-critique + verification against explicit evidence standards to LLM-generated code. Models critique their own outputs against correctness criteria, security standards, and codebase conventions — then fix issues in a closed loop before final output. Forms the basis for skeptic gates and verification loops in production agent pipelines.

## Key Claims

### Verification Criteria (Evidence Standards)
1. **Correctness** — Does it solve the stated problem?
2. **Edge cases** — Does it handle boundary conditions?
3. **Security** — Are there vulnerabilities, injection risks?
4. **Performance** — Efficiency and resource usage
5. **Style** — Adherence to codebase conventions

### Closed Loop Pattern
```
Generate → Verify against standards → If issues: Fix → Re-verify → Repeat (max N iterations)
Only output when all gates pass
```

### Results
- Error detection rate: 78.7% of self-identified issues are real bugs
- Models generate 55.8% vulnerable code by default; verification catches most
- Test-time compute invested here pays off in post-merge reduction

## Connections

- [[VerificationLoop]] — the full pipeline
- [[EvidenceReviewPipeline]] — your existing two-stage pipeline
- [[SkepticAgent]] — the skeptic reviewing claims
- [[AdversarialTesting]] — generating edge cases to attack own code
