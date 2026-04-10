---
title: "Zero Artificial Delays"
type: concept
tags: [performance, ui, timing, user-experience]
sources: []
last_updated: 2026-04-08
---

## Description
A performance principle requiring that UI interactions complete immediately without artificial waiting periods. Form submissions must complete within 10ms of user action, and progress animations must be purely visual—they cannot block the actual submission flow.

## Implementation Requirements
1. Form submission happens within 10ms of button click
2. Progress animation is visual-only, never blocks submission
3. completeProgress() can override animation when backend finishes
4. No setTimeout delays in critical form submission path

## Related Tests
- [[Campaign Wizard Timing Tests]] — validates zero artificial delays enforcement

## Connections
- [[UserExperience]] — directly impacts perceived performance
- [[ProgressiveEnhancement]] — ensures functionality without blocking UI
