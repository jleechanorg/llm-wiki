---
title: "Dual Agent Architecture"
type: concept
tags: [AI-architecture, code-review, quality-assurance]
sources: [openai-harness-ryan-notes]
last_updated: 2026-04-08
---

## Definition

Separating the roles of execution and evaluation by using two distinct AI agents: a Generator that writes code and a Reviewer Agent that validates against documented standards.

## The Two Roles

### Generator (Coding Agent)
- Translates linear text prompt into functional code
- Reads relevant constraints and attempts to solve the problem
- Prone to the same oversights as humans (different algorithmic reasons)

### Evaluator (Reviewer Agent)
- Spun up via GitHub Actions when PR is opened
- Given narrow mandate: "Read reliability.md, assess diff, report only P2+ violations"
- Near-infinite patience, zero review fatigue
- Scans every line against markdown rules

## Key Insight

> "Coding agents possess near-infinite patience and zero review fatigue. They will meticulously scan every line of the diff against the markdown rules. This eliminates the 'fiddly' work that humans typically dread."

## Result

Creates an almost impenetrable, ~100% reliable programmatic gate for non-functional requirements (reliability, security, etc.).

## The Stack

1. **Worker Agents** - Push completed features to PR
2. **Custom Review Bots** - Locally hosted AI reviewers checking constraints
3. **CodeRabbit** - Final arbiter, reads all bot comments
4. **Human** - Only if consensus not reached

Current confidence rate: 60-70% autonomous merge decisions

## Connections

- [[HarnessEngineering]] - Part of the harness
- [[CodeRabbit]] - AI review tool
- [[ProofOfWork]] - Evidence-based validation
