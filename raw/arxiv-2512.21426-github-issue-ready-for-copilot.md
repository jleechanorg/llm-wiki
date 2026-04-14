---
title: "What Makes a GitHub Issue Ready for Copilot?"
type: paper
tags: [GitHub-issues, Copilot, issue-quality, prompt-engineering]
date: 2025-12-24
arxiv_url: https://arxiv.org/abs/2512.21426
---

## Summary

Studies what makes a GitHub issue ready for AI coding agents like Copilot. Developed 32 detailed quality criteria for evaluating GitHub issues. Found that merged PRs tend to originate from shorter, well-scoped issues with clear guidance and hints about relevant artifacts. Model achieved 72% AUC for predicting merge likelihood.

## Key Claims

- **32 detailed quality criteria** for evaluating GitHub issues
- Merged PRs: shorter, well-scoped, containing clear guidance and hints
- Issues referencing external dependencies/APIs/config setups correlated with **lower merge rates**
- **72% AUC** median for predicting merge likelihood

## Method

- Developed interpretable ML model from 32 quality criteria
- Compared issues leading to merged vs closed pull requests
- Analyzed what issue features predict successful agent-assisted outcomes

## Connections

- Relevant to [[AgenticMuch]] — adoption of coding agents
- Evidence for importance of [[HarnessEngineering]] — issue quality as harness
- [[WhatMakesAGitHubIssueReadyForCopilot]] informs prompt design
