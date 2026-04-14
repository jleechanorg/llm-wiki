---
title: "Master AI Research & Product Taste System"
type: source
tags: [agent-harness, llm-wiki, self-research, product-judgement]
date: 2026-04-14
source_file: gist/db97de6d82fe4af89f75e0479fb6a6f2
---

## Summary

A complete self-contained master document (Version 2.1, April 2026) that integrates the Karpathy LLM Wiki, a self-discovering auto-research loop that tests techniques on real historical PRs, and a new Product Taste Layer for codifying personal product judgement. Runs inside an existing agent harness (beads, MCP, evidence standards, skeptic gates).

## Key Claims

- **LLM Wiki**: Living, self-maintaining knowledge base for papers, canonical code, and experiment results
- **Self-Discovering Meta-Research Loop**: Agent generates its own falsifiable hypotheses from PR patterns, then tests published techniques and own ideas against real PRs
- **Product Taste Layer**: Codifies and continuously refines personal product judgement so PRs match what you actually want, not just technically correct
- **Scoring Engine**: Rubric (6 dimensions) + diff similarity against canonical clean code, weighted 0.7/0.3
- **Integration**: Runs inside existing harness — beads for tracking, MCP for context, evidence standards for verification

## Key Components

### Skills (5 total)

1. **self_critique_verification_loop.md** — 3-iteration cap verification loop (ReVeal 2026 + Self-Correction 2025)
   - Phase 0: Prompt chaining from wiki canonical patterns
   - Phase 1: Step-by-step code generation
   - Phase 2: Full test suite generation + sandboxed execution
   - Phase 3: Self-critique against test results; iterate if needed (max 3)
   - Output: initial code, test results, critique, revised code (if needed), final verified code

2. **auto_research_loop.md** — Self-discovering meta-research loop
   - Phase 0: Hypothesis generation from PR patterns (1–3 novel, falsifiable hypotheses)
   - Phase 1: PR/hypothesis selection
   - Phase 2: Implementation with self_critique_verification_loop
   - Phase 3: Baseline vs improved scoring via canonical_code_scorer
   - Phase 4: Wiki update + bead creation

3. **canonical_code_scorer.md** — Rubric + diff similarity scoring
   - 6 rubric dimensions (Pass/Fail): Naming & Consistency, Error Handling, Type Safety/Architecture (30% weight), Test Coverage, Documentation, Evidence-Standard Adherence
   - Diff similarity: token-level edit distance to ground-truth PR file → 0–100 score
   - Overall = 0.7 × rubric-weighted Pass-rate + 0.3 × diff similarity

4. **product_judge.md** — Product Taste Oracle
   - Scores each PR: Strategic Alignment, UX & Delight, Simplicity & Clarity, Long-term Maintainability & Vision Fit, Edge-case & Business Nuance (each 0–100)
   - References product-taste/ wiki pages for judgement
   - Output: overall score, per-dimension breakdown, verdict (Approve/Minor Changes/Major Changes/Reject)

5. **taste_learning_loop.md** — Self-improving taste
   - On manual PR rejection/editing: extract feedback, add to good-bad-examples.md, update taste-rubric.md if new principles, create bead
   - Turns every correction into permanent institutional knowledge

### Directory Structure

```
~/research-wiki/
├── raw/                  # Paper PDFs / text extracts
├── canonical-repos/      # High-quality reference repos
├── test-prs/             # Historical PR descriptions + diffs
├── wiki/
│   ├── index.md
│   └── product-taste/    # Product Taste Layer
├── skills/               # 5 skills above
├── program.md            # Wiki compiler instructions
├── results.md            # Master experiment log
└── scripts/
    └── verify_setup.sh   # Bootstrap verification script
```

## Connections

- [[SelfCritiqueVerificationLoop]] — the verification loop skill
- [[AutoResearchLoop]] — the meta-research loop skill
- [[CanonicalCodeScorer]] — the scoring engine concept
- [[ProductJudge]] — the product taste oracle skill
- [[TasteLearningLoop]] — the taste learning skill
- [[ProductTasteLayer]] — the full product taste subsystem

## Contradictions

- None yet — this is a new subsystem for this wiki
