---
title: "Web-advice browser transport split"
type: source
tags: [browser-automation, playwright, web-advice]
date: 2026-08-31
source_file: raw/feedback_2026-08-31_web_advice_browser_transport_split.md
---

## Summary

`/web-advice` needs two provenance-safe browser routes: an owned built-in
browser for app sessions and a fresh direct Chrome process for CLI sessions.
Shared chat state invalidates review attribution; attachment chips alone do
not make a response attributable to the intended request.

## Key Claims

- Direct Playwright can launch the installed Chrome in strict headless mode.
- A fresh chat, exact attachment chips, and a packet echo are required for a
  trustworthy vendor result.
- Perplexity and Gemini require menu-driven file chooser handling rather than
  generic file-input selection.

## Connections

- [[BrowserAutomation]] — headless browser transport and isolation.
- [[Playwright]] — direct Chrome control for CLI execution.
- [[RealBrowserTesting]] — provenance requirements for a real vendor review.
