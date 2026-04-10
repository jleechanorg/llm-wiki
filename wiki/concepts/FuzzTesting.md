---
title: "Fuzz Testing"
type: concept
tags: [testing, quality-assurance, input-validation]
sources: ["game-state-initialization-safety-tests"]
last_updated: 2026-04-08
---

## Description
Software testing technique that provides random/invalid input to discover bugs and validate error handling. In this context, fuzz tests verify that GameState handles extreme inputs (None, garbage types, malformed dicts) without crashing.

## Key Principles
- Test boundary conditions and unexpected input types
- Expect graceful failure, not crashes
- Validate that error messages/corrections are returned, not exceptions raised

## Related Tests
- [[GameState]] fuzz tests validate defensive defaults
