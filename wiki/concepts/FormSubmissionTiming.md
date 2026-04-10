---
title: "Form Submission Timing"
type: concept
tags: [timing, performance, ui]
sources: ["campaign-wizard-timing-tests"]
last_updated: 2026-04-08
---

## Description
UI pattern ensuring form submission happens immediately when triggered (within 10ms), without artificial setTimeout delays that create unnecessary wait times for users.

## Key Principles
- No artificial delays between user action and submission
- Progress animation is visual feedback only
- Real completion can override progress animation state

## Related Concepts
- [[NonBlockingAnimation]] — visual feedback that doesn't block execution
- [[ProgressiveEnhancement]] — loading states enhance rather than block
