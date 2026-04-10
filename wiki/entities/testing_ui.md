---
title: "testing_ui"
type: entity
tags: [testing, module, python]
sources: []
last_updated: 2026-04-08
---

## Summary
Test infrastructure module providing test base classes for browser testing. Contains BrowserTestBase and ByokBrowserTestBase with configurable test user email via environment variables.

## Key Components
- BrowserTestBase — base class for standard browser tests
- ByokBrowserTestBase — BYOK variant with separate email env var
- DEFAULT_TEST_EMAIL — constant defaulting to jleechantest@gmail.com

## Connections
- Provides test infrastructure for [[worldarchitect]] browser tests
