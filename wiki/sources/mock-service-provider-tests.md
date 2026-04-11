---
title: "MockServiceProvider Unit Tests"
type: source
tags: [python, testing, mock, service-provider, interface]
source_file: "raw/test_mock_service_provider.py"
sources: []
last_updated: 2026-04-08
---

## Summary
Unit tests validating MockServiceProvider implementation, which provides mock instances of Firestore and LLM services for testing. Tests verify interface compliance, mock behavior, and service lifecycle management.

## Key Claims
- **Interface implementation**: MockServiceProvider correctly implements TestServiceProvider interface
- **Firestore mock**: get_firestore returns MockFirestoreClient with get_campaigns_for_user method
- **LLM mock**: get_gemini returns MockLLMClient with generate_content method
- **Service consistency**: Multiple calls return the same singleton instances
- **Cleanup behavior**: cleanup() resets operation counters to zero
- **Mock flag**: is_real_service returns False for mock provider

## Key Connections
- Related to [[MCP Server Health Checks]] — both validate service configuration
- Related to [[Flask App Import and Endpoint Tests]] — testing infrastructure

## Test Coverage
- Interface compliance verification
- Mock service instance creation
- Singleton pattern validation
- Cleanup and reset functionality
