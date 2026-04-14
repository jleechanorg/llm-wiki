---
title: "FM-Agent"
type: concept
tags: [formal-methods, hoare-logic, code-verification, bug-finding, compositional-reasoning]
sources: [fm-agent-paper.md]
last_updated: 2026-04-14
---

## Summary
FM-Agent scales formal methods to large real-world codebases (up to 143k LOC) by using LLMs to automatically generate function-level specifications via a top-down Hoare-style reasoning paradigm. It derives specs from caller expectations (capturing developer intent even when called functions are buggy), generalizes Hoare inference to natural language, and automatically generates test cases to confirm bugs — finding 522 previously unknown bugs in already-tested systems.

## How It Works
1. **Top-down specification generation**: LLM infers function specs from what callers expect, not from formal annotations
2. **Natural-language Hoare inference**: Extends classical Hoare triples {P} c {Q} to work with natural-language pre/post-conditions
3. **Compositional reasoning**: Breaks large systems into smaller components, verifies each independently
4. **Automated test generation**: Generates concrete test inputs that trigger and confirm detected bugs

## Key Insight
The critical bottleneck in scaling formal methods is specification authorship — writing formal specs for every function is prohibitively expensive. FM-Agent circumvents this by deriving specs from caller expectations (what the code is *used* for) rather than requiring explicit formal annotations. Even when a called function is buggy, the caller's expectations encode the intended behavior, so the discrepancy becomes the bug signal.

## Results
- Systems up to 143k lines of code reasoned about within 2 days
- 522 newly discovered bugs in already-tested systems
- Bugs caused system crashes and incorrect execution results

## Complementary Approaches
- **vs [[SWE-Shepherd]]**: SWE-Shepherd guides agent *during* code generation (step-level steering); FM-Agent verifies code *after* generation (post-hoc checking). They address different failure modes: generation missteps vs verification gaps.
- **vs traditional formal methods**: Traditional tools (CBMC, KLEE) require formal specs; FM-Agent generates specs automatically from natural language and caller context.
- **vs LLM self-verification**: FM-Agent uses structured Hoare-style reasoning rather than unstructured LLM self-critique, providing stronger correctness guarantees.

## Connections
- [[HoareLogic]] — formal foundation extended to natural language
- [[FormalVerification]] — the overarching goal at scale
- [[CompositionalReasoning]] — key technique for scaling to large systems
- [[TestCaseGeneration]] — automated bug confirmation
- [[SWE-Shepherd]] — complementary: guides generation vs verifies output
