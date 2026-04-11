---
title: "Browser Automation Workflows"
type: source
tags: [browser-automation, playwright, superpowers-chrome, testing, workflows, worldarchitect]
source_file: "raw/browser-automation-workflows.md"
sources: []
last_updated: 2026-04-07
---

## Summary
Practical workflows combining Playwright and Superpowers Chrome for WorldArchitect.AI testing. Four distinct workflows cover daily development, PR visual regression, bug investigation, and CI/CD pipeline integration.

## Key Claims

- **Daily Development Testing**: Superpowers Chrome for quick checks (1-2s) + Playwright for comprehensive validation before commit (5-10min)
- **PR Visual Regression**: Playwright-only workflow with baseline management and automated diff generation (8-12s per page)
- **Bug Investigation**: Chrome for fast reproduction (2-5min) + Playwright for verification and regression test creation
- **CI/CD Pipeline**: Staged approach with quick smoke test (30s) running before full E2E suite (10min)

## Key Quotes

> "Why This Workflow: Fast iteration with Chrome during dev, comprehensive validation before commit, minimal overhead for quick checks"

> "Why Playwright: Built-in visual regression system, baseline management, automated diff generation, multi-viewport support"

## Connections
- [[Playwright]] — comprehensive testing with visual regression
- [[Superpowers Chrome]] — fast, lightweight browser automation
- [[WorldArchitect.AI]] — project this workflow supports
- [[Browser Automation Comparison]] — detailed tool comparison

## Contradictions
- None identified
