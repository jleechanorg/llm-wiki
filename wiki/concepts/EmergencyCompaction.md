---
title: "EmergencyCompaction"
type: concept
tags: [context-management, emergency, compaction]
sources: ["context-budgeting-allocation-tdd-tests"]
last_updated: 2026-04-08
---

## Description
Fallback mechanism triggered when system instruction exceeds 100k tokens (SYSTEM_INSTRUCTION_EMERGENCY_THRESHOLD). Unlike normal allocation which allows system instruction up to 42% of budget, emergency compaction aggressively reduces system instruction size to fit within limits.

## Trigger Condition
System instruction tokens > 100k (regardless of remaining budget)
