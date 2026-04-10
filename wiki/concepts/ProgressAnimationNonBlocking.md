---
title: "Progress Animation (Non-Blocking)"
type: concept
tags: [ui, animation, async, user-experience]
sources: []
last_updated: 2026-04-08
---

## Description
A design pattern where visual progress indicators run independently of actual backend operations. The animation provides feedback to users without impeding the submission flow.

## Key Patterns
- Animation is purely visual, fires immediately on user action
- Backend completion can call completeProgress() to override animation
- Animation does not use setTimeout or other delays in critical path
- Graceful handling when backend finishes before animation completes

## Related Tests
- [[Campaign Wizard Timing Tests]] — validates non-blocking progress animation behavior

## Connections
- [[ZeroArtificialDelays]] — part of the zero-delay principle
- [[AsyncUI]] — handles async completion patterns
