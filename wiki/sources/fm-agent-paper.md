---
title: "FM-Agent: Scaling Formal Methods to Large Systems via LLM-Based Hoare-Style Reasoning"
type: source
tags: [formal-methods, hoare-logic, code-verification, bug-finding, llm-agents, compositional-reasoning]
sources: []
last_updated: 2026-04-14
---

## Summary
FM-Agent is the first framework to achieve automated compositional reasoning for large-scale systems using LLM-based Hoare-style reasoning. It introduces a top-down paradigm that automatically generates function-level specifications from caller expectations, generalizing Hoare inference to work with natural-language specs instead of formal formulas. The system successfully reasoned about systems up to 143k lines of code within 2 days, discovering 522 previously unknown bugs in already-tested systems.

## Key Claims
- First framework to achieve automated compositional reasoning for large-scale systems
- Top-down specification generation: derives function specs from caller expectations, capturing developer intent even with buggy code
- Generalizes Hoare-style inference to work with natural-language specifications (not just formal formulas)
- Automatically generates test cases to confirm and explain bugs found
- Successfully reasoned about systems up to 143k lines of code within 2 days
- Found 522 newly discovered bugs in already-tested systems (causing crashes and incorrect execution)

## Key Quotes
> "LLM-assisted software development can generate large-scale systems like compilers, making code correctness verification crucial." — Motivation

> "While Hoare logic enables compositional reasoning by decomposing systems into smaller components, existing approaches require manual formal specifications for each function—a burden especially problematic when code is AI-generated and developers lack deep understanding of function behavior." — Problem statement

> "Discovered 522 previously unknown bugs in already-tested systems." — Key result

## Methodology
1. Top-down paradigm: leverage LLMs to automatically generate function-level specifications
2. Derive specifications from caller expectations (capturing developer intent even when the called function is buggy)
3. Generalize Hoare-style inference to work with natural-language specifications
4. Automatically generate test cases that trigger potential bugs and confirm them

## Results
- Systems up to 143k lines of code reasoned about within 2 days
- 522 newly discovered bugs found in already-tested systems
- Bugs caused serious consequences: system crashes and incorrect execution results

## Connections
- [[HoareLogic]] — the formal foundation this paper extends to natural language
- [[FormalVerification]] — the broader goal this paper advances at scale
- [[CodeAgents]] — complements LLM code generation with verification
- [[TestCaseGeneration]] — automated test generation for bug confirmation
- [[CompositionalReasoning]] — breaking systems into smaller verifiable components

## Paper Info
- **Authors:** Haoran Ding, Zhaoguo Wang, Haibo Chen
- **arXiv:** 2604.11556
- **Submitted:** April 14, 2026
- **Category:** cs.SE
