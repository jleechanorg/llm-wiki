---
title: "Conversation History"
type: concept
tags: [context, detection, loop-tracking]
sources: [planning-loop-detection-social-encounters-red-tests.md]
last_updated: 2026-04-08
---

## Summary
Context tracking mechanism used to detect planning loops by analyzing previous user messages for similar action patterns.

## Detection Logic
The test tracks conversation history to detect loops:
1. Collect all user messages
2. Check for similar action keywords: ["press", "maintain", "logical", "argument", "pressure", "mathematical"]
3. Count matches
4. When count >= 2, loop is detected

## Why It Matters
Without conversation history tracking, the system cannot detect when users are stuck in loops and cannot enforce the [[AntiLoopRule]].

## Connections
- [[AntiLoopRule]] — uses conversation history to detect loops
- [[PlanningLoopDetection]] — the bug this detects
- [[UserMessage]] — individual messages being tracked
