---
title: "Web-advice browser transport split"
type: feedback
date: 2026-08-31
tags: [browser-automation, playwright, web-advice, review-provenance]
---

# Web-advice browser transport split

For `/web-advice`, use the owning app's browser and a newly created vendor
chat in app sessions. CLI/Bash runs use a clean strict-headless Chrome process
through Playwright with fresh local cookie state. Do not reuse a shared GUI
conversation as a CLI review transport.

The successful PR #9583 run established the acceptance proof: Perplexity Pro
showed both exact packet attachment chips and the fresh app-browser response
echoed the exact head SHA and both packet names. A shared chat later showed a
different PR's response, which is invalid provenance even if its attachments
look correct.

Headless uploads must use vendor-specific visible controls. Treat a login or
plan gate, missing attachment chips, or absent packet echo as a failed seat,
not as a completed review.

Source: `raw/feedback_2026-08-31_web_advice_browser_transport_split.md`.
Related concepts: [[BrowserAutomation]], [[Playwright]], [[RealBrowserTesting]].
