---
title: "Token Budgeting"
type: concept
tags: [context-management, tokens, architecture]
sources: [context-budgeting-allocation-tdd-tests, entity-tracking-budget-fix-end2end-test]
last_updated: 2026-04-08
---

Process of allocating tokens across different components of an LLM prompt (system instructions, narrative, entity tracking, etc.) to prevent ContextTooLargeError. The ENTITY_TRACKING_TOKEN_RESERVE fix ensures entity tracking tokens are budgeted upfront.