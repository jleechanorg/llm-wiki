---
title: "Auto-Research Experiment Program"
type: source
tags: [auto-research, meta-research]
date: 2026-04-14
source_file: research-wiki-program.md
---

## Summary

The compiler rules for the AUTO-RESEARCH EXPERIMENT v2.1 system — a self-discovering meta-research loop combining LLM wiki, self-critique verification, canonical code scoring, and product taste evaluation.

## What It Covers

- **Golden Rule**: Never hallucinate; read from disk only (raw/, canonical-repos/, test-prs/, skills/, results.md, beads/)
- **Directory Structure**: Full layout of all experiment directories
- **The 5 Skills**: When to use each (auto_research_loop, self_critique_verification_loop, canonical_code_scorer, product_judge, taste_learning_loop)
- **How to Read Sources**: Papers (raw/), canonical repos, test PRs
- **How to Update results.md**: Append-only format per cycle
- **How to Maintain the Wiki**: concept page format, "Results on My Codebase" section
- **How to Create Beads**: format for ~/.beads/
- **Full Experiment Cycle**: master orchestration step-by-step
- **Exit Criteria**: when to stop

## Key Principles

1. Never hallucinate — only read from disk
2. All results are append-only to results.md
3. Every experiment creates a bead in ~/.beads/
4. 3-iteration cap on self-critique loop
5. Canonical scorer formula: 0.7 × rubric Pass-rate + 0.3 × diff similarity

## Connections

- [[AutoResearchExperiment]] — Full system concept
- [[CanonicalCodeScorer]] — Scored 77/100 on this codebase
- [[SelfCritiqueVerificationLoop]] — Inner verification loop
