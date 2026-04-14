---
title: "Are Coding Agents Generating Over-Mocked Tests?"
type: source
tags: [coding-agent, testing, mocks, empirical, software-quality]
sources: []
date: 2026-01-30
source_file: raw/arxiv-2602.00409-coding-agents-over-mocked-tests.md
---

## Summary

Empirical study analyzing 1.2M+ commits from 2025 across 2,168 repositories. Found that coding agents generate more tests with mocks than human developers: 23% vs 13% for test file changes, 36% vs 26% for mock additions.

## Key Claims

- Agents add/change test files in **23%** of commits vs **13%** for non-agents
- Agents add mocks in **36%** of commits vs **26%** for non-agents
- **60%** of repositories with agent activity showed agent test activity
- **68%** of those also showed agent mock activity
- Study of **1.2M+ commits**, **48,563 agent commits**

## Method

Analyzed commits from 2025 across TypeScript, JavaScript, and Python repositories.

## Connections

- Evidence for test quality concerns in agent-generated code
- Related to [[EvoEval]] — benchmark integrity and quality
- Relevant to [[SelfGeneratedTestGeneration]]
