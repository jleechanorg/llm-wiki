---
title: "Browser Automation Workflows"
type: source
tags: [playwright, superpowers-chrome, browser-automation, testing, workflows, worldarchitect, cdp, ci-cd]
sources: [worldarchitect.ai-docs-browser_automation_comparison.md-cf793872]
date: 2026-04-07
source_file: raw/browser_automation_workflows.md
last_updated: 2026-04-07
---

## Summary
Practical workflows combining Playwright and Superpowers Chrome for WorldArchitect.AI testing, covering daily development, PR visual regression, bug investigation, and CI/CD pipelines. Each workflow optimizes for different goals: speed during development, comprehensive validation before commit, fast bug reproduction, and automated CI testing.

## Key Claims

- **Workflow 1 (Daily Dev Testing)**: Superpowers Chrome for fast 1-2s checks during development, Playwright for comprehensive 5-10min E2E validation before commit
- **Workflow 2 (PR Visual Regression)**: Playwright-only approach with built-in baseline management, automated diff generation, and multi-viewport support (8-12s per page)
- **Workflow 3 (Bug Investigation)**: Chrome for fast 2-5min reproduction and exploration, Playwright for reliable verification and permanent regression tests
- **Workflow 4 (CI/CD Pipeline)**: Staged approach - quick 30s smoke test with Chrome first, then full 10min E2E suite with Playwright; visual regression runs on PRs only

## Key Quotes

> "Fast iteration with Chrome during dev, comprehensive validation before commit, minimal overhead for quick checks" — Workflow 1 rationale

> "Quick bug reproduction with Chrome, persistent session for investigation, reliable verification with Playwright, creates regression test" — Workflow 3 rationale

## Connections

- [[Browser Automation Comparison]] — this workflow guide builds on the comparison document
- [[Testing MCP]] — E2E testing framework referenced in workflow implementations

## Contradictions

- None identified - this document complements the comparison guide with practical application