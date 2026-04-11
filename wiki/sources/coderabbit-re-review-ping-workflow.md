---
title: "CodeRabbit Re-Review Ping Workflow"
type: source
tags: ["coderrabbit", "code-review", "automation", "workflow", "github"]
date: 2026-04-07
source_file: "raw/llm_wiki-raw-coderabbit-re-review-ping.md"
sources: []
last_updated: 2026-04-07
---

## Summary
Documentation of the correct CodeRabbit re-review ping workflow including exact comment format, timing rules, and deduplication logic. Addresses common misconfigurations that caused re-review failures.

## Key Claims
- **Correct handle**: Must use `@coderabbitai` (no hyphen, includes `ai`) — other variants like `@coderabbit-ai` or `@coderabbit` do not trigger re-review
- **Correct timing**: Post only after pushing at least one new commit addressing CodeRabbit review comments — never on a schedule or before fixes
- **Deduplication**: Post at most once per push; skip if recent "all good?" comment already exists for the same head commit

## Key Quotes
> "Post exactly `@coderabbitai all good?`" — correct comment format

> "Only after you have **pushed at least one new commit** that addresses CodeRabbit review comments" — timing rule

## Connections
- [[CodeRabbit]] — the AI code review tool being configured
- [[GitHubAutomation]] — this workflow is part of PR automation

## Contradictions
- None identified
