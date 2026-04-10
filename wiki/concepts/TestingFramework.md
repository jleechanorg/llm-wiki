---
title: "Testing Framework"
type: concept
tags: [testing, infrastructure, python]
sources: [worldarchitect-ai-code-coverage-report-mvp-site]
last_updated: 2026-04-08
---

Python testing infrastructure for WorldArchitect.AI located in testing_framework/ directory. Contains 1,500+ lines across capture.py, capture_analysis.py, capture_cli.py, fixtures.py, integration_utils.py, and test validation modules. Exists separately from mvp_site module and includes mock_provider.py and real_provider.py for service simulation.

## Components
- [[CaptureFramework]] — API call recording and playback
- [[CaptureAnalyzer]] — service interaction analysis
- Mock providers for Firestore and Gemini services
- Integration test utilities

## Current State
- Testing framework present but not integrated with mvp_site test execution
- Coverage report shows 0% execution against main codebase
