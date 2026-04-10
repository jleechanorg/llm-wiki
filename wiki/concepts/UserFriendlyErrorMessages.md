---
title: "User-Friendly Error Messages"
type: concept
tags: [ux, error-handling, frontend]
sources: ["auth-resilience-clock-skew-tests"]
last_updated: 2026-04-08
---

## Description
Frontend approach to displaying clear, actionable error messages instead of technical error details.

## Message Types
- "Authentication timing issue detected" — for clock skew errors
- "Would you like to try again?" — with retry button (showRetryOption)
- "Network connection issue" — for network failures
- "Authentication issue" — for auth failures

## Related Entities
- [[AppJs]] — displays the messages
- [[AuthenticationResilience]] — overall error strategy
