---
title: "Auto-Research Experiment v2.1"
type: source
tags: [agent-harness, llm-wiki, self-research, coding-agents]
date: 2026-04-14
source_file: gist/0620377b1944f8c4b244aee1f55fa1ea
---

## Summary

Streamlined version of the auto-research experiment system (v2.1, April 2026) — a subset of the master system focused on 3 core skills (self-critique loop, auto-research loop, canonical scorer) without the Product Taste Layer. Tests frontier coding techniques (2025–2026) on real historical PRs while letting the system generate and test its own novel hypotheses.

## Key Claims

- **Self-Discovering Meta-Research Loop**: Agent generates its own hypotheses based on PR patterns, tests published papers, evaluates rigorously, and updates the wiki
- **Grounded in real PR history**: Test-PRs directory contains 12–15 historical PR descriptions + diffs for replay
- **3-iteration cap on self-critique**: Balances quality vs token efficiency
- **Rubric + diff similarity scoring**: Quantitative evaluation of generated code quality
- **beads integration**: Every experiment run tracked as a bead

## Key Components

### program.md (LLM Wiki Compiler)

```
# LLM Wiki Program - Research Compiler & Experiment Tracker

Rules:
- Read all documents in raw/ and canonical-repos/
- For each paper, create one clean markdown concept page with: technique summary, exact prompts, results, limitations
- For each canonical repo, create pattern pages (e.g., "Error Handling in FastAPI", "Type-Safe API Design in tRPC")
- After every auto-research run, add a "Results on My Codebase" section with metrics (pass rate, iterations, token usage, rubric score, diff similarity)
- Maintain index.md with summaries and cross-references
- Never hallucinate. Only use content from raw/ and canonical-repos/
- Output only markdown files ready for the wiki/ directory
```

### skills/self_critique_verification_loop.md (ReVeal 2026 + Self-Correction 2025 – 3-iteration cap)

- Phase 0: Insert canonical pattern prompt from wiki
- Phase 1: Step-by-step code generation
- Phase 2: Full test suite + sandboxed execution
- Phase 3: Self-critique; loop back to Phase 2 if issues found and iterations < 3
- Max 3 iterations; exact output format required

### skills/auto_research_loop.md (Self-Discovering Meta-Research)

- Phase 0: Generate 1–3 novel, falsifiable hypotheses from PR patterns
- Phase 1: Select next PR or hypothesis
- Phase 2: Implement using self_critique_verification_loop
- Phase 3: Score baseline vs improved via canonical_code_scorer
- Phase 4: Update wiki + create bead

### skills/canonical_code_scorer.md

- 6 rubric dimensions, weighted Pass/Fail scoring
- Diff similarity: token-level edit distance to ground-truth
- Overall = 0.7 × rubric Pass-rate + 0.3 × diff similarity

### scripts/verify_setup.sh

Bootstrap verification — checks all required directories exist, at least one canonical repo cloned, at least one PR file present.

## Master Launch Prompt

```
Start the full self-discovering auto-research experiment.

1. Load all papers from raw/ and all canonical repos.
2. Run Phase 0 to generate 1–3 novel hypotheses based on patterns in my codebase.
3. Select the next historical PR from test-prs/ or test one of the generated hypotheses.
4. Run baseline (direct generation with current harness).
5. Run improved version using the current paper's technique OR the generated hypothesis + self_critique_verification_loop (with real sandboxed test execution).
6. Score both versions using the canonical_code_scorer.
7. Record everything in the wiki with full metrics and create beads for every run.
8. Repeat for the next PR or hypothesis.

Maintain the wiki continuously.
```

## Connections

- [[SelfCritiqueVerificationLoop]] — the verification loop skill
- [[AutoResearchLoop]] — the meta-research loop skill
- [[CanonicalCodeScorer]] — the scoring engine concept

## Contradictions

- No contradictions — this is a streamlined subset of [[auto-product-master-system]] which additionally includes the Product Taste Layer
