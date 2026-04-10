---
title: "Pytest"
type: concept
tags: [pytest, testing, framework, python, ci-cd]
sources: [pytest-configuration]
last_updated: 2026-04-08
---

## Definition
Pytest is a mature full-featured Python testing framework that simplifies test writing with fixtures, parametrization, and plugins. Used in WorldArchitect.AI for both unit and integration testing with dual-mode (mock/real) support.

## Key Features
- **Fixtures** — Dependency injection for test setup/teardown
- **Markers** — Test categorization (unit, integration, mock_only, real_only)
- **Parametrization** — Run tests with multiple parameter combinations
- **Plugins** — Extensible via `conftest.py` and third-party packages

## WorldArchitect.AI Usage
- [[PytestIntegrationForRealModeTestingFramework]] provides dual-mode fixtures
- [[RealModeTestingFrameworkMigration]] guides transition from mock-only to dual-mode
- Configuration uses `--cache-optimizer` and `--num-workers=4` for CI optimization
