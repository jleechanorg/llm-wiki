---
title: "Capture Analysis Framework"
type: source
tags: [capture, mock-validation, testing, service-interactions]
sources: []
last_updated: 2026-04-14
---

## Summary

Analyzes captured real service interactions and compares with mock responses. Supports performance analysis (duration, slowest/fastest operations), error tracking, service breakdown, and accuracy scoring. Also provides mock baseline generation from real capture data.

## Key Claims

- **CaptureAnalyzer Class**: Main analysis class that examines capture files from last N days
- **Performance Analysis**: Tracks total/avg duration, identifies slowest and fastest operations
- **Service Breakdown**: Groups interactions by service with operation counts and error rates
- **Mock Comparison**: `compare_with_mock()` compares real responses with mock and identifies gaps
- **Mock Baseline Creation**: `create_mock_baseline()` generates mock responses from first successful real response per service.operation
- **Deep Comparison**: Recursive dict/list comparison with path tracking for nested differences
- **Accuracy Score**: Calculates match percentage as `matches / total_comparisons`

## Key Quotes

> "Analyzes captured service interactions and compares with mock data"

> "Use the first successful response as the mock baseline"

> "Compare real and mock responses for differences"

## Connections

- [[APIMocking]] — mock validation framework
- [[APITesting]] — testing utilities
- [[ServiceLayer]] — services being captured

## Contradictions

- None identified