---
title: "GitHub Actions expression comment trap"
type: concept
tags: [github-actions, yaml, expression-syntax, ci]
date: 2026-07-07
---

## Concept
A `#` character starts a YAML comment only in the surrounding YAML document — it has no special meaning once inside the string content of a GitHub Actions expression (`${{ ... }}`, or the folded-scalar body of a multi-line `if: >-` block). The Actions expression lexer has no comment syntax at all, so a `#` placed inside an `if: >-` expression is parsed as literal, invalid expression text, producing a parse/`startup_failure` for the entire workflow.

## Why it's dangerous
This is not a soft failure — the workflow fails to even start. Because workflow-file triggers such as `issue_comment` and `workflow_dispatch` always load the workflow definition from `main`'s copy (not the PR branch's), a single bad `#` placement merged to `main` breaks the workflow on every branch and every PR simultaneously.

## Detection
`actionlint` catches this precisely: `got unexpected character '#' while lexing expression, expecting 'a'..'z', 'A'..'Z', '_', ...` with an exact line number. Run `actionlint` on any workflow with a multi-line `if: >-` block before merging.

## Fix
Move comments above the `if:` key, entirely outside the expression body, keeping the expression itself byte-identical.

## Connections
- [[project-2026-07-07-pr8198-ci-workflow-regressions]] — the incident this concept was extracted from (worldarchitect.ai PR #8192 regression, fixed in PR #8198)
- [[GitHubActionsReusableWorkflowConcurrencyCollision]] — sibling bug class, same incident
