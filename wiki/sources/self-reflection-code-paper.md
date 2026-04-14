---
title: "Generating Equivalent Representations of Code By A Self-Reflection Approach"
type: source
tags: [self-reflection, code-representation, self-debugging, LLM]
sources: []
date: 2024-10-04
source_file: raw/arxiv-2410.21014-self-reflection-code.md
---

## Summary

This paper introduces a self-reflection approach for generating Equivalent Representations (ERs) of code — textual representations that preserve code semantics like natural language comments and pseudocode. The method enables two LLMs to work mutually and produce an ER through an iterative reflection process. The paper addresses both open settings (no constraints) and constrained settings (specific formats like comments, pseudocode, flowcharts).

## Key Claims

- Two LLMs collaborate through iterative reflection to generate semantic-preserving code representations
- Addresses both open and constrained generation settings
- Presents eight empirical findings about how LLMs understand syntactic structures, APIs, and numerical computations
- Demonstrates applicability across various software engineering tasks through constraint-based generation
- Iterative reflection improves representation quality over single-pass generation

## Technique/Method

- **Dual-LLM collaboration**: two models mutually evaluate and refine representations
- **Iterative reflection**: multiple rounds of generation → evaluation → refinement
- **Constraint-based generation**: supports structured outputs (comments, pseudocode, flowcharts)
- **Semantic preservation checking**: reflection ensures output maintains original code semantics

## Connections

- Self-reflection as precursor to self-debugging in agentic coding pipelines
- Empirical findings about LLM code understanding useful for harness design
- Related to [[SelfRefine]] — iterative refinement process
