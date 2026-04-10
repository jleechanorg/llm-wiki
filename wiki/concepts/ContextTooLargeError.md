---
title: "ContextTooLargeError"
type: concept
tags: [errors, context-management]
sources: [entity-tracking-budget-fix-end2end-test, context-too-large-error-handling-tests]
last_updated: 2026-04-08
---

Error thrown when LLM prompt exceeds token budget. The entity tracking budget fix prevents this by reserving tokens in the scaffold calculation rather than adding entity tracking after truncation.