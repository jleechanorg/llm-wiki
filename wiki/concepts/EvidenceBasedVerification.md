---
title: "Evidence-Based Verification"
type: concept
tags: [evidence-standards, verification, skeptic, ReVeal, multi-criteria, correctness, security]
sources: [ReVeal, formal-verification-frontier]
last_updated: 2026-04-14
---

## Summary

Evidence-Based Verification is the practice of evaluating AI-generated code against a structured checklist of explicit evidence criteria before accepting it as correct. [[ReVeal]] demonstrated that models generate 55.8% vulnerable code by default, but most errors are caught when verified against evidence standards (correctness, edge cases, security, performance, style). This is the formal foundation for skeptic gates in production agent pipelines.

## Key Claims

### The Five Evidence Criteria (from ReVeal)

1. **Correctness** — Does it solve the stated problem?
2. **Edge cases** — Does it handle boundary conditions (empty input, max values, nulls)?
3. **Security** — Are there injection risks, authentication bypasses, data exposure?
4. **Performance** — Efficiency and resource usage within acceptable bounds
5. **Style** — Adherence to codebase conventions and readability

### Why Evidence Standards Beat "Looks Good"

| Approach | Error Detection Rate |
|----------|---------------------|
| LLM self-assessment ("looks good") | ~44% (generates 55.8% vulnerable) |
| Evidence standards checklist | ~78.7% of self-identified issues are real |
| Evidence standards + skeptic review | Higher still |

### Integration with Skeptic Pipeline

```
Generate → Self-verify against evidence criteria →
If issues found: Fix → Re-verify (max N iterations) →
Skeptic reviews evidence bundle →
If skeptic approves: Pass gate → PR created
```

This maps directly to the [[EvidenceBundles]] and [[EvidenceGateVsCompileCI]] distinction: evidence bundles are comprehensive proof of quality, while compile CI is merely necessary (not sufficient).

### What Evidence Must Include

Per [[EvidenceReviewPipeline]]:
- Correctness proof (tests pass, edge cases covered)
- Security review (no OWASP Top 10 violations)
- Performance validation (p99 latency, memory under load)
- Contradiction check (no conflicts with existing patterns)
- Skeptic sign-off

## Connections

- [[ReVeal]] — the source paper establishing evidence standards effectiveness
- [[SkepticAgent]] — the agent that reviews evidence bundles
- [[EvidenceReviewPipeline]] — the full pipeline from generation to skeptic approval
- [[VerificationLoop]] — evidence verification is the core of the loop
- [[SelfCritique]] — self-critique generates the evidence in the first pass
- [[AdversarialTesting]] — adversarial tests provide edge case evidence

## See Also

- [[SkepticAgent]] — the skeptic reviewing evidence
- [[EvidenceBundles]] — the artifact being reviewed
- [[VerificationLoop]] — evidence-based verification is the loop's core
