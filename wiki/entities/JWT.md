---
title: "JWT"
type: entity
tags: [authentication, token, security]
sources: ["auth-resilience-clock-skew-tests"]
last_updated: 2026-04-08
---

## Description
JSON Web Token authentication system used in WorldArchitect.AI. Vulnerable to clock skew errors when client time differs from server time, causing "Token used too early" errors.

## Related Concepts
- [[AuthenticationResilience]] — handling JWT failures gracefully
- [[ClockSkewHandling]] — detecting and correcting time mismatches
