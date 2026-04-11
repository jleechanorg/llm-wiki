---
title: "Code Reviewer Agent Definition"
type: source
tags: [claude-code, agent, code-review, quality-assurance]
date: 2026-04-07
source_file: /Users/jleechan/.claude/agents/code-reviewer.md
last_updated: 2026-04-07
---

## Summary
Defines a Claude Code agent for expert code review that identifies bugs, logic errors, security vulnerabilities, and code quality issues. Uses confidence-based filtering to report only high-priority issues (confidence ≥ 80) and defaults to reviewing unstaged changes from `git diff`.

## Key Claims
- **Agent Type**: Expert code reviewer for modern software development across multiple languages and frameworks
- **Default Scope**: Unstaged changes from `git diff` (user may specify different files)
- **Confidence Scoring**: 0-100 scale, only issues with confidence ≥ 80 reported
- **Core Responsibilities**: Project guidelines compliance, bug detection, code quality evaluation

## Confidence Scoring System
| Score | Meaning |
|-------|---------|
| 0 | False positive, doesn't stand up to scrutiny |
| 25 | Somewhat confident, might be false positive |
| 50 | Moderately confident, real issue but nitpick |
| 75 | Highly confident, verified real issue important to functionality |
| 100 | Absolutely certain, happens frequently in practice |

## Review Responsibilities

### Project Guidelines Compliance
Verifies adherence to explicit project rules (CLAUDE.md or equivalent) including:
- Import patterns
- Framework conventions
- Language-specific style
- Function declarations
- Error handling
- Logging
- Testing practices
- Platform compatibility
- Naming conventions

### Bug Detection
Identifies actual bugs impacting functionality:
- Logic errors
- Null/undefined handling issues
- Race conditions
- Memory leaks
- Security vulnerabilities
- Performance problems

### Code Quality
Evaluates significant issues:
- Code duplication
- Missing critical error handling
- Accessibility problems
- Inadequate test coverage

## Output Guidance
- Start by stating what is being reviewed
- For each high-confidence issue, provide: description with score, file path and line number, guideline reference or bug explanation, concrete fix suggestion
- Group by severity (Critical vs Important)
- If no high-confident issues exist, confirm code meets standards

## Connections
- [[ClaudeCode]] — the platform this agent runs on
- [[CodeQuality]] — the concept of evaluating code quality
- [[ConfidenceScoring]] — the confidence-based filtering pattern

## Contradictions
None identified — this is a skill/agent definition file, not a claim about world state.
