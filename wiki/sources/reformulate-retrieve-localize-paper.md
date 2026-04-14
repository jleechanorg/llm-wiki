---
title: "Reformulate, Retrieve, Localize: Agents for Repository-Level Bug Localization"
type: source
tags: [bug-localization, retrieval, SWE-agent, BM25]
sources: []
date: 2025-12-07
source_file: raw/arxiv-2512.07022-reformulate-retrieve-localize.md
---

## Summary

LLM-powered agent for repository-level bug localization using query reformulation. Achieves 35% better ranking in first-file retrieval vs BM25 baseline, and +22% improvement over SWE-agent.

## Key Claims

- Bug localization remains "critical yet time-consuming" in large-scale repositories
- Query reformulation significantly improves localization accuracy
- **35%** better ranking vs BM25 baseline
- **+22%** improvement over SWE-agent

## Technique/Method

- Non-fine-tuned LLM extracts key information from bug reports
- Reformulates queries pre-retrieval (identifiers, code snippets)
- BM25 retrieval using preprocessed queries

## Connections

- Related to [[SWE-Agent]] — bug localization improvements
- Related to [[E3-TIR]] — tool-integrated reasoning
