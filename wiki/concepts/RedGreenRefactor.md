---
title: "Red-Green-Refactor"
type: concept
tags: [tdd, testing, workflow]
sources: [modal-agent-intent-classifier-tdd-tests]
last_updated: 2026-04-08
---

## Description
TDD workflow pattern where tests are written first (RED - tests fail), then code is fixed to make tests pass (GREEN), then implementation is cleaned up (REFACTOR) while keeping tests green.

## Application
PR #5225 tests use this pattern to capture bugs before implementing fixes.
